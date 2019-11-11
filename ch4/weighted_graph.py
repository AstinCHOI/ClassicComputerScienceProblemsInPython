# weighted_graph.py
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
from typing import TypeVar, Generic, List, Tuple
from graph import Graph
from weighted_edge import WeightedEdge

V = TypeVar('V')  # 그래프 정점(vertice) 타입


class WeightedGraph(Generic[V], Graph[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices
        self._edges: List[List[WeightedEdge]] = [[] for _ in vertices]

    def add_edge_by_indices(self, u: int, v: int, weight: float) -> None:
        edge: WeightedEdge = WeightedEdge(u, v, weight)
        self.add_edge(edge)  # 슈퍼 클래스 메서드 호출

    def add_edge_by_vertices(self, first: V, second: V, weight: float) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v, weight)

    def neighbors_for_index_with_weights(self, index: int) -> List[Tuple[V, float]]:
        distance_tuples: List[Tuple[V, float]] = []
        for edge in self.edges_for_index(index):
            distance_tuples.append((self.vertex_at(edge.v), edge.weight))
        return distance_tuples

    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index_with_weights(i)}\n"
        return desc


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

    print(city_graph2)
