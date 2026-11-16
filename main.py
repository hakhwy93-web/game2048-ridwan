import pygame
import random
import sys
import array
import math

# تهيئة Pygame والصوت
pygame.init()
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1)
except:
    pass

# إعدادات الشاشة (تتكيف تلقائياً مع شاشة الهاتف)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Mobile - Ridwan Edition")

# الألوان (تصميم كلاسيكي أنيق)
BG_COLOR = (250, 248, 239)
GRID_COLOR = (187, 173, 160)
TEXT_DARK = (119, 110, 101)
TEXT_LIGHT = (249, 246, 242)
BTN_COLOR = (143, 122, 102)

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# حساب أبعاد لوحة اللعب لتناسب عرض الهاتف
BOARD_SIZE = int(WIDTH * 0.9)
TILE_MARGIN = int(BOARD_SIZE * 0.03)
TILE_SIZE = (BOARD_SIZE - TILE_MARGIN * 5) // 4
START_X = (WIDTH - BOARD_SIZE) // 2
START_Y = (HEIGHT - BOARD_SIZE) // 2 + int(HEIGHT * 0.05)

# الخطوط
font_title = pygame.font.SysFont("arial", int(WIDTH * 0.12), bold=True)
font_score = pygame.font.SysFont("arial", int(WIDTH * 0.045), bold=True)
font_tile = pygame.font.SysFont("arial", int(TILE_SIZE * 0.4), bold=True)
font_dev = pygame.font.SysFont("arial", int(WIDTH * 0.045), bold=True)
font_btn = pygame.font.SysFont("arial", int(WIDTH * 0.05), bold=True)

# دالة توليد صوت الحجر البرمجي
def generate_stone_sound():
    try:
        duration = 0.07  
        sample_rate = 22050
        num_samples = int(sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            val = int(14000 * (math.sin(2 * math.pi * 90 * t) + math.sin(2 * math.pi * 180 * t) * 0.5) * math.exp(-t * 30))
            samples.append(val)
        return pygame.mixer.Sound(buffer=array.array('h', samples))
    except:
        return None

stone_sound = generate_stone_sound()

class Game2048:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (4 - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(3):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        new_grid = []
        for row in self.grid:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final_row = self.compress(merged)
            if final_row != row:
                moved = True
            new_grid.append(final_row)
        self.grid = new_grid
        return moved

    def move_right(self):
        self.grid = [row[::-1] for row in self.grid]
        moved = self.move_left()
        self.grid = [row[::-1] for row in self.grid]
        return moved

    def move_up(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self.move_left()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved

    def move_down(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self.move_right()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved

    def check_game_over(self):
        for r in range(4):
            for c in range(4):
                if self.grid[r][c] == 0:
                    return False
                if c < 3 and self.grid[r][c] == self.grid[r][c + 1]:
                    return False
                if r < 3 and self.grid[r][c] == self.grid[r + 1][c]:
                    return False
        return True

    def draw(self):
        screen.fill(BG_COLOR)

        # رسم العنوان الرئيسي
        title_surf = font_title.render("2048", True, TEXT_DARK)
        screen.blit(title_surf, (START_X, START_Y - int(HEIGHT * 0.19)))

        # رفع اسمك Ridwan قليلاً للأعلى ليصبح غير ملتصق بحقل النقاط
        dev_surf = font_dev.render("By: Ridwan", True, (235, 67, 67))
        screen.blit(dev_surf, (START_X, START_Y - int(HEIGHT * 0.125)))

        # حقل النقاط المنظم (Score)
        score_surf = font_score.render(f"Score: {self.score}", True, TEXT_DARK)
        screen.blit(score_surf, (START_X, START_Y - int(HEIGHT * 0.08)))

        # زر إعادة اللعب (New Game)
        restart_rect = pygame.Rect(START_X + BOARD_SIZE - int(WIDTH * 0.32), START_Y - int(HEIGHT * 0.09), int(WIDTH * 0.32), int(HEIGHT * 0.055))
        pygame.draw.rect(screen, BTN_COLOR, restart_rect, border_radius=10)
        restart_text = font_score.render("New Game", True, TEXT_LIGHT)
        screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))

        # رسم خلفية الشبكة
        board_rect = pygame.Rect(START_X, START_Y, BOARD_SIZE, BOARD_SIZE)
        pygame.draw.rect(screen, GRID_COLOR, board_rect, border_radius=15)

        # رسم المربعات
        for r in range(4):
            for c in range(4):
                val = self.grid[r][c]
                color = TILE_COLORS.get(val, (60, 58, 50))
                x = START_X + TILE_MARGIN + c * (TILE_SIZE + TILE_MARGIN)
                y = START_Y + TILE_MARGIN + r * (TILE_SIZE + TILE_MARGIN)
                pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE), border_radius=10)

                if val != 0:
                    text_color = TEXT_DARK if val <= 4 else TEXT_LIGHT
                    text_surf = font_tile.render(str(val), True, text_color)
                    screen.blit(text_surf, text_surf.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2)))

        # رسالة انتهاء اللعبة
        if self.game_over:
            overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
            overlay.fill((238, 228, 218, 190))
            screen.blit(overlay, (START_X, START_Y))
            over_text = font_title.render("Game Over!", True, TEXT_DARK)
            screen.blit(over_text, over_text.get_rect(center=(START_X + BOARD_SIZE // 2, START_Y + BOARD_SIZE // 2)))

        pygame.display.flip()
        return restart_rect

def draw_start_screen():
    screen.fill(BG_COLOR)
    
    # عنوان اللعبة في الواجهة
    title_surf = font_title.render("2048 GAME", True, TEXT_DARK)
    screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 40)))

    # اسمك بالانكليزي في الواجهة
    dev_surf = font_dev.render("Developer: Ridwan", True, (235, 67, 67))
    screen.blit(dev_surf, dev_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 30)))

    # زر بدء اللعبة
    start_btn = pygame.Rect(WIDTH // 2 - int(WIDTH * 0.35), HEIGHT // 2 + 40, int(WIDTH * 0.7), int(HEIGHT * 0.08))
    pygame.draw.rect(screen, BTN_COLOR, start_btn, border_radius=12)
    start_text = font_btn.render("START GAME", True, TEXT_LIGHT)
    screen.blit(start_text, start_text.get_rect(center=start_btn.center))

    pygame.display.flip()
    return start_btn

def main():
    game_state = "START"
    game = None
    touch_start = None
    clock = pygame.time.Clock()

    while True:
        if game_state == "START":
            start_btn = draw_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_btn.collidepoint(event.pos):
                        if stone_sound:
                            stone_sound.play()
                        game = Game2048()
                        game_state = "PLAYING"

        elif game_state == "PLAYING":
            restart_btn = game.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    touch_start = event.pos
                    if restart_btn.collidepoint(event.pos):
                        if stone_sound:
                            stone_sound.play()
                        game = Game2048()

                elif event.type == pygame.MOUSEBUTTONUP and touch_start:
                    touch_end = event.pos
                    dx = touch_end[0] - touch_start[0]
                    dy = touch_end[1] - touch_start[1]
                    touch_start = None

                    if not game.game_over and (abs(dx) > 40 or abs(dy) > 40):
                        moved = False
                        if abs(dx) > abs(dy):
                            moved = game.move_right() if dx > 0 else game.move_left()
                        else:
                            moved = game.move_down() if dy > 0 else game.move_up()

                        if moved:
                            if stone_sound:
                                stone_sound.play()
                            game.add_new_tile()
                            if game.check_game_over():
                                game.game_over = True

        clock.tick(60)

if __name__ == "__main__":
    main()
