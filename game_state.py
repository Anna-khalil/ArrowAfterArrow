"""
一箭又一箭 - 游戏状态管理
负责当前关卡、失误次数、游戏状态流转、撤销历史栈。
"""
import copy
import pygame
from board import Board
from levels import LEVELS


class GameState:
    """游戏全局状态"""

    def __init__(self):
        self.current_level_index = 0
        self.board = None
        self.mistakes_left = 3
        self.status = "playing"  # playing / won / lost
        self.history = []         # 撤销栈，存棋盘快照和失误数
        self.start_time = 0
        self.elapsed_time = 0.0
        self.level_score = 0

    def load_level(self, index):
        """加载指定关卡"""
        if index < 0 or index >= len(LEVELS):
            return False
        self.current_level_index = index
        level = LEVELS[index]
        self.board = Board(level["rows"], level["cols"])
        for (r, c, d) in level["arrows"]:
            self.board.add_arrow(r, c, d)
        self.mistakes_left = level["max_mistakes"]
        self.status = "playing"
        self.history = []
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0.0
        self.level_score = 0
        return True

    def click_arrow(self, arrow):
        """
        处理点击箭头。
        返回 'fly'（可飞出）、'collide'（碰撞）、None（无效点击）
        """
        if self.status != "playing":
            return None
        if arrow.is_animating():
            return None

        if self.board.is_path_clear(arrow):
            # 保存历史快照（用于撤销）
            self.history.append(self._snapshot())
            arrow.start_fly()
            return "fly"
        else:
            arrow.start_shake()
            self.mistakes_left -= 1
            if self.mistakes_left <= 0:
                self.status = "lost"
            return "collide"

    def update_animation(self, dt):
        """更新所有箭头动画，处理飞出结束后的移除和通关判定"""
        to_remove = []
        for arrow in self.board.arrows:
            if arrow.update(dt):
                to_remove.append(arrow)

        for arrow in to_remove:
            self.board.remove_arrow(arrow)

        # 全部消除 → 通关
        if to_remove and not self.board.has_arrows() and self.status == "playing":
            self.status = "won"
            self._calculate_score()

        # 计时
        if self.status == "playing":
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0

    def _calculate_score(self):
        """通关得分 = 基础分 + 时间奖励 + 失误奖励"""
        base = 1000
        time_bonus = max(0, int(500 - self.elapsed_time * 15))
        mistake_bonus = self.mistakes_left * 150
        self.level_score = base + time_bonus + mistake_bonus

    def get_stars(self):
        """根据得分评定星级（1-3星）"""
        if self.level_score >= 1400:
            return 3
        elif self.level_score >= 1000:
            return 2
        return 1

    def _snapshot(self):
        """保存当前棋盘状态和失误数（深拷贝）"""
        return {
            "arrows": [a.get_state() for a in self.board.arrows],
            "mistakes": self.mistakes_left,
        }

    def undo(self):
        """撤销上一步成功消除操作，返回是否成功"""
        if not self.history:
            return False
        snap = self.history.pop()
        level = LEVELS[self.current_level_index]
        self.board = Board(level["rows"], level["cols"])
        for (r, c, d) in snap["arrows"]:
            self.board.add_arrow(r, c, d)
        self.mistakes_left = snap["mistakes"]
        self.status = "playing"
        return True

    def restart(self):
        """重新开始当前关卡"""
        self.load_level(self.current_level_index)

    def next_level(self):
        """进入下一关，返回是否成功（是否还有下一关）"""
        if self.current_level_index + 1 < len(LEVELS):
            self.load_level(self.current_level_index + 1)
            return True
        return False

    def get_current_level(self):
        return LEVELS[self.current_level_index]

    def has_next_level(self):
        return self.current_level_index + 1 < len(LEVELS)
