# generic_search.py
# From Classic Computer Science Problems in Python Chapter 2
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
from typing import TypeVar, Iterable, Sequence, Generic, List, Callable, Set, Deque, Dict, Any, Optional
from typing_extensions import Protocol
from heapq import heappush, heappop

T = TypeVar('T')


def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:  # 검색 공간(범위)이 있을 때 까지 수행
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # 컨테이너가 비었다면 false가 아니다(=true)

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()  # LIFO

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier는 아직 방문하지 않은 곳이다.
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # explored는 이미 방문한 곳이다.
    explored: Set[T] = {initial}

    # 방문할 곳이 더 있는지 탐색한다.
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # 목표 지점을 찾았다면 종료한다.
        if goal_test(current_state):
            return current_node
        # 방문하지 않은 다음 장소가 있는지 확인한다.
        for child in successors(current_state):
            if child in explored:  # 이미 방문한 자식 노드(장소)라면 건너뛴다.
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # 모든 곳을 방문했지만 결국 목표 지점을 찾지 못했다.


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # 노드 경로를 반전한다.
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container  # 컨테이너가 비었다면 false가 아니다(=true)

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()  # 선입선출(FIFO)

    def __repr__(self) -> str:
        return repr(self._container)


def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier는 아직 방문하지 않은 곳이다.
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored는 이미 방문한 곳이다.
    explored: Set[T] = {initial}

    # 방문할 곳이 더 있는지 탐색한다.
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # 목표 지점을 찾았다면 종료한다.
        if goal_test(current_state):
            return current_node
        # 방문하지 않은 다음 장소가 있는지 확인한다.
        for child in successors(current_state):
            if child in explored:  # 이미 방문한 자식 노드(장소)라면 건너뛴다.
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # 모든 곳을 방문했지만 결국 목표 지점을 찾지 못했다.


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


def astar(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]], heuristic: Callable[[T], float]) -> Optional[Node[T]]:
    # frontier는 아직 방문하지 않은 곳이다.
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored는 이미 방문한 곳이다.
    explored: Dict[T, float] = {initial: 0.0}

    # 방문할 곳이 더 있는지 탐색한다.
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # 목표 지점을 찾았다면 종료한다.
        if goal_test(current_state):
            return current_node
        # 방문하지 않은 다음 장소가 있는지 확인한다.
        for child in successors(current_state):
            # 현재 장소에서 갈 수 있는 다음 장소의 비용은 1이라 가정한다.
            new_cost: float = current_node.cost + 1

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node,
                                   new_cost, heuristic(child)))
    return None  # 모든 곳을 방문했지만 결국 목표 지점을 찾지 못했다.


if __name__ == "__main__":
    print(linear_contains([1, 5, 15, 15, 15, 15, 20], 5))  # True
    print(binary_contains(["a", "d", "e", "f", "z"], "f"))  # True
    print(binary_contains(
        ["john", "mark", "ronald", "sarah"], "sheila"))  # False
