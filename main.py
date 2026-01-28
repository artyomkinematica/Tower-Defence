import arcade
import database as db
import random
import math

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

ENEMY_HEIGHT = 66
ENEMY_WIDTH = 92

ENEMY_SPEED = 2
ENEMY_SPAWN_INTERVAL = 2.0
BULLET_SPEED = 10
FIRE_RATE = 0.125


class Bullet:
    """создание объектов снарядов"""
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.radius = 8
        self.color = arcade.color.YELLOW
        self.speed = BULLET_SPEED

        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            self.dx = dx / distance * self.speed
            self.dy = dy / distance * self.speed
        else:
            self.dx = 0
            self.dy = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)

    def is_off_screen(self):
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)


class Enemy:
    """создание врагов"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED
        self.health = 3
        self.max_health = 3
        self.color = random.choices(range(256), k=3)

    def update(self):
        target_x = SCREEN_WIDTH // 2
        target_y = GROUND_Y + ENEMY_HEIGHT // 2

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)

        health_width = (self.width - 10) * (self.health / self.max_health)
        arcade.draw_rectangle_filled(self.x, self.y + self.height // 2 + 10,
                                     self.width - 10, 4, arcade.color.DARK_GRAY)
        arcade.draw_rectangle_filled(self.x - (self.width - 10) // 2 + health_width // 2,
                                     self.y + self.height // 2 + 10,
                                     health_width, 4, arcade.color.GREEN)

    def take_damage(self, damage=1):
        self.health -= damage
        return self.health <= 0

    def collides_with(self, bullet):
        return (abs(self.x - bullet.x) < self.width // 2 + bullet.radius and
                abs(self.y - bullet.y) < self.height // 2 + bullet.radius)


class MainMenuView(arcade.View):
    """отрисовка меню игры"""
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
    """отрисовка меню выбора уровней"""
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
    """отрисовка меню достижений"""
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
    """Отрисовка уровней игры"""
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

        self.bullets = []
        self.enemies = []
        self.time_since_last_shot = 0
        self.time_since_last_spawn = 0
        self.enemies_killed = 0
        self.health = 100
        self.game_over = False

    def setup(self, level=1):
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

        self.bullets = []
        self.enemies = []
        self.time_since_last_shot = 0
        self.time_since_last_spawn = 0
        self.enemies_killed = 0
        self.health = 100
        self.game_over = False

        global ENEMY_SPEED, ENEMY_SPAWN_INTERVAL
        if level == 1:
            ENEMY_SPEED = 2
            ENEMY_SPAWN_INTERVAL = 2.0
        elif level == 2:
            ENEMY_SPEED = 3
            ENEMY_SPAWN_INTERVAL = 1.5

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

        for enemy in self.enemies:
            enemy.draw()

        for bullet in self.bullets:
            bullet.draw()

        arcade.draw_text("← → : Ходьба | Пробел: Прыжок | ЛКМ: Стрельба", 20, 20, arcade.color.WHITE, 18)

        arcade.draw_text(f"Здоровье: {self.health}", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30,
                         arcade.color.WHITE, 24, anchor_x="right")

        arcade.draw_text(f"Уничтожено врагов: {self.enemies_killed}", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 60,
                         arcade.color.WHITE, 20, anchor_x="right")

        if not self.game_over:
            arcade.draw_rectangle_filled(80, SCREEN_HEIGHT - 40, 140, 60, arcade.color.DARK_RED)
            arcade.draw_text("Выйти", 80, SCREEN_HEIGHT - 40,
                             arcade.color.WHITE, 16, anchor_x="center", anchor_y="center")

        for i, note in enumerate(self.achievement_notifications):
            y = SCREEN_HEIGHT - 100 - i * 40
            arcade.draw_text(note['text'], SCREEN_WIDTH - 20, y,
                             arcade.color.GOLD, 20, anchor_x="right")

        if self.game_over:
            arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, (0, 0, 0, 200))
            arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                             arcade.color.RED, 72, anchor_x="center", anchor_y="center")
            arcade.draw_text(f"Уничтожено врагов: {self.enemies_killed}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                             arcade.color.WHITE, 36, anchor_x="center", anchor_y="center")
            arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 200, 80, arcade.color.GREEN)
            arcade.draw_text("Меню", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150,
                             arcade.color.BLACK, 24, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time):
        if self.game_over:
            return

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

        new_x = self.player_sprite.center_x + self.player_sprite.change_x

        tower_left_boundary = TOWER_X - TOWER_WIDTH // 2 + PLAYER_WIDTH // 2
        tower_right_boundary = TOWER_X + TOWER_WIDTH // 2 - PLAYER_WIDTH // 2

        if new_x < tower_left_boundary:
            new_x = tower_left_boundary
        elif new_x > tower_right_boundary:
            new_x = tower_right_boundary

        self.player_sprite.center_x = new_x

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

        if moving and abs(new_x - old_x) > 0.1:
            distance = abs(new_x - old_x)
            self.step_accumulator += distance

            if self.step_accumulator >= STEP_DISTANCE:
                steps_count = int(self.step_accumulator // STEP_DISTANCE)

                current_achievements = db.load_achievements()
                step_achievement = next((a for a in current_achievements if a['id'] == 2), None)
                if step_achievement:
                    was_unlocked = step_achievement['unlocked']

                    db.update_achievement(2, steps_count)
                    self.step_accumulator -= steps_count * STEP_DISTANCE

                    updated_achievements = db.load_achievements()
                    updated_step_ach = next((a for a in updated_achievements if a['id'] == 2), None)
                    if updated_step_ach and not was_unlocked and updated_step_ach['unlocked']:
                        self.show_achievement_notification(updated_step_ach['name'], ach_id=2)
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.update()
            if bullet.is_off_screen():
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)

        enemies_to_remove = []
        for enemy in self.enemies:
            enemy.update()

            bullets_to_remove_local = []
            for bullet in self.bullets:
                if enemy.collides_with(bullet):
                    if enemy.take_damage():
                        enemies_to_remove.append(enemy)
                        self.enemies_killed += 1
                    bullets_to_remove_local.append(bullet)

            for bullet in bullets_to_remove_local:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

            if enemy.x > TOWER_X - TOWER_WIDTH // 2 and enemy.x < TOWER_X + TOWER_WIDTH // 2:
                self.health -= 10
                enemies_to_remove.append(enemy)

                if self.health <= 0:
                    self.game_over = True
                    self.health = 0

        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)

        self.time_since_last_spawn += delta_time
        if self.time_since_last_spawn >= ENEMY_SPAWN_INTERVAL:
            side = random.choice(['left', 'right'])
            if side == 'left':
                x = -ENEMY_WIDTH
            else:
                x = SCREEN_WIDTH + ENEMY_WIDTH

            y = GROUND_Y + ENEMY_HEIGHT // 2 + random.randint(-50, 50)
            self.enemies.append(Enemy(x, y))
            self.time_since_last_spawn = 0

        self.time_since_last_shot += delta_time
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
        if self.game_over:
            if (SCREEN_WIDTH // 2 - 100 < x < SCREEN_WIDTH // 2 + 100 and
                    SCREEN_HEIGHT // 2 - 190 < y < SCREEN_HEIGHT // 2 - 110):
                menu_view = MainMenuView()
                self.window.show_view(menu_view)
            return
        if (10 < x < 150) and (SCREEN_HEIGHT - 70 < y < SCREEN_HEIGHT - 10):
            menu_view = MainMenuView()
            self.window.show_view(menu_view)
        elif button == arcade.MOUSE_BUTTON_LEFT and self.time_since_last_shot >= FIRE_RATE or\
            button == arcade.MOUSE_BUTTON_RIGHT and self.time_since_last_shot >= FIRE_RATE:
            self.shoot(x, y)
            self.time_since_last_shot = 0

    def shoot(self, target_x, target_y):
        """Создание пули от игрока к цели"""
        bullet = Bullet(self.player_sprite.center_x, self.player_sprite.center_y,
                        target_x, target_y)
        self.bullets.append(bullet)

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
    """отрисовка окна приложения"""
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, resizable=False)


def main():
    """запуск игры"""
    db.init_db()
    print("Достижения при запуске:", db.load_achievements())
    window = GameWindow()
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
