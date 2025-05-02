import pygame
import time
import numpy as np
from settings import Game

pygame.init()

game = Game()
FONT = pygame.font.SysFont("JetBrains Mono", 40)
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class PuzzleGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Tạo một surface, đóng vai trò là màn hình con để vẽ lưới puzzle
        # Mọi hình ảnh puzzle sẽ được vẽ lên surface này trước, sau đó mới hiển thị lên giao diện chính
        self.surface = pygame.Surface((self.width, self.height))
        self.current_state = None
        self.prev_state = None
        self.animation_progress = 1.0
        # Danh sách lưu vị trí của 2 ô bị hoán đổi khi có sự thay đổi trạng thái.
        # Thông tin này sẽ được dùng để xử lý hoạt ảnh (ví dụ: di chuyển ô từ vị trí cũ đến vị trí mới).
        self.swapped_positions = []

    def find_swapped_tiles(self, state1, state2):
        swapped = [i for i in range(len(state1)) if state1[i] != state2[i]]
        return swapped

    def ease_in_out_cubic(self, t):
        t *= 2
        if t < 1:
            return 0.5 * t * t * t
        t -= 2
        return 0.5 * (t * t * t + 2)

    def get_direction(self, pos1, pos2):
        row1, col1 = pos1 // 3, pos1 % 3
        row2, col2 = pos2 // 3, pos2 % 3
        if row1 > row2:
            return "up"
        elif row1 < row2:
            return "down"
        elif col1 > col2:
            return "left"
        elif col1 < col2:
            return "right"
        return None

    def draw(self, state, prev_state=None, animation_progress=1.0):
        self.current_state = state
        self.prev_state = prev_state
        self.animation_progress = animation_progress
        self.swapped_positions = self.find_swapped_tiles(prev_state, state) if prev_state else []
        tile_positions, tile_scales, tile_alphas = {}, {}, {}

        for i in range(game.GRID_SIZE):
            for j in range(game.GRID_SIZE):
                tile = state[i * 3 + j]
                tile_positions[i * 3 + j] = (game.GRID_X + j * game.TILE_SIZE, game.GRID_Y + i * game.TILE_SIZE)
                tile_scales[i * 3 + j] = 1.0
                tile_alphas[i * 3 + j] = 255

        if prev_state and animation_progress < 1.0 and self.swapped_positions:
            pos1, pos2 = self.swapped_positions
            direction = self.get_direction(pos1, pos2)
            row1, col1 = pos1 // 3, pos1 % 3
            row2, col2 = pos2 // 3, pos2 % 3
            start_x1, start_y1 = game.GRID_X + col2 * game.TILE_SIZE, game.GRID_Y + row2 * game.TILE_SIZE
            end_x1, end_y1 = game.GRID_X + col1 * game.TILE_SIZE, game.GRID_Y + row1 * game.TILE_SIZE
            start_x2, start_y2 = game.GRID_X + col1 * game.TILE_SIZE, game.GRID_Y + row1 * game.TILE_SIZE
            end_x2, end_y2 = game.GRID_X + col2 * game.TILE_SIZE, game.GRID_Y + row2 * game.TILE_SIZE

            eased_progress = self.ease_in_out_cubic(animation_progress)
            scale = 1.0 + 0.2 * (1 - abs(2 * eased_progress - 1))
            alpha = 255 * (1 - 0.3 * (1 - abs(2 * eased_progress - 1)))

            if direction in ["up", "down"]:
                tile_positions[pos1] = (start_x1, start_y1 + (end_y1 - start_y1) * eased_progress)
                tile_positions[pos2] = (start_x2, start_y2 + (end_y2 - start_y2) * eased_progress)
            elif direction in ["left", "right"]:
                tile_positions[pos1] = (start_x1 + (end_x1 - start_x1) * eased_progress, start_y1)
                tile_positions[pos2] = (start_x2 + (end_x2 - start_x2) * eased_progress, start_y2)

            tile_scales[pos1] = scale
            tile_scales[pos2] = scale
            tile_alphas[pos1] = alpha
            tile_alphas[pos2] = alpha

        self.surface.fill((245, 245, 245))  # Light gray background

        for i in range(game.GRID_SIZE):
            for j in range(game.GRID_SIZE):
                tile = state[i * 3 + j]
                if tile != 0:
                    pos_idx = i * 3 + j
                    x, y = tile_positions[pos_idx]
                    scale = tile_scales[pos_idx]
                    alpha = tile_alphas[pos_idx]
                    is_correct = (tile == GOAL_STATE[pos_idx])
                    color = (200, 255, 200) if is_correct else (255, 100, 100) if pos_idx in self.swapped_positions else (180, 180, 180)

                    if pos_idx in self.swapped_positions and animation_progress < 1.0:
                        shadow_surface = pygame.Surface((game.TILE_SIZE, game.TILE_SIZE), pygame.SRCALPHA)
                        shadow_surface.fill((0, 0, 0, 50))
                        shadow_rect = shadow_surface.get_rect(center=(x + game.TILE_SIZE / 2 + 5, y + game.TILE_SIZE / 2 + 5))
                        self.surface.blit(shadow_surface, shadow_rect)

                    tile_surface = pygame.Surface((game.TILE_SIZE - 2, game.TILE_SIZE - 2), pygame.SRCALPHA)
                    pygame.draw.rect(tile_surface, color, (0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2), border_radius=5)
                    tile_surface.set_alpha(int(alpha))
                    scaled_size = (int((game.TILE_SIZE - 2) * scale), int((game.TILE_SIZE - 2) * scale))
                    scaled_tile = pygame.transform.scale(tile_surface, scaled_size)
                    tile_rect = scaled_tile.get_rect(center=(x + game.TILE_SIZE / 2, y + game.TILE_SIZE / 2))
                    self.surface.blit(scaled_tile, tile_rect)

                    text = FONT.render(str(tile), True, (50, 50, 50))
                    text_rect = text.get_rect(center=(x + game.TILE_SIZE / 2, y + game.TILE_SIZE / 2))
                    self.surface.blit(text, text_rect)

    def get_surface(self):
        return self.surface
