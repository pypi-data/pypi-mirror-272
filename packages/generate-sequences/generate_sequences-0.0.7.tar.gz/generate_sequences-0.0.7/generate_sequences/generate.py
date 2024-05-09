import heapq
import warnings
from typing import Callable, Iterator, List, Union

import torch
import torch.nn.functional as F
import torch.utils
from tqdm.auto import tqdm

from generate_sequences.utils import sort_list_with_positions


class BaseGenerator:
    def __init__(
        self,
        decoder_start_token_id: int,
        eos_token_id: int,
        generation_forward: Callable[
            [Union[List[torch.Tensor], List[str]], torch.Tensor],
            torch.Tensor,
        ],
        max_length: int = 1_024,
        batch_size: int = 1,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        temperature: float = 1.0,
        use_tqdm: bool = True,
        multinomial_sampling: bool = False,
        sort_samples: bool = False,
    ) -> None:
        self.device = device
        self.use_tqdm = use_tqdm
        self.max_length = max_length
        self.batch_size = batch_size
        self.generation_forward = generation_forward
        self.eos_token_id = eos_token_id
        self.decoder_start_token_id = decoder_start_token_id
        self.temperature = temperature
        self.multinomial_sampling = multinomial_sampling
        self.sort_samples = sort_samples

    def get_batches(self, inputs: Union[List[torch.Tensor], List[str]]) -> Iterator[List[str]]:
        batched_inputs = inputs
        if self.sort_samples:
            sorted_inputs, inputs_positions = sort_list_with_positions(inputs)
            self.inputs_original_positions = inputs_positions
            batched_inputs = sorted_inputs

        for i in tqdm(
            range(0, len(batched_inputs), self.batch_size),
            disable=not self.use_tqdm,
            desc="Generating Sequences",
            total=len(batched_inputs) // self.batch_size,
        ):
            yield batched_inputs[i : i + self.batch_size]

    def restore_outputs_order(self, outputs):
        if not self.sort_samples:
            return outputs
        ordered_outputs = []
        for position in self.inputs_original_positions:
            ordered_outputs.append(outputs[position])
        return ordered_outputs


class GreedyGenerator(BaseGenerator):
    @torch.no_grad()
    def generate(self, inputs: Union[List[torch.Tensor], List[str]]) -> List[torch.Tensor]:
        outputs = []
        # add user warning if temperature is not 1.0 that greedy search is not appropriate
        if self.temperature != 1.0 and not self.multinomial_sampling:
            warnings.warn(
                "Temperature does not have an affect on Greedy search if multinomial sampling is set to False! If forgot to add multinomial sampling, set `multinomial_sampling=True` to the generator."
            )

        for batch_inputs in self.get_batches(inputs):
            batch_size = len(batch_inputs)
            decoder_inputs = torch.full(
                (batch_size, self.max_length),
                self.eos_token_id,  # Pre-fill with EOS; only overwrite if generating
                dtype=torch.long,
                device=self.device,
            )
            decoder_inputs[:, 0] = self.decoder_start_token_id
            finished_mask = torch.zeros(batch_size, dtype=torch.bool, device=self.device)

            for step in range(1, self.max_length):
                if finished_mask.all():
                    break  # Stop if all sequences are finished
                batch_outputs = self.generation_forward(batch_inputs, decoder_inputs[:, :step])
                batch_outputs = batch_outputs[:, -1, :]  # Get last tokens' outputs for the batch
                next_tokens = batch_outputs / self.temperature
                next_tokens = F.softmax(next_tokens, dim=-1)
                # check for multinomial sampling
                if self.multinomial_sampling:
                    next_tokens = torch.multinomial(
                        next_tokens,
                        num_samples=1,
                    ).squeeze()
                else:
                    next_tokens = torch.argmax(next_tokens, dim=-1)
                not_finished = ~finished_mask
                decoder_inputs[not_finished, step] = next_tokens[not_finished]
                finished_mask |= next_tokens == self.eos_token_id  # Update finished sequences
            outputs += decoder_inputs
        return self.restore_outputs_order(outputs)


class BeamNode:
    """Represents a node in a beam search. Stores token sequences and their associated score."""

    def __init__(self, tokens: List[int], score: float) -> None:
        self.tokens = tokens
        self.score = score


def default_beam_nodes_ordering_fn(
    node: BeamNode,
    eos_token_id: int,
    length_penalty: float = 1.0,
) -> float:
    """Calculates the adjusted score of a node for beam sorting. Applies length penalty to score."""
    tokens = node.tokens
    if eos_token_id in tokens:
        tokens = tokens[1 : tokens.index(eos_token_id) + 1]
    return node.score / (len(tokens) ** length_penalty)


