# trivial_compression.py
# From Classic Computer Science Problems in Python Chapter 1
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


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1  # 1로 시작한다.
        for nucleotide in gene.upper():
            self.bit_string <<= 2  # 왼쪽으로 두 비트 이동
            if nucleotide == "A":  # 마지막 두 비트를 00으로 변경
                self.bit_string |= 0b00
            elif nucleotide == "C":  # 마지막 두 비트를 01으로 변경
                self.bit_string |= 0b01
            elif nucleotide == "G":  # 마지막 두 비트를 10으로 변경
                self.bit_string |= 0b10
            elif nucleotide == "T":  # 마지막 두 비트를 11으로 변경
                self.bit_string |= 0b11
            else:
                raise ValueError("유효하지 않은 뉴클레오타이드 입니다:{}".format(nucleotide))

    def decompress(self) -> str:
        gene: str = ""
        # 1로 시작해서 - 1이 있다.
        for i in range(0, self.bit_string.bit_length() - 1, 2):
            bits: int = self.bit_string >> i & 0b11  # 마지막 두 비트를 추출한다.
            if bits == 0b00:  # A
                gene += "A"
            elif bits == 0b01:  # C
                gene += "C"
            elif bits == 0b10:  # G
                gene += "G"
            elif bits == 0b11:  # T
                gene += "T"
            else:
                raise ValueError("Invalid bits:{}".format(bits))
        return gene[::-1]  # [::-1] 문자열을 뒤집는다.

    def __str__(self) -> str:  # 출력을 위한 문자열 표현
        return self.decompress()


if __name__ == "__main__":
    from sys import getsizeof
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print("원본: {} 바이트".format(getsizeof(original)))
    compressed: CompressedGene = CompressedGene(original)  # 압축
    print("압축: {} 바이트".format(getsizeof(compressed.bit_string)))
    print(compressed)  # 압축 해제
    print("원본 문자열과 압축 해제한 문자열은 같습니까? {}".format(
        original == compressed.decompress()))
