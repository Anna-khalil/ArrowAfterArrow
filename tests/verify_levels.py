"""验证所有关卡可解性的临时脚本"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from board import Board
from levels import LEVELS
from solver import Solver

solver = Solver()
all_ok = True

for level in LEVELS:
    board = Board(level["rows"], level["cols"])
    for (r, c, d) in level["arrows"]:
        board.add_arrow(r, c, d)

    solution = solver.solve(board)
    if solution:
        print(f"[OK] 第{level['id']}关 {level['name']}: {len(level['arrows'])}个箭头, {len(solution)}步可解")
    else:
        print(f"[FAIL] 第{level['id']}关 {level['name']}: 无解!")
        all_ok = False

print()
print("全部关卡可解!" if all_ok else "存在不可解关卡，需要调整!")
