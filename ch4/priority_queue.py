# priority_queue.py
# From Classic Computer Science Problems in Python Chapter 4
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
from typing import TypeVar, Generic, List
from heapq import heappush, heappop


T = TypeVar('T')


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # 컨테이너가 비었다면 false가 아니다(=true)

    def push(self, item: T) -> None:
        heappush(self._container, item)  # 우선순위 push

    def pop(self) -> T:
        return heappop(self._container)  # 우선순위 pop

    def __repr__(self) -> str:
        return repr(self._container)
