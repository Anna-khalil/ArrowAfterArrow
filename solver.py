"""
一箭又一箭 - AI 求解器
使用 DFS 回溯 + 记忆化（memoization）求解关卡的通关步骤。
"""


class Solver:
    """AI 自动求解器"""

    def __init__(self):
        self.memo = {}

    def solve(self, board):
        """
        求解给定棋盘的通关步骤。
        返回步骤列表，每步为 (row, col, direction) 元组；无解返回 None。
        传入的 board 不会被修改。
        """
        self.memo = {}
        # 在克隆棋盘上求解，不影响原棋盘
        result = self._dfs(board.clone())
        return result

    def _dfs(self, board):
        """深度优先搜索回溯"""
        # 终止条件：棋盘无箭头 → 通关
        if not board.has_arrows():
            return []

        # 记忆化：相同棋盘状态直接返回缓存结果
        key = board.get_state_key()
        if key in self.memo:
            return self.memo[key]

        # 尝试所有当前可消除的箭头
        clear_arrows = board.get_clear_arrows()
        for arrow in clear_arrows:
            # 临时移除箭头
            board.remove_arrow(arrow)
            # 递归求解剩余棋盘
            result = self._dfs(board)
            # 恢复箭头（回溯，使用原对象而非新建）
            board.add_arrow(arrow.row, arrow.col, arrow.direction, arrow=arrow)

            if result is not None:
                solution = [(arrow.row, arrow.col, arrow.direction)] + result
                self.memo[key] = solution
                return solution

        # 所有尝试都失败 → 无解
        self.memo[key] = None
        return None
