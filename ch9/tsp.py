# tsp.py
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
from typing import Dict, List, Iterable, Tuple
from itertools import permutations

vt_distances: Dict[str, Dict[str, int]] = {
    "러틀랜드":
        {"벌링턴": 67,
         "화이트 리버 정션": 46,
         "베닝턴": 55,
         "브래틀보로": 75},
    "벌링턴":
        {"러틀랜드": 67,
         "화이트 리버 정션": 91,
         "베닝턴": 122,
         "브래틀보로": 153},
    "화이트 리버 정션":
        {"러틀랜드": 46,
         "벌링턴": 91,
         "베닝턴": 98,
         "브래틀보로": 65},
    "베닝턴":
        {"러틀랜드": 55,
         "벌링턴": 122,
         "화이트 리버 정션": 98,
         "브래틀보로": 40},
    "브래틀보로":
        {"러틀랜드": 75,
         "벌링턴": 153,
         "화이트 리버 정션": 65,
         "베닝턴": 40}
}

vt_cities: Iterable[str] = vt_distances.keys()
city_permutations: Iterable[Tuple[str, ...]] = permutations(vt_cities)
tsp_paths: List[Tuple[str, ...]] = [c + (c[0],) for c in city_permutations]

if __name__ == "__main__":
    best_path: Tuple[str, ...]
    min_distance: int = 99999999999  # 높은 숫자로 설정한다.
    for path in tsp_paths:
        distance: int = 0
        last: str = path[0]
        for next in path[1:]:
            distance += vt_distances[last][next]
            last = next
        if distance < min_distance:
            min_distance = distance
            best_path = path
    print(f"최단 경로는 {best_path} 이고, {min_distance} 마일입니다.")
