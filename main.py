import arcade

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TITLE = "Tower Defense"

GROUND_Y = 63

TOWER_HEIGHT = 500
PLATFORM_OFFSET = 23
TOWER_WIDTH = 254
TOWER_X = SCREEN_WIDTH // 2

PLAYER_WIDTH = 66
PLAYER_HEIGHT = 92
PLATFORM_Y = GROUND_Y + TOWER_HEIGHT - PLATFORM_OFFSET
PLAYER_START_Y = PLATFORM_Y + PLAYER_HEIGHT // 2

PLAYER_JUMP_SPEED = 12
GRAVITY = 0.9
PLAYER_MOVE_SPEED = 5


class MainMenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Tower Defense", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200,
                         arcade.color.WHITE, font_size=72, anchor_x="center", bold=True)
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 400, 100, arcade.color.GREEN)
        arcade.draw_text("Начать игру", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.BLACK, font_size=40, anchor_x="center", anchor_y="center")
        arcade.draw_text("Используй ← → и ПРОБЕЛ", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150,
                         arcade.color.LIGHT_GRAY, font_size=24, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if (SCREEN_WIDTH // 2 - 200 < x < SCREEN_WIDTH // 2 + 200 and
            SCREEN_HEIGHT // 2 - 50 < y < SCREEN_HEIGHT // 2 + 50):
            game_view = GameLevelView()
            game_view.setup()
            self.window.show_view(game_view)


class GameLevelView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = None
        self.background = None
        self.tower_texture = None
        self.on_ground = False
        self.keys = set()
        self.facing_right = True
        self.walk_frame = 0  # текущий кадр анимации ходьбы
        self.walk_frames = []  # список текстур ходьбы
        self.last_walk_time = 0

    def setup(self):
        self.background = arcade.load_texture("assets/background.jpg")
        self.tower_texture = arcade.load_texture("assets/tower.png")

        # Загружаем текстуры
        idle = arcade.load_texture("assets/player_idle.png", scale=1.5)
        run1 = arcade.load_texture("assets/player_run1.png", scale=1.5)
        run2 = arcade.load_texture("assets/player_run2.png", scale=1.5)
        jump = arcade.load_texture("assets/player_jump.png", scale=1.5)

        # Создаём спрайт
        self.player_sprite = arcade.Sprite()
        self.player_sprite.texture = idle
        self.player_sprite.center_x = TOWER_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.on_ground = True
        self.facing_right = True

        # Подготовка анимации ходьбы
        self.walk_frames = [
            arcade.load_texture("assets/player_run1.png", scale=1.5),
            arcade.load_texture("assets/player_run2.png", scale=1.5)
        ]

        # Отражённые версии
        self.idle_left = arcade.load_texture("assets/player_idle.png", flipped_horizontally=True, scale=1.5)
        self.jump_left = arcade.load_texture("assets/player_jump.png", flipped_horizontally=True, scale=1.5)
        self.walk_frames_left = [
            arcade.load_texture("assets/player_run1.png", flipped_horizontally=True, scale=1.5),
            arcade.load_texture("assets/player_run2.png", flipped_horizontally=True, scale=1.5)
        ]

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.player_sprite.draw()

        arcade.draw_lrwh_rectangle_textured(
            TOWER_X - TOWER_WIDTH // 2,  # x: левый край
            GROUND_Y,  # y: нижний край (башня начинается от земли)
            TOWER_WIDTH,  # ширина
            TOWER_HEIGHT,  # высота
            self.tower_texture  # текстура
        )

        arcade.draw_text("← → : Ходьба | Пробел: Прыжок", 20, 20, arcade.color.WHITE, 18)

    def on_update(self, delta_time):
        # === Вертикальное движение ===
        self.player_sprite.center_y += self.player_sprite.change_y

        if self.player_sprite.center_y > PLAYER_START_Y:
            self.player_sprite.change_y -= GRAVITY
            self.on_ground = False
        else:
            self.player_sprite.center_y = PLAYER_START_Y
            self.player_sprite.change_y = 0
            self.on_ground = True

        # === Горизонтальное движение ===
        self.player_sprite.change_x = 0
        moving = False

        if arcade.key.LEFT in self.keys:
            self.player_sprite.change_x = -PLAYER_MOVE_SPEED
            self.facing_right = False
            moving = True
        elif arcade.key.RIGHT in self.keys:
            self.player_sprite.change_x = PLAYER_MOVE_SPEED
            self.facing_right = True
            moving = True

        self.player_sprite.center_x += self.player_sprite.change_x

        # === Анимация ===
        # Если не на земле — прыжок
        if not self.on_ground:
            self.player_sprite.texture = self.jump_left if not self.facing_right else self.jump_right
        # Если на земле и двигается — бег
        elif moving:
            # Меняем кадр каждые 0.1 секунды
            self.last_walk_time += delta_time
            if self.last_walk_time > 0.1:
                self.walk_frame = (self.walk_frame + 1) % 2
                self.last_walk_time = 0

            if self.facing_right:
                self.player_sprite.texture = self.walk_frames[self.walk_frame]
            else:
                self.player_sprite.texture = self.walk_frames_left[self.walk_frame]
        # Если стоит — idle
        else:
            self.player_sprite.texture = self.idle_left if not self.facing_right else self.idle_right

        # === Ограничение по краям ===
        tower_left = TOWER_X - TOWER_WIDTH // 2
        tower_right = TOWER_X + TOWER_WIDTH // 2

        player_left = self.player_sprite.center_x - self.player_sprite.width // 2
        player_right = self.player_sprite.center_x + self.player_sprite.width // 2

        if player_left < tower_left:
            self.player_sprite.center_x = tower_left + self.player_sprite.width // 2
        elif player_right > tower_right:
            self.player_sprite.center_x = tower_right - self.player_sprite.width // 2

    def on_key_press(self, key, modifiers):
        self.keys.add(key)
        if key == arcade.key.SPACE:
            #print(f"Пробел нажат! on_ground = {self.on_ground}")
            if self.on_ground:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                #print("Прыжок выполнен!")

    def on_key_release(self, key, modifiers):
        if key in self.keys:
            self.keys.remove(key)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, resizable=False)


def main():
    window = GameWindow()
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()