# this implementation is inspired by:
# https://hussainwali.medium.com/simple-implementation-of-beam-search-in-python-64b2d3e2fd7e
class BeamSearchGenerator(BaseGenerator):
    def __init__(
        self,
        decoder_start_token_id: int,
        eos_token_id: int,
        generation_forward: Callable[
            [Union[List[torch.Tensor], List[str]], torch.Tensor],
            torch.Tensor,
        ],
        max_length: int = 1_024,
        batch_size: int = 1,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        temperature: float = 1.0,
        use_tqdm: bool = True,
        multinomial_sampling: bool = False,
        sort_samples: bool = False,
        beam_width: int = 4,
        length_penalty: float = 1.0,
        beam_nodes_ordering_function: Callable[
            [BeamNode, int, float], float
        ] = default_beam_nodes_ordering_fn,
    ) -> None:
        super().__init__(
            decoder_start_token_id,
            eos_token_id,
            generation_forward,
            max_length,
            batch_size,
            device,
            temperature,
            use_tqdm,
            multinomial_sampling,
            sort_samples,
        )
        self.beam_width = beam_width
        self.length_penalty = length_penalty
        self.beam_nodes_ordering_function = beam_nodes_ordering_function

    def get_top_nodes(self, nodes) -> List[BeamNode]:
        """Returns the top k nodes in the beam according to the ordering function."""
        return heapq.nlargest(
            self.beam_width,
            nodes,
            key=lambda node: self.beam_nodes_ordering_function(
                node,
                self.eos_token_id,
                self.length_penalty,
            ),
        )

    @torch.no_grad
    def generate(self, inputs: Union[List[torch.Tensor], List[str]]) -> List[torch.Tensor]:
        outputs = []
        for batch in self.get_batches(inputs):
            batch_nodes = [
                [
                    BeamNode(
                        tokens=[self.decoder_start_token_id],
                        score=0.0,
                    )
                ]
                for _ in range(len(batch))
            ]
            batch_best_nodes = batch_nodes
            for step in range(self.max_length):
                next_nodes: List[List[BeamNode]] = [[] for _ in range(len(batch))]
                batch_best_nodes = [
                    self.get_top_nodes(sample_nodes) for sample_nodes in batch_best_nodes
                ]
                # break when all best nodes ends with eos
                if all(
                    batch_best_nodes[sample_index][i].tokens[-1] == self.eos_token_id
                    for sample_index in range(len(batch))
                    for i in range(len(batch_best_nodes[sample_index]))
                ):
                    break
                # beam width, taking the case where k < len(best_beams_nodes[0]), i.e. in the first step
                beam_width = 1 if step == 0 else self.beam_width
                for k in range(beam_width):
                    decoder_input_ids = torch.LongTensor(
                        [sample_best_nodes[k].tokens for sample_best_nodes in batch_best_nodes]
                    ).to(self.device)
                    batch_outputs = self.generation_forward(batch, decoder_input_ids)
                    batch_outputs = batch_outputs[:, -1, :]
                    batch_outputs = batch_outputs / self.temperature
                    batch_outputs = F.log_softmax(batch_outputs, dim=-1)
                    # check for multinomial sampling
                    if self.multinomial_sampling:
                        topk_indices = torch.multinomial(
                            torch.exp(batch_outputs),
                            self.beam_width,
                            replacement=True,
                        )
                        topk_scores = batch_outputs.gather(1, topk_indices)
                    else:
                        topk_scores, topk_indices = torch.topk(batch_outputs, self.beam_width)
                    for sample_index in range(len(batch)):
                        if batch_best_nodes[sample_index][k].tokens[-1] == self.eos_token_id:
                            next_nodes[sample_index] += [
                                BeamNode(
                                    tokens=batch_best_nodes[sample_index][k].tokens
                                    + [self.eos_token_id],
                                    score=0,
                                )
                            ] * self.beam_width
                        else:
                            next_nodes[sample_index] += [
                                BeamNode(
                                    tokens=batch_best_nodes[sample_index][k].tokens
                                    + [topk_indices[sample_index][i].item()],
                                    score=batch_best_nodes[sample_index][k].score
                                    + topk_scores[sample_index][i].item(),
                                )
                                for i in range(self.beam_width)
                            ]

                batch_best_nodes = next_nodes  # Update beams for the next time step

            batch_predictions = []
            for sample_nodes in batch_best_nodes:
                best_node = max(
                    sample_nodes,
                    key=lambda node: self.beam_nodes_ordering_function(
                        node,
                        self.eos_token_id,
                        self.length_penalty,
                    ),
                )
                batch_predictions.append(best_node.tokens)
            outputs += batch_predictions
        return self.restore_outputs_order(outputs)
