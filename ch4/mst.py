# mst.py
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
from typing import TypeVar, List, Optional
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue

V = TypeVar('V')  # 그래프 정점(vertice) 타입
WeightedPath = List[WeightedEdge]  # 경로 타입 앨리어스


def total_weight(wp: WeightedPath) -> float:
    return sum([e.weight for e in wp])


def mst(wg: WeightedGraph[V], start: int = 0) -> Optional[WeightedPath]:
    if start > (wg.vertex_count - 1) or start < 0:
        return None
    result: WeightedPath = []  # 최소 신장 트리 결과
    pq: PriorityQueue[WeightedEdge] = PriorityQueue()
    visited: [bool] = [False] * wg.vertex_count  # 방문한 곳

    def visit(index: int):
        visited[index] = True  # 방문한 곳을 표시한다.
        for edge in wg.edges_for_index(index):
            # 해당 정점의 모든 에지를 우선 순위 큐(pq)에 추가한다.
            if not visited[edge.v]:
                pq.push(edge)

    visit(start)  # 첫 번째 정점에서 모든게 시작된다.

    while not pq.empty:  # 우선 순위 큐에 에지가 남아있을 때까지 계속 반복한다.
        edge = pq.pop()
        if visited[edge.v]:
            continue  # 방문한 곳이면 넘어간다.
        result.append(edge)  # 최소 가중치의 에지를 결과에 추가한다.
        visit(edge.v)  # 연결된 에지를 방문한다.

    return result


def print_weighted_path(wg: WeightedGraph, wp: WeightedPath) -> None:
    for edge in wp:
        print(f"{wg.vertex_at(edge.u)} {edge.weight}> {wg.vertex_at(edge.v)}")
    print(f"가중치 총합: {total_weight(wp)}")


if __name__ == "__main__":
    city_graph2: WeightedGraph[str] = WeightedGraph(["시애틀", "샌프란시스코", "로스앤젤레스", "리버사이드", "피닉스", "시카고",
                                                     "보스턴", "뉴욕", "애틀랜타", "마이애미", "댈러스", "휴스턴", "디트로이트", "필라델피아", "워싱턴"])

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

    result: Optional[WeightedPath] = mst(city_graph2)
    if result is None:
        print("[최소 신장 트리] 답을 찾을 수 없습니다.")
    else:
        print_weighted_path(city_graph2, result)
