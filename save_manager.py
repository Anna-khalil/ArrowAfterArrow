"""
一箭又一箭 - 存档管理
使用 JSON 文件保存游戏进度、最佳成绩和星级。
"""
import json
import os
from constants import SAVE_DIR, SAVE_FILE


class SaveManager:
    """存档读写工具类"""

    @staticmethod
    def _ensure_dir():
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)

    @staticmethod
    def load():
        """读取存档，不存在则返回默认数据"""
        SaveManager._ensure_dir()
        default = {
            "unlocked_level": 1,   # 已解锁的最大关卡 id
            "current_level": 0,    # 当前关卡索引
            "best_scores": {},     # {level_id: 最高分}
            "best_times": {},      # {level_id: 最短用时}
            "stars": {},           # {level_id: 最高星级}
        }
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                default.update(data)
            except (json.JSONDecodeError, IOError):
                pass
        return default

    @staticmethod
    def save(data):
        """写入存档"""
        SaveManager._ensure_dir()
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    @staticmethod
    def update_level_result(level_id, score, time_val, stars):
        """通关后更新成绩并解锁下一关"""
        data = SaveManager.load()
        lid = str(level_id)

        # 更新最高分
        if lid not in data["best_scores"] or score > data["best_scores"][lid]:
            data["best_scores"][lid] = score
        # 更新最短用时
        if lid not in data["best_times"] or time_val < data["best_times"][lid]:
            data["best_times"][lid] = round(time_val, 1)
        # 更新最高星级
        if lid not in data["stars"] or stars > data["stars"][lid]:
            data["stars"][lid] = stars

        # 解锁下一关
        next_level = level_id + 1
        if next_level > data["unlocked_level"]:
            data["unlocked_level"] = next_level

        # 记录当前关卡
        data["current_level"] = level_id - 1

        SaveManager.save(data)
        return data
