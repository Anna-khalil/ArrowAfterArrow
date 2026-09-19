"""
一箭又一箭 - 程序入口
Python + Pygame 实现的箭头消除休闲小游戏。
学号：102401402
"""
import pygame
from constants import WIDTH, HEIGHT, FPS
from game_state import GameState
from solver import Solver
from save_manager import SaveManager
from ui import StartScreen, LevelSelectScreen, GameScreen, ResultScreen


class GameApp:
    """游戏主应用，管理界面切换和全局状态"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("一箭又一箭 ArrowAfterArrow")
        self.clock = pygame.time.Clock()
        self.running = True

        # 全局状态
        self.game_state = GameState()
        self.solver = Solver()
        self.save_data = SaveManager.load()

        # 界面管理
        self.current_screen = None
        self.screens = {}
        self._init_screens()
        self.switch_screen("start")

    def _init_screens(self):
        self.screens["start"] = StartScreen(self)
        self.screens["level_select"] = LevelSelectScreen(self)
        self.screens["game"] = GameScreen(self)
        self.screens["result"] = ResultScreen(self)

    def switch_screen(self, name, **kwargs):
        """切换到指定界面"""
        self.current_screen = self.screens[name]
        self.current_screen.on_enter(**kwargs)

    def run(self):
        """主循环"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_screen.handle_event(event)

            # 更新
            self.current_screen.update(dt)

            # 绘制
            self.current_screen.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    app = GameApp()
    app.run()
