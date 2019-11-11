# graph.py
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
from typing import TypeVar, Generic, List, Optional
from edge import Edge


V = TypeVar('V')  # 그래프 정점(vertice) 타입


class Graph(Generic[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices
        self._edges: List[List[Edge]] = [[] for _ in vertices]

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)  # 정점의 수

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))  # 에지의 수

    # 그래프에 정점을 추가하고 인덱스를 반환한다.
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])  # 에지에 빈 리스트를 추가한다.
        return self.vertex_count - 1  # 추가된 정점의 인덱스를 반환한다.

    # 무방향(undirected) 그래프이므로 항상 양방향으로 에지를 추가한다.
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())

    # # 정점 인덱스를 사용하여 에지를 추가한다(헬퍼 메서드).
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge: Edge = Edge(u, v)
        self.add_edge(edge)

    # 정점 인덱스를 참조하여 에지를 추가한다(헬퍼 메서드).
    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v)

    # 특정 인덱스에서 정점을 찾는다.
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    # 정점 인덱스를 찾는다.
    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    # 정점 인덱스에 연결된 이웃 정점을 찾는다.
    def neighbors_for_index(self, index: int) -> List[V]:
        return list(map(self.vertex_at, [e.v for e in self._edges[index]]))

    # 정점의 이웃 정점을 찾는다(헬퍼 메서드).
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    # 정점 인덱스에 연결된 모든 에지를 반환한다.
    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]

    # 정점의 해당 에지를 반환한다(헬퍼 메서드).
    def edges_for_vertex(self, vertex: V) -> List[Edge]:
        return self.edges_for_index(self.index_of(vertex))

    # 그래프를 예쁘게 출력한다(pretty-print).
    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc


if __name__ == "__main__":
    # 기본 그래프 구축 테스트
    city_graph: Graph[str] = Graph(["시애틀", "샌프란시스코", "로스앤젤레스", "리버사이드", "피닉스", "시카고",
                                    "보스턴", "뉴욕", "애틀랜타", "마이애미", "댈러스", "휴스턴", "디트로이트", "필라델피아", "워싱턴"])
    city_graph.add_edge_by_vertices("시애틀", "시카고")
    city_graph.add_edge_by_vertices("시애틀", "샌프란시스코")
    city_graph.add_edge_by_vertices("샌프란시스코", "리버사이드")
    city_graph.add_edge_by_vertices("샌프란시스코", "로스앤젤레스")
    city_graph.add_edge_by_vertices("로스앤젤레스", "리버사이드")
    city_graph.add_edge_by_vertices("로스앤젤레스", "피닉스")
    city_graph.add_edge_by_vertices("리버사이드", "피닉스")
    city_graph.add_edge_by_vertices("리버사이드", "시카고")
    city_graph.add_edge_by_vertices("피닉스", "댈러스")
    city_graph.add_edge_by_vertices("피닉스", "휴스턴")
    city_graph.add_edge_by_vertices("댈러스", "시카고")
    city_graph.add_edge_by_vertices("댈러스", "애틀랜타")
    city_graph.add_edge_by_vertices("댈러스", "휴스턴")
    city_graph.add_edge_by_vertices("휴스턴", "애틀랜타")
    city_graph.add_edge_by_vertices("휴스턴", "마이애미")
    city_graph.add_edge_by_vertices("애틀랜타", "시카고")
    city_graph.add_edge_by_vertices("애틀랜타", "워싱턴")
    city_graph.add_edge_by_vertices("애틀랜타", "마이애미")
    city_graph.add_edge_by_vertices("마이애미", "워싱턴")
    city_graph.add_edge_by_vertices("시카고", "디트로이트")
    city_graph.add_edge_by_vertices("디트로이트", "보스턴")
    city_graph.add_edge_by_vertices("디트로이트", "워싱턴")
    city_graph.add_edge_by_vertices("디트로이트", "뉴욕")
    city_graph.add_edge_by_vertices("보스턴", "뉴욕")
    city_graph.add_edge_by_vertices("뉴욕", "필라델피아")
    city_graph.add_edge_by_vertices("필라델피아", "워싱턴")
    print(city_graph)

    # city_graph 변수에 2장의 너비 우선 탐색을 재사용한다.
    import sys
    # 상위 디렉터리에 있는 2장 패키지에 접근한다.
    sys.path.insert(0, '..')
    from ch2.generic_search import bfs, Node, node_to_path

    bfs_result: Optional[Node[V]] = bfs(
        "보스턴", lambda x: x == "마이애미", city_graph.neighbors_for_vertex)
    if bfs_result is None:
        print("[너비 우선 탐색] 답을 찾을 수 없습니다.")
    else:
        path: List[V] = node_to_path(bfs_result)
        print("보스턴에서 마이애미 최단 경로:")
        print(path)
