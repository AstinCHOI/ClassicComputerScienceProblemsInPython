# dijkstra.py
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
from __future__ import annotations
from typing import TypeVar, List, Optional, Tuple, Dict
from dataclasses import dataclass
from mst import WeightedPath, print_weighted_path
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue

V = TypeVar('V')  # 그래프 정점(vertice) 타입


@dataclass
class DijkstraNode:
    vertex: int
    distance: float

    def __lt__(self, other: DijkstraNode) -> bool:
        return self.distance < other.distance

    def __eq__(self, other: DijkstraNode) -> bool:
        return self.distance == other.distance


def dijkstra(wg: WeightedGraph[V], root: V) -> Tuple[List[Optional[float]], Dict[int, WeightedEdge]]:
    first: int = wg.index_of(root)  # 시작 인덱스를 찾는다.
    # 처음에는 거리(distances)를 알 수 없다.
    distances: List[Optional[float]] = [None] * wg.vertex_count
    distances[first] = 0  # 루트(root)에서 루트 자신의 거리는 0이다.
    path_dict: Dict[int, WeightedEdge] = {}  # 정점에 대한 경로
    pq: PriorityQueue[DijkstraNode] = PriorityQueue()
    pq.push(DijkstraNode(first, 0))

    while not pq.empty:
        u: int = pq.pop().vertex  # 다음 가까운 정점을 탐색한다.
        dist_u: float = distances[u]  # 이 정점에 대한 거리를 이미 알고 있다.
        # 이 정점에서 모든 에지 및 정점을 살펴본다.
        for we in wg.edges_for_index(u):
            # 이 정점에 대한 이전 거리
            dist_v: float = distances[we.v]
            # 이전 거리가 없거나 혹은 새 최단 경로가 존재한다면,
            if dist_v is None or dist_v > we.weight + dist_u:
                # 정점의 거리를 갱신한다.
                distances[we.v] = we.weight + dist_u
                # 정점의 최단 경로의 에지를 갱신한다.
                path_dict[we.v] = we
                # 해당 정점을 나중에 곧 탐색한다.
                pq.push(DijkstraNode(we.v, we.weight + dist_u))

    return distances, path_dict


# 다익스트라 알고리즘 결과를 더 쉽게 접근하게 하는 헬퍼 함수
def distance_array_to_vertex_dict(wg: WeightedGraph[V], distances: List[Optional[float]]) -> Dict[V, Optional[float]]:
    distance_dict: Dict[V, Optional[float]] = {}
    for i in range(len(distances)):
        distance_dict[wg.vertex_at(i)] = distances[i]
    return distance_dict


# 에지의 딕셔너리 인자를 취해 각 노드에 접근하여,
# 정점 start 에서 end 까지가는 에지 리스트를 반환한다.
def path_dict_to_path(start: int, end: int, path_dict: Dict[int, WeightedEdge]) -> WeightedPath:
    if len(path_dict) == 0:
        return []
    edge_path: WeightedPath = []
    e: WeightedEdge = path_dict[end]
    edge_path.append(e)
    while e.u != start:
        e = path_dict[e.u]
        edge_path.append(e)
    return list(reversed(edge_path))


if __name__ == "__main__":
    city_graph2: WeightedGraph[str] = WeightedGraph(
        ["시애틀", "샌프란시스코", "로스앤젤레스", "리버사이드", "피닉스", "시카고", "보스턴", "뉴욕", "애틀랜타", "마이애미", "댈러스", "휴스턴", "디트로이트", "필라델피아", "워싱턴"])

    city_graph2.add_edge_by_vertices("시애틀", "시카고", 1737)
    city_graph2.add_edge_by_vertices("시애틀", "샌프란시스코", 678)
    city_graph2.add_edge_by_vertices("샌프란시스코", "리버사이드", 386)
    city_graph2.add_edge_by_vertices("샌프란시스코", "로스앤젤레스", 348)
    city_graph2.add_edge_by_vertices("로스앤젤레스", "리버사이드", 50)
    city_graph2.add_edge_by_vertices("로스앤젤레스", "피닉스", 357)
    city_graph2.add_edge_by_vertices("리버사이드", "피닉스", 307)
    city_graph2.add_edge_by_vertices("리버사이드", "시카고", 1704)
    city_graph2.add_edge_by_vertices("피닉스", "댈러스", 887)
    city_graph2.add_edge_by_vertices("피닉스", "휴스턴", 1015)
    city_graph2.add_edge_by_vertices("댈러스", "시카고", 805)
    city_graph2.add_edge_by_vertices("댈러스", "애틀랜타", 721)
    city_graph2.add_edge_by_vertices("댈러스", "휴스턴", 225)
    city_graph2.add_edge_by_vertices("휴스턴", "애틀랜타", 702)
    city_graph2.add_edge_by_vertices("휴스턴", "마이애미", 968)
    city_graph2.add_edge_by_vertices("애틀랜타", "시카고", 588)
    city_graph2.add_edge_by_vertices("애틀랜타", "워싱턴", 543)
    city_graph2.add_edge_by_vertices("애틀랜타", "마이애미", 604)
    city_graph2.add_edge_by_vertices("마이애미", "워싱턴", 923)
    city_graph2.add_edge_by_vertices("시카고", "디트로이트", 238)
    city_graph2.add_edge_by_vertices("디트로이트", "보스턴", 613)
    city_graph2.add_edge_by_vertices("디트로이트", "워싱턴", 396)
    city_graph2.add_edge_by_vertices("디트로이트", "뉴욕", 482)
    city_graph2.add_edge_by_vertices("보스턴", "뉴욕", 190)
    city_graph2.add_edge_by_vertices("뉴욕", "필라델피아", 81)
    city_graph2.add_edge_by_vertices("필라델피아", "워싱턴", 123)

    distances, path_dict = dijkstra(city_graph2, "로스앤젤레스")
    name_distance: Dict[str, Optional[int]] = distance_array_to_vertex_dict(
        city_graph2, distances)
    print("로스앤젤레스에서의 거리:")
    for key, value in name_distance.items():
        print(f"{key} : {value}")
    print("")  # 공백 라인

    print("로스앤젤레스에서 보스턴까지의 최단 경로:")
    path: WeightedPath = path_dict_to_path(city_graph2.index_of(
        "로스앤젤레스"), city_graph2.index_of("보스턴"), path_dict)
    print_weighted_path(city_graph2, path)
