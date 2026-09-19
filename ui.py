"""
一箭又一箭 - 界面模块
包含按钮组件和四个界面：开始界面、关卡选择、游戏界面、结果界面。
"""
import pygame
from constants import (
    WIDTH, HEIGHT, BG_COLOR, PANEL_COLOR, CELL_COLOR, GRID_COLOR,
    TEXT_COLOR, TEXT_DIM, BUTTON_COLOR, BUTTON_HOVER, BUTTON_DISABLED,
    ACCENT, DANGER, WARNING, CELL_SIZE, get_font,
)
from levels import LEVELS
from save_manager import SaveManager


# ========== 按钮组件 ==========

class Button:
    """通用文字按钮"""

    def __init__(self, x, y, w, h, text, callback,
                 color=BUTTON_COLOR, text_color=TEXT_COLOR, font_size=24):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.color = color
        self.text_color = text_color
        self.font = get_font(font_size)
        self.enabled = True
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.enabled and self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.enabled and self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

    def draw(self, surface):
        if not self.enabled:
            color = BUTTON_DISABLED
        elif self.hover:
            color = BUTTON_HOVER
        else:
            color = self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class LevelButton:
    """关卡选择按钮"""

    def __init__(self, x, y, w, h, level_id, name, stars, unlocked, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.level_id = level_id
        self.name = name
        self.stars = stars
        self.unlocked = unlocked
        self.callback = callback
        self.hover = False
        self.font_id = get_font(26)
        self.font_name = get_font(13)
        self.font_star = get_font(15)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.unlocked and self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.unlocked and self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

    def draw(self, surface):
        if not self.unlocked:
            color = BUTTON_DISABLED
        elif self.hover:
            color = BUTTON_HOVER
        else:
            color = BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        if self.unlocked:
            id_text = self.font_id.render(str(self.level_id), True, TEXT_COLOR)
            surface.blit(id_text, id_text.get_rect(center=(self.rect.centerx, self.rect.y + 24)))
            name_text = self.font_name.render(self.name, True, TEXT_DIM)
            surface.blit(name_text, name_text.get_rect(center=(self.rect.centerx, self.rect.y + 50)))
            for i in range(3):
                c = WARNING if i < self.stars else (70, 70, 90)
                s = self.font_star.render("★", True, c)
                surface.blit(s, (self.rect.x + 22 + i * 20, self.rect.y + 64))
        else:
            lock = self.font_id.render("锁", True, TEXT_DIM)
            surface.blit(lock, lock.get_rect(center=self.rect.center))


# ========== 界面基类 ==========

class Screen:
    def __init__(self, game):
        self.game = game

    def on_enter(self, **kwargs):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


# ========== 开始界面 ==========

class StartScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = []
        self._init_buttons()

    def _init_buttons(self):
        bw, bh = 240, 56
        gap = 18
        x = (WIDTH - bw) // 2
        y = 420
        self.btn_start = Button(x, y, bw, bh, "开始游戏", self.on_start, font_size=26)
        self.btn_level = Button(x, y + bh + gap, bw, bh, "关卡选择", self.on_level_select, font_size=26)
        self.btn_continue = Button(x, y + (bh + gap) * 2, bw, bh, "继续游戏", self.on_continue, font_size=26)
        self.buttons = [self.btn_start, self.btn_level, self.btn_continue]

    def on_enter(self):
        save = self.game.save_data
        self.btn_continue.enabled = save.get("unlocked_level", 1) > 1

    def on_start(self):
        self.game.game_state.load_level(0)
        self.game.switch_screen("game")

    def on_level_select(self):
        self.game.switch_screen("level_select")

    def on_continue(self):
        save = self.game.save_data
        idx = min(save.get("current_level", 0), len(LEVELS) - 1)
        self.game.game_state.load_level(idx)
        self.game.switch_screen("game")

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, surface):
        surface.fill(BG_COLOR)

        font_title = get_font(60)
        font_sub = get_font(24)
        font_small = get_font(18)

        title = font_title.render("一箭又一箭", True, TEXT_COLOR)
        surface.blit(title, title.get_rect(center=(WIDTH // 2, 200)))

        sub = font_sub.render("看清方向 · 找到出口", True, ACCENT)
        surface.blit(sub, sub.get_rect(center=(WIDTH // 2, 280)))

        for btn in self.buttons:
            btn.draw(surface)

        tips = [
            "点击箭头使其沿方向飞出棋盘",
            "前方有箭头阻挡则碰撞并扣除一次失误",
            "消除全部箭头即可通关",
        ]
        for i, tip in enumerate(tips):
            t = font_small.render(tip, True, TEXT_DIM)
            surface.blit(t, t.get_rect(center=(WIDTH // 2, 690 + i * 28)))

        ver = font_small.render("v1.0 | Python + Pygame | 学号 102401402", True, TEXT_DIM)
        surface.blit(ver, ver.get_rect(center=(WIDTH // 2, HEIGHT - 25)))


# ========== 关卡选择界面 ==========

class LevelSelectScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.level_buttons = []
        self.back_button = None
        self._init_buttons()

    def _init_buttons(self):
        self.level_buttons = []
        save = self.game.save_data
        unlocked = save.get("unlocked_level", 1)
        stars = save.get("stars", {})

        cols = 5
        bw, bh = 110, 90
        gap_x, gap_y = 18, 18
        total_w = cols * bw + (cols - 1) * gap_x
        start_x = (WIDTH - total_w) // 2
        start_y = 160

        for i, level in enumerate(LEVELS):
            r = i // cols
            c = i % cols
            x = start_x + c * (bw + gap_x)
            y = start_y + r * (bh + gap_y)
            lid = level["id"]
            is_unlocked = lid <= unlocked
            star_count = stars.get(str(lid), 0)
            btn = LevelButton(
                x, y, bw, bh, lid, level["name"], star_count, is_unlocked,
                lambda idx=i: self._select_level(idx),
            )
            self.level_buttons.append(btn)

        self.back_button = Button(30, HEIGHT - 70, 120, 44, "返回", self.on_back)

    def _select_level(self, index):
        self.game.game_state.load_level(index)
        self.game.switch_screen("game")

    def on_back(self):
        self.game.switch_screen("start")

    def on_enter(self):
        self._init_buttons()

    def handle_event(self, event):
        for btn in self.level_buttons:
            btn.handle_event(event)
        self.back_button.handle_event(event)

    def draw(self, surface):
        surface.fill(BG_COLOR)
        font_title = get_font(36)
        title = font_title.render("选择关卡", True, TEXT_COLOR)
        surface.blit(title, title.get_rect(center=(WIDTH // 2, 90)))

        for btn in self.level_buttons:
            btn.draw(surface)
        self.back_button.draw(surface)


# ========== 游戏界面 ==========

class GameScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = []
        self._init_buttons()
        self.auto_solving = False
        self.solve_steps = []
        self.solve_index = 0
        self.solve_timer = 0.0
        self.message = ""
        self.message_timer = 0.0

    def _init_buttons(self):
        bw, bh = 128, 44
        gap = 10
        total_w = bw * 5 + gap * 4
        start_x = (WIDTH - total_w) // 2
        y = HEIGHT - 68
        self.btn_restart = Button(start_x, y, bw, bh, "重新开始", self.on_restart, font_size=20)
        self.btn_undo = Button(start_x + (bw + gap), y, bw, bh, "撤销", self.on_undo, font_size=20)
        self.btn_hint = Button(start_x + (bw + gap) * 2, y, bw, bh, "提示", self.on_hint, font_size=20)
        self.btn_ai = Button(start_x + (bw + gap) * 3, y, bw, bh, "AI求解", self.on_ai_solve, font_size=20)
        self.btn_back = Button(start_x + (bw + gap) * 4, y, bw, bh, "返回", self.on_back, font_size=20)
        self.buttons = [self.btn_restart, self.btn_undo, self.btn_hint, self.btn_ai, self.btn_back]

    def on_enter(self, level_index=None):
        if level_index is not None:
            self.game.game_state.load_level(level_index)
        self.auto_solving = False
        self.solve_steps = []
        self.message = ""

    def on_restart(self):
        self.game.game_state.restart()
        self.auto_solving = False
        self.show_message("已重新开始")

    def on_undo(self):
        if self.auto_solving:
            return
        if self.game.game_state.undo():
            self.show_message("已撤销上一步")
        else:
            self.show_message("没有可撤销的操作")

    def on_hint(self):
        if self.auto_solving:
            return
        gs = self.game.game_state
        # 用求解器找通关路径的第一步（最优提示）
        solution = self.game.solver.solve(gs.board.clone())
        if solution:
            first = solution[0]
            for a in gs.board.arrows:
                if (a.row, a.col, a.direction) == first:
                    a.start_hint()
                    break
            self.show_message("提示：金色闪烁的箭头可消除")
        else:
            # 求解器无解时，退而求其次给任意可消除箭头
            clear = gs.board.get_clear_arrows()
            if clear:
                clear[0].start_hint()
                self.show_message("提示：金色闪烁的箭头可消除")
            else:
                self.show_message("当前关卡似乎无解")

    def on_ai_solve(self):
        gs = self.game.game_state
        if gs.status != "playing":
            return
        solution = self.game.solver.solve(gs.board.clone())
        if solution:
            self.solve_steps = solution
            self.solve_index = 0
            self.auto_solving = True
            self.solve_timer = 0.0
            self.show_message(f"AI 求解中，共 {len(solution)} 步")
        else:
            self.show_message("当前关卡无解")

    def on_back(self):
        self.auto_solving = False
        self.game.switch_screen("level_select")

    def show_message(self, msg):
        self.message = msg
        self.message_timer = 2.0

    def handle_event(self, event):
        for btn in self.buttons:
            if btn.handle_event(event):
                return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.auto_solving:
                return
            gs = self.game.game_state
            if gs.status != "playing":
                return
            # 像素坐标转网格坐标
            mx, my = event.pos
            bx, by = self._get_board_offset()
            col = int((mx - bx) // CELL_SIZE)
            row = int((my - by) // CELL_SIZE)
            arrow = gs.board.get_arrow_at(row, col)
            if arrow:
                gs.click_arrow(arrow)

    def _get_board_offset(self):
        """计算棋盘左上角像素坐标，使其在 HUD 下方居中"""
        gs = self.game.game_state
        level = gs.get_current_level()
        board_w = level["cols"] * CELL_SIZE
        board_h = level["rows"] * CELL_SIZE
        bx = (WIDTH - board_w) // 2
        by = 130 + (580 - board_h) // 2
        return bx, by

    def update(self, dt):
        gs = self.game.game_state
        gs.update_animation(dt)

        # AI 自动求解演示：每 0.55 秒执行一步
        if self.auto_solving and gs.status == "playing":
            self.solve_timer += dt
            if self.solve_timer >= 0.55:
                self.solve_timer = 0.0
                if self.solve_index < len(self.solve_steps):
                    step = self.solve_steps[self.solve_index]
                    for a in gs.board.arrows:
                        if (a.row, a.col, a.direction) == step:
                            gs.click_arrow(a)
                            break
                    self.solve_index += 1
                else:
                    self.auto_solving = False

        # 通关 → 保存成绩 → 切换结果界面
        if gs.status == "won":
            level = gs.get_current_level()
            SaveManager.update_level_result(
                level["id"], gs.level_score, gs.elapsed_time, gs.get_stars()
            )
            self.game.save_data = SaveManager.load()
            self.auto_solving = False
            self.game.switch_screen("result", result_type="won")
        elif gs.status == "lost":
            self.auto_solving = False
            self.game.switch_screen("result", result_type="lost")

        if self.message_timer > 0:
            self.message_timer -= dt

    def draw(self, surface):
        surface.fill(BG_COLOR)
        gs = self.game.game_state
        level = gs.get_current_level()

        font_large = get_font(28)
        font_med = get_font(22)
        font_small = get_font(18)
        font_heart = get_font(24)

        # HUD — 关卡名
        title = font_large.render(f"第 {level['id']} 关 · {level['name']}", True, TEXT_COLOR)
        surface.blit(title, (30, 22))

        # HUD — 剩余箭头
        arrow_count = len(gs.board.arrows)
        ac_text = font_med.render(f"剩余箭头: {arrow_count}", True, TEXT_COLOR)
        surface.blit(ac_text, (30, 62))

        # HUD — 用时
        time_text = font_med.render(f"用时: {gs.elapsed_time:.1f}s", True, TEXT_DIM)
        surface.blit(time_text, (250, 62))

        # HUD — 失误次数（心形）
        label = font_med.render("失误:", True, TEXT_COLOR)
        surface.blit(label, (WIDTH - 30 - level["max_mistakes"] * 28 - 65, 60))
        for i in range(level["max_mistakes"]):
            color = DANGER if i < gs.mistakes_left else (70, 70, 90)
            h = font_heart.render("♥", True, color)
            surface.blit(h, (WIDTH - 30 - (i + 1) * 28, 58))

        # 棋盘背景面板
        bx, by = self._get_board_offset()
        board_w = level["cols"] * CELL_SIZE
        board_h = level["rows"] * CELL_SIZE
        pygame.draw.rect(surface, PANEL_COLOR, (bx - 12, by - 12, board_w + 24, board_h + 24), border_radius=14)

        # 网格
        for r in range(level["rows"]):
            for c in range(level["cols"]):
                cell_rect = pygame.Rect(bx + c * CELL_SIZE, by + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, CELL_COLOR, cell_rect, border_radius=4)
                pygame.draw.rect(surface, GRID_COLOR, cell_rect, 1, border_radius=4)

        # 箭头
        for arrow in gs.board.arrows:
            arrow.draw(surface, bx, by)

        # 底部按钮
        for btn in self.buttons:
            btn.draw(surface)

        # 消息提示
        if self.message_timer > 0:
            alpha = min(255, int(self.message_timer * 128))
            msg_surf = font_small.render(self.message, True, WARNING)
            msg_rect = msg_surf.get_rect(center=(WIDTH // 2, HEIGHT - 110))
            surface.blit(msg_surf, msg_rect)


# ========== 结果界面 ==========

class ResultScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.result_type = "won"
        self.buttons = []

    def on_enter(self, result_type="won"):
        self.result_type = result_type
        self._init_buttons()

    def _init_buttons(self):
        self.buttons = []
        gs = self.game.game_state
        bw, bh = 160, 50
        gap = 20
        y = HEIGHT - 160

        if self.result_type == "won":
            has_next = gs.has_next_level()
            if has_next:
                total_w = bw * 3 + gap * 2
                sx = (WIDTH - total_w) // 2
                self.buttons.append(Button(sx, y, bw, bh, "下一关", self.on_next, font_size=22))
                self.buttons.append(Button(sx + bw + gap, y, bw, bh, "重玩", self.on_replay, font_size=22))
                self.buttons.append(Button(sx + (bw + gap) * 2, y, bw, bh, "返回主页", self.on_home, font_size=22))
            else:
                total_w = bw * 2 + gap
                sx = (WIDTH - total_w) // 2
                self.buttons.append(Button(sx, y, bw, bh, "重玩", self.on_replay, font_size=22))
                self.buttons.append(Button(sx + bw + gap, y, bw, bh, "返回主页", self.on_home, font_size=22))
        else:
            total_w = bw * 2 + gap
            sx = (WIDTH - total_w) // 2
            self.buttons.append(Button(sx, y, bw, bh, "重新开始", self.on_replay, font_size=22))
            self.buttons.append(Button(sx + bw + gap, y, bw, bh, "返回主页", self.on_home, font_size=22))

    def on_next(self):
        self.game.game_state.next_level()
        self.game.switch_screen("game")

    def on_replay(self):
        self.game.game_state.restart()
        self.game.switch_screen("game")

    def on_home(self):
        self.game.switch_screen("start")

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, surface):
        surface.fill(BG_COLOR)
        gs = self.game.game_state
        level = gs.get_current_level()

        font_title = get_font(48)
        font_med = get_font(26)
        font_star = get_font(42)
        font_small = get_font(20)

        if self.result_type == "won":
            is_final = not gs.has_next_level()
            title_text = "全部通关！" if is_final else "通关！"
            color = ACCENT
        else:
            title_text = "失败"
            color = DANGER

        title = font_title.render(title_text, True, color)
        surface.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

        if self.result_type == "won":
            # 星级
            stars = gs.get_stars()
            for i in range(3):
                c = WARNING if i < stars else (70, 70, 90)
                s = font_star.render("★", True, c)
                surface.blit(s, (WIDTH // 2 - 63 + i * 55, 250))

            # 成绩信息
            info = [
                f"关卡：第 {level['id']} 关 · {level['name']}",
                f"得分：{gs.level_score}",
                f"用时：{gs.elapsed_time:.1f} 秒",
                f"剩余失误：{gs.mistakes_left}",
            ]
            for i, line in enumerate(info):
                t = font_med.render(line, True, TEXT_COLOR)
                surface.blit(t, t.get_rect(center=(WIDTH // 2, 350 + i * 42)))
        else:
            t = font_med.render("失误次数已耗尽，再试一次吧！", True, TEXT_DIM)
            surface.blit(t, t.get_rect(center=(WIDTH // 2, 320)))

        for btn in self.buttons:
            btn.draw(surface)

        tip = font_small.render("提示：可使用「撤销」回退错误操作，或「AI求解」查看通关步骤", True, TEXT_DIM)
        surface.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT - 80)))
