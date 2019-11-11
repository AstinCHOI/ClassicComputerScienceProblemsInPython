# map_coloring.py
# From Classic Computer Science Problems in Python Chapter 3
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
from csp import Constraint, CSP
from typing import Dict, List, Optional


class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # 두 지역 중 하나가 색상이 할당되지 않았다면, 색상 충돌은 발생하지 않는다.
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # place1과 place2에 할당된 색상이 다른지 확인한다.
        return assignment[self.place1] != assignment[self.place2]


if __name__ == "__main__":
    variables: List[str] = ["웨스턴 오스트레일리아 주", "노던 준주", "사우스 오스트레일리아 주",
                            "퀸즐랜드 주", "뉴사우스웨일스 주", "빅토리아 주", "태즈메이니아 주"]
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ["빨강", "초록", "파랑"]
    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(MapColoringConstraint(
        "웨스턴 오스트레일리아 주", "노던 준주"))
    csp.add_constraint(MapColoringConstraint(
        "웨스턴 오스트레일리아 주", "사우스 오스트레일리아 주"))
    csp.add_constraint(MapColoringConstraint(
        "사우스 오스트레일리아 주", "노던 준주"))
    csp.add_constraint(MapColoringConstraint(
        "퀸즐랜드 주", "노던 준주"))
    csp.add_constraint(MapColoringConstraint("퀸즐랜드 주", "사우스 오스트레일리아 주"))
    csp.add_constraint(MapColoringConstraint("퀸즐랜드 주", "뉴사우스웨일스 주"))
    csp.add_constraint(MapColoringConstraint(
        "뉴사우스웨일스 주", "사우스 오스트레일리아 주"))
    csp.add_constraint(MapColoringConstraint("빅토리아 주", "사우스 오스트레일리아 주"))
    csp.add_constraint(MapColoringConstraint("빅토리아 주", "뉴사우스웨일스 주"))
    csp.add_constraint(MapColoringConstraint("빅토리아 주", "태즈메이니아 주"))
    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print("답이 없습니다!")
    else:
        print(solution)
