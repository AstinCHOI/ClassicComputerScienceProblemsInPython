# list_compression.py
# From Classic Computer Science Problems in Python Chapter 5
# Copyright 2018 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations
from typing import Tuple, List, Any
from chromosome import Chromosome
from genetic_algorithm import GeneticAlgorithm
from random import shuffle, sample
from copy import deepcopy
from zlib import compress
from sys import getsizeof
from pickle import dumps

# 165 바이트 압축
PEOPLE: List[str] = ["Michael", "Sarah", "Joshua", "Narine", "David",
                     "Sajid", "Melanie", "Daniel", "Wei", "Dean", "Brian", "Murat", "Lisa"]


class ListCompression(Chromosome):
    def __init__(self, lst: List[Any]) -> None:
        self.lst: List[Any] = lst

    @property
    def bytes_compressed(self) -> int:
        return getsizeof(compress(dumps(self.lst)))

    def fitness(self) -> float:
        return 1 / self.bytes_compressed

    @classmethod
    def random_instance(cls) -> ListCompression:
        mylst: List[str] = deepcopy(PEOPLE)
        shuffle(mylst)
        return ListCompression(mylst)

    def crossover(self, other: ListCompression) -> Tuple[ListCompression, ListCompression]:
        child1: ListCompression = deepcopy(self)
        child2: ListCompression = deepcopy(other)
        idx1, idx2 = sample(range(len(self.lst)), k=2)
        l1, l2 = child1.lst[idx1], child2.lst[idx2]
        child1.lst[child1.lst.index(
            l2)], child1.lst[idx2] = child1.lst[idx2], l2
        child2.lst[child2.lst.index(
            l1)], child2.lst[idx1] = child2.lst[idx1], l1
        return child1, child2

    def mutate(self) -> None:  # 두 위치를 스왑한다.
        idx1, idx2 = sample(range(len(self.lst)), k=2)
        self.lst[idx1], self.lst[idx2] = self.lst[idx2], self.lst[idx1]

    def __str__(self) -> str:
        return f"순서: {self.lst} 바이트: {self.bytes_compressed}"


if __name__ == "__main__":
    initial_population: List[ListCompression] = [
        ListCompression.random_instance() for _ in range(100)]
    ga: GeneticAlgorithm[ListCompression] = GeneticAlgorithm(initial_population=initial_population, threshold=1.0, max_generations=100,
                                                             mutation_chance=0.2, crossover_chance=0.7, selection_type=GeneticAlgorithm.SelectionType.TOURNAMENT)
    result: ListCompression = ga.run()
    print(result)

# 저자가 테스트한 결과 각 세대에 1000 개체를 546번째 세대까지 실행했을 때, 제일 좋은 결과를 얻었다.
# 순서: ['Wei', 'Michael', 'Melanie', 'Daniel', 'Joshua', 'Narine', 'Lisa', 'Dean', 'Brian', 'David', 'Sajid', 'Sarah', 'Murat'] 바이트: 159
