"""
一箭又一箭 - 棋盘与路径检测
核心逻辑：判断箭头前进方向上是否存在其他箭头阻挡。
"""
import copy
from arrow import Arrow
from constants import DIRECTIONS


class Board:
    """游戏棋盘，管理网格和箭头"""

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # grid[r][c] 存储 Arrow 对象或 None
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.arrows = []

    def add_arrow(self, row, col, direction, arrow=None):
        """在指定位置添加箭头，可传入已有 arrow 对象（用于求解器回溯）"""
        if arrow is None:
            arrow = Arrow(row, col, direction)
        self.grid[row][col] = arrow
        self.arrows.append(arrow)
        return arrow

    def remove_arrow(self, arrow):
        """从棋盘移除箭头，按位置清空 grid 并从列表移除"""
        if 0 <= arrow.row < self.rows and 0 <= arrow.col < self.cols:
            self.grid[arrow.row][arrow.col] = None
        if arrow in self.arrows:
            self.arrows.remove(arrow)

    def get_arrow_at(self, row, col):
        """获取指定网格位置的箭头，越界返回 None"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def has_arrows(self):
        return len(self.arrows) > 0

    def is_path_clear(self, arrow):
        """
        核心算法：判断箭头前进方向上是否有其他箭头阻挡。
        从箭头的下一格开始，沿方向逐格扫描，直到棋盘边界。
        若遇到任意箭头则返回 False（有阻挡），否则返回 True（可飞出）。
        """
        r, c = arrow.row, arrow.col
        dx, dy = DIRECTIONS[arrow.direction]
        # 注意：dx 影响列(col)，dy 影响行(row)
        nr, nc = r + dy, c + dx
        while 0 <= nr < self.rows and 0 <= nc < self.cols:
            if self.grid[nr][nc] is not None:
                return False
            nr += dy
            nc += dx
        return True

    def get_clear_arrows(self):
        """返回所有当前可消除（前方无阻挡）的箭头列表"""
        return [a for a in self.arrows if self.is_path_clear(a)]

    def clone(self):
        """深拷贝棋盘，用于撤销和求解器"""
        return copy.deepcopy(self)

    def get_state_key(self):
        """
        序列化棋盘状态为不可变元组，用于求解器记忆化（memoization）。
        排序后保证相同布局生成相同 key。
        """
        states = sorted((a.row, a.col, a.direction) for a in self.arrows)
        return tuple(states)
