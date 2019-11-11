# knapsack.py
# From Classic Computer Science Problems in Python Chapter 9
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
from typing import NamedTuple, List


class Item(NamedTuple):
    name: str
    weight: int
    value: float


def knapsack(items: List[Item], max_capacity: int) -> List[Item]:
    # 동적 프로그래밍 표를 작성한다.
    table: List[List[float]] = [
        [0.0 for _ in range(max_capacity + 1)] for _ in range(len(items) + 1)]
    for i, item in enumerate(items):
        for capacity in range(1, max_capacity + 1):
            previous_items_value: float = table[i][capacity]
            if capacity >= item.weight:  # 물건이 용량에 맞는 경우
                value_freeing_weight_for_item: float = table[i][capacity - item.weight]
                # 이전 물건보다 더 가치가 있는 경우에만 물건을 넣는다.
                table[i + 1][capacity] = max(value_freeing_weight_for_item +
                                             item.value, previous_items_value)
            else:  # 용량에 맞지 않아서 물건을 넣을 수 없다.
                table[i + 1][capacity] = previous_items_value
    # 표에서 최상의 결과를 구한다.
    solution: List[Item] = []
    capacity = max_capacity
    for i in range(len(items), 0, -1):  # 거꾸로 반복한다.
        # 배낭에 이 물건이 있는가?
        if table[i - 1][capacity] != table[i][capacity]:
            solution.append(items[i - 1])
            # 용량에서 물건 무게를 뺀다.
            capacity -= items[i - 1].weight
    return solution


if __name__ == "__main__":
    items: List[Item] = [Item("TV", 50, 500),
                         Item("촛대", 2, 300),
                         Item("오디오", 35, 400),
                         Item("노트북", 3, 1000),
                         Item("식량", 15, 50),
                         Item("옷", 20, 800),
                         Item("보석", 1, 4000),
                         Item("책", 100, 300),
                         Item("프린터", 18, 30),
                         Item("냉장고", 200, 700),
                         Item("그림", 10, 1000)]
    print(knapsack(items, 75))
