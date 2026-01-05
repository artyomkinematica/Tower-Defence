import arcade
import database as db

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TITLE = "Tower Defense"

GROUND_Y = 63

TOWER_HEIGHT = 500
PLATFORM_OFFSET = 0
TOWER_WIDTH = 254
TOWER_X = SCREEN_WIDTH // 2

PLAYER_WIDTH = 66
PLAYER_HEIGHT = 92
PLATFORM_Y = GROUND_Y + TOWER_HEIGHT - PLATFORM_OFFSET
PLAYER_START_Y = PLATFORM_Y + PLAYER_HEIGHT // 2

PLAYER_JUMP_SPEED = 12
GRAVITY = 0.9
PLAYER_MOVE_SPEED = 5
STEP_DISTANCE = 100


class MainMenuView(arcade.View):
    def on_show_view(self):
        self.menu_background = arcade.load_texture("assets/background_general.png")

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.menu_background)

        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (0, 0, 0, 100))

        arcade.draw_text("Tower Defense", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200,
                         arcade.color.WHITE, font_size=72, anchor_x="center", bold=True)

        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 400, 100, arcade.color.GREEN)
        arcade.draw_text("Начать игру", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.BLACK, font_size=40, anchor_x="center", anchor_y="center")

        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 300, 300, 80, arcade.color.BLUE)
        arcade.draw_text("Уровни", SCREEN_WIDTH // 2, 300,
                         arcade.color.WHITE, font_size=24, anchor_x="center", anchor_y="center")

        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 200, 300, 80, arcade.color.PURPLE)
        arcade.draw_text("Достижения", SCREEN_WIDTH // 2, 200,
                         arcade.color.WHITE, font_size=24, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if (SCREEN_WIDTH // 2 - 200 < x < SCREEN_WIDTH // 2 + 200 and
            SCREEN_HEIGHT // 2 - 50 < y < SCREEN_HEIGHT // 2 + 50):
            game_view = GameLevelView()
            game_view.setup()
            self.window.show_view(game_view)

        elif (SCREEN_WIDTH // 2 - 150 < x < SCREEN_WIDTH // 2 + 150 and
              300 - 40 < y < 300 + 40):
            level_view = LevelSelectView()
            self.window.show_view(level_view)

        elif (SCREEN_WIDTH // 2 - 150 < x < SCREEN_WIDTH // 2 + 150 and
              200 - 40 < y < 200 + 40):
            achievements_view = AchievementsView()
            self.window.show_view(achievements_view)


class LevelSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_background = None

    def on_show_view(self):
        self.menu_background = arcade.load_texture("assets/background_levels.jpg")

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.menu_background)
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (0, 0, 0, 150))

        arcade.draw_text("Выбор уровня", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100,
                         arcade.color.WHITE, font_size=48, anchor_x="center", anchor_y="center")

        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 300, 300, 80, arcade.color.GREEN)
        arcade.draw_text("Уровень 1", SCREEN_WIDTH // 2, 300,
                         arcade.color.BLACK, font_size=24, anchor_x="center", anchor_y="center")

        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 200, 300, 80, arcade.color.GOLD)
        arcade.draw_text("Уровень 2", SCREEN_WIDTH // 2, 200,
                         arcade.color.BLACK, font_size=24, anchor_x="center", anchor_y="center")

        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, 100, 300, 80, arcade.color.RED)
        arcade.draw_text("Назад", SCREEN_WIDTH // 2, 100,
                         arcade.color.WHITE, font_size=24, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if (SCREEN_WIDTH // 2 - 150 < x < SCREEN_WIDTH // 2 + 150 and
            300 - 40 < y < 300 + 40):
            game_view = GameLevelView()
            game_view.setup()
            self.window.show_view(game_view)

        elif (SCREEN_WIDTH // 2 - 150 < x < SCREEN_WIDTH // 2 + 150 and
              200 - 40 < y < 200 + 40):
            game_view = GameLevelView()
            game_view.setup(level=2)
            self.window.show_view(game_view)

        elif (SCREEN_WIDTH // 2 - 150 < x < SCREEN_WIDTH // 2 + 150 and
              100 - 40 < y < 100 + 40):
            menu_view = MainMenuView()
            self.window.show_view(menu_view)


class AchievementsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_background = None

    def on_show_view(self):
        self.menu_background = arcade.load_texture("assets/background_achievements.jpg")
        self.achievements = db.load_achievements()

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.menu_background)
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (0, 0, 0, 150))

        arcade.draw_text("Достижения", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100,
                         arcade.color.WHITE, font_size=36, anchor_x="center", anchor_y="center")

        y = SCREEN_HEIGHT - 150
        for ach in self.achievements:
            color = arcade.color.GOLD if ach['unlocked'] else arcade.color.WHITE
            arcade.draw_text(f"{ach['name']}: {ach['progress']}/{ach['max_progress']}",
                             100, y, color, 18)
            y -= 50

        arcade.draw_rectangle_filled(200, 80, 200, 60, arcade.color.GOLD)
        arcade.draw_text("Назад", 200, 80, arcade.color.BLACK, 16, anchor_x="center", anchor_y="center")

        arcade.draw_rectangle_filled(SCREEN_WIDTH - 200, 80, 200, 60, arcade.color.RED)
        arcade.draw_text("Очистить", SCREEN_WIDTH - 200, 80, arcade.color.WHITE, 16, anchor_x="center",
                         anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if 100 < x < 300 and 50 < y < 110:
            self.window.show_view(MainMenuView())

        elif SCREEN_WIDTH - 300 < x < SCREEN_WIDTH - 100 and 50 < y < 110:
            db.reset_achievements()
            self.achievements = db.load_achievements()


class GameLevelView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = None
        self.background = None
        self.tower_texture = None
        self.on_ground = False
        self.keys = set()
        self.facing_right = True
        self.walk_frame = 0
        self.walk_frames = []
        self.last_walk_time = 0
        self.achievement_notifications = []
        self.shown_notifications = set()
        self.last_x = 0
        self.step_accumulator = 0.0

    def setup(self):
        self.background = arcade.load_texture("assets/background.png")
        self.tower_texture = arcade.load_texture("assets/tower.png")

        self.idle_right = arcade.load_texture("assets/player_idle.png")
        self.run1_right = arcade.load_texture("assets/player_run1.png")
        self.run2_right = arcade.load_texture("assets/player_run2.png")
        self.jump_right = arcade.load_texture("assets/player_jump.png")

        self.idle_left = arcade.load_texture("assets/player_idle.png", flipped_horizontally=True)
        self.run1_left = arcade.load_texture("assets/player_run1.png", flipped_horizontally=True)
        self.run2_left = arcade.load_texture("assets/player_run2.png", flipped_horizontally=True)
        self.jump_left = arcade.load_texture("assets/player_jump.png", flipped_horizontally=True)

        self.walk_frames_right = [self.run1_right, self.run2_right]
        self.walk_frames_left = [self.run1_left, self.run2_left]

        self.player_sprite = arcade.Sprite(scale=1.5)
        self.player_sprite.texture = self.idle_right

        self.player_sprite.center_x = TOWER_X
        self.player_sprite.center_y = PLAYER_START_Y

        self.on_ground = True
        self.facing_right = True
        self.last_x = TOWER_X

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.player_sprite.draw()

        arcade.draw_lrwh_rectangle_textured(
            TOWER_X - TOWER_WIDTH // 2,
            GROUND_Y,
            TOWER_WIDTH,
            TOWER_HEIGHT,
            self.tower_texture
        )

        arcade.draw_text("← → : Ходьба | Пробел: Прыжок", 20, 20, arcade.color.WHITE, 18)

        for i, note in enumerate(self.achievement_notifications):
            y = SCREEN_HEIGHT - 50 - i * 40
            arcade.draw_text(note['text'], SCREEN_WIDTH - 20, y,
                             arcade.color.GOLD, 20, anchor_x="right")

        arcade.draw_rectangle_filled(80, SCREEN_HEIGHT - 40, 140, 60, arcade.color.DARK_RED)
        arcade.draw_text("Выйти", 80, SCREEN_HEIGHT - 40,
                         arcade.color.WHITE, 16, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time):
        self.player_sprite.center_y += self.player_sprite.change_y

        if self.player_sprite.center_y > PLAYER_START_Y:
            self.player_sprite.change_y -= GRAVITY
            self.on_ground = False
        else:
            self.player_sprite.center_y = PLAYER_START_Y
            self.player_sprite.change_y = 0
            self.on_ground = True

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

        old_x = self.player_sprite.center_x

        self.player_sprite.center_x += self.player_sprite.change_x

        tower_left = TOWER_X - TOWER_WIDTH // 2
        tower_right = TOWER_X + TOWER_WIDTH // 2

        player_left = self.player_sprite.center_x - self.player_sprite.width // 2
        player_right = self.player_sprite.center_x + self.player_sprite.width // 2

        if player_left < tower_left:
            self.player_sprite.center_x = tower_left + self.player_sprite.width // 2
        elif player_right > tower_right:
            self.player_sprite.center_x = tower_right - self.player_sprite.width // 2

        new_x = self.player_sprite.center_x
        if moving and abs(new_x - old_x) > 0.1:
            distance = abs(new_x - old_x)
            self.step_accumulator += distance / STEP_DISTANCE
            progress = int(self.step_accumulator)

            if progress > 0:
                ach_before = db.load_achievements()
                hundred_before = next((a for a in ach_before if a['id'] == 2), None)
                was_unlocked = hundred_before['unlocked'] if hundred_before else False

                db.update_achievement(2, progress)
                self.step_accumulator -= progress

                ach_after = db.load_achievements()
                hundred_after = next((a for a in ach_after if a['id'] == 2), None)
                is_now_unlocked = hundred_after['unlocked'] if hundred_after else False

                if not was_unlocked and is_now_unlocked:
                    self.show_achievement_notification(hundred_after['name'], ach_id=2)

        if not self.on_ground:
            self.player_sprite.texture = self.jump_left if not self.facing_right else self.jump_right
        elif moving:
            self.last_walk_time += delta_time
            if self.last_walk_time > 0.1:
                self.walk_frame = (self.walk_frame + 1) % 2
                self.last_walk_time = 0

            if self.facing_right:
                self.player_sprite.texture = self.walk_frames_right[self.walk_frame]
            else:
                self.player_sprite.texture = self.walk_frames_left[self.walk_frame]
        else:
            self.player_sprite.texture = self.idle_left if not self.facing_right else self.idle_right

        tower_left = TOWER_X - TOWER_WIDTH // 2
        tower_right = TOWER_X + TOWER_WIDTH // 2

        player_left = self.player_sprite.center_x - self.player_sprite.width // 2
        player_right = self.player_sprite.center_x + self.player_sprite.width // 2

        if player_left < tower_left:
            self.player_sprite.center_x = tower_left + self.player_sprite.width // 2
        elif player_right > tower_right:
            self.player_sprite.center_x = tower_right - self.player_sprite.width // 2

        to_remove = []
        for note in self.achievement_notifications:
            note['created_at'] += delta_time
            if note['created_at'] > note['lifetime']:
                to_remove.append(note)

        for note in to_remove:
            self.achievement_notifications.remove(note)

    def on_key_press(self, key, modifiers):
        self.keys.add(key)
        if key == arcade.key.SPACE and self.on_ground:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED

            achievements = db.load_achievements()
            first_jump = next((a for a in achievements if a['id'] == 1), None)

            if first_jump and not first_jump['unlocked']:
                db.update_achievement(1, 1)
                self.show_achievement_notification(first_jump['name'], ach_id=1)

    def on_key_release(self, key, modifiers):
        if key in self.keys:
            self.keys.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if (10 < x < 150) and (SCREEN_HEIGHT - 70 < y < SCREEN_HEIGHT - 10):
            menu_view = MainMenuView()
            self.window.show_view(menu_view)

    def show_achievement_notification(self, achievement_name, ach_id=None):
        if ach_id is not None and ach_id in self.shown_notifications:
            return
        if ach_id is not None:
            self.shown_notifications.add(ach_id)
        self.achievement_notifications.append({
            'text': f"Достижение: {achievement_name}!",
            'lifetime': 3.0,
            'created_at': 0.0
        })


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, resizable=False)


def main():
    db.init_db()
    print("Достижения при запуске:", db.load_achievements())
    window = GameWindow()
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()