import pygame
import os
import random
from user_manager import UserManager
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

MENU_STATE = "menu"
GAME_STATE = "game"
GAME_OVER_STATE = "game_over"
LOGIN_STATE = "login"
REGISTER_STATE = "register"

BULLET_COLOR = (255, 0, 0)  # Red color for bullets
BULLET_SPEED = 15
BULLET_SIZE = 10
GIFT_SPAWN_CHANCE = 0.8  # 100% chance when it's time to spawn (after 5 obstacles)
OBSTACLE_COUNT_FOR_GIFT = 3  # Every N obstacles
INITIAL_BULLETS = 5
GIFT_MIN_HEIGHT = 300  # Higher position
GIFT_MAX_HEIGHT = 150   # Even higher for jump collection
MIN_OBSTACLE_DISTANCE = 50  # Keep good distance for the larger gift box

# Add gift box appearance constants
GIFT_BOX = pygame.image.load(os.path.join("Assets/Other", "GiftBox.png"))


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_SIZE, BULLET_SIZE)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.x += self.speed
        return self.rect.x > SCREEN_WIDTH  # Return True if bullet is off screen

    def draw(self, screen):
        pygame.draw.circle(screen, BULLET_COLOR, self.rect.center, BULLET_SIZE // 2)


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.bullets = []
        self.shoot_cooldown = 0
        self.SHOOT_DELAY = 20  # Minimum frames between shots
        self.bullet_count = INITIAL_BULLETS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if userInput[pygame.K_s] and self.shoot_cooldown == 0 and self.bullet_count > 0:
            # Shoot from dinosaur's mouth position
            bullet_x = self.dino_rect.x + self.dino_rect.width
            bullet_y = self.dino_rect.y + self.dino_rect.height // 2
            self.bullets.append(Bullet(bullet_x, bullet_y))
            self.shoot_cooldown = self.SHOOT_DELAY
            self.bullet_count -= 1  # Decrease bullet count

        # Update bullets
        self.bullets = [bullet for bullet in self.bullets if not bullet.update()]

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
            if self.dino_rect.y >= self.Y_POS:
                self.dino_rect.y = self.Y_POS
                self.dino_jump = False
                self.jump_vel = self.JUMP_VEL

    def add_bullets(self, amount=1):
        self.bullet_count += amount

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(SCREEN)
        # Draw bullet count
        font = pygame.font.Font('freesansbold.ttf', 20)
        bullet_text = font.render(f"Bullets: {self.bullet_count}", True, (0, 0, 0))
        SCREEN.blit(bullet_text, (20, 40))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game_speed):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            return True
        return False

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


class Game:
    def __init__(self):
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.obstacles = []
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.game_state = LOGIN_STATE
        self.player = None
        self.cloud = None
        self.paused = False
        self.clock = pygame.time.Clock()
        self.user_manager = UserManager()
        self.login_username = self.user_manager.last_login["username"]
        self.login_password = self.user_manager.last_login["password"]
        self.input_state = "username"
        self.error_message = ""
        self.current_score_saved = False
        self.gift_boxes = []
        self.obstacle_count = 0  # Add counter for obstacles

    def reset_game(self):
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.obstacles.clear()
        self.player = Dinosaur()
        self.cloud = Cloud()
        self.current_score_saved = False
        self.gift_boxes = []
        self.obstacle_count = 0  # Reset obstacle counter
        self.player.bullet_count = INITIAL_BULLETS

    def draw_pause_screen(self):
        SCREEN.fill((173, 216, 230))
        pause_font = pygame.font.Font('freesansbold.ttf', 30)
        
        # Show current user
        user_text = pause_font.render(f"Current User: {self.user_manager.current_user}", True, (0, 0, 0))
        user_rect = user_text.get_rect()
        user_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        
        # Pause text
        pause_text = pause_font.render("GAME PAUSED", True, (0, 0, 0))
        pause_rect = pause_text.get_rect()
        pause_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        
        # Instructions
        inst_font = pygame.font.Font('freesansbold.ttf', 20)
        instructions = [
            "Press SPACE to Resume",
            "Press R to Restart",
            "Press Q to Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = inst_font.render(instruction, True, (0, 0, 0))
            inst_rect = inst_text.get_rect()
            inst_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40)
            SCREEN.blit(inst_text, inst_rect)
        
        SCREEN.blit(user_text, user_rect)
        SCREEN.blit(pause_text, pause_rect)

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        
        if len(self.login_username) > 10:
            username = self.login_username[:10] + "**"
        else:
            username = self.login_username
        text = self.font.render(f"User: {username}, Points: {self.points}", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    def background(self):
        image_width = BG.get_width()
        SCREEN.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def handle_menu_state(self):
        SCREEN.fill((173, 216, 230))
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press any Key to Start", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.reset_game()
                self.game_state = GAME_STATE
        return True

    def get_safe_gift_position(self):
        """Calculate a safe position between obstacles for the gift box"""
        obstacle_size = 100

        safe_start = SCREEN_WIDTH + obstacle_size + MIN_OBSTACLE_DISTANCE
        safe_end = SCREEN_WIDTH * 2 - MIN_OBSTACLE_DISTANCE
        return random.randint(safe_start, safe_end)

    def handle_game_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.paused:  # Allow restart when paused
                    self.reset_game()
                    self.paused = False
                    return True
                elif event.key == pygame.K_q and self.paused:  # Allow quit when paused
                    return False

        if not self.paused:
            SCREEN.fill((173, 216, 230))
            userInput = pygame.key.get_pressed()

            self.player.draw(SCREEN)
            self.player.update(userInput)

            # Check bullet collisions with obstacles
            for bullet in self.player.bullets[:]:  # Create a copy of the list to modify it safely
                for obstacle in self.obstacles[:]:  # Same here
                    if bullet.rect.colliderect(obstacle.rect):
                        if bullet in self.player.bullets:  # Check again as it might have been removed
                            self.player.bullets.remove(bullet)
                        if obstacle in self.obstacles:  # Check again as it might have been removed
                            self.obstacles.remove(obstacle)
                        break

            # Check dinosaur collisions with remaining obstacles
            for obstacle in self.obstacles:
                obstacle.draw(SCREEN)
                if self.player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(2000)
                    self.game_state = GAME_OVER_STATE
                    return True

            self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.update(self.game_speed)]
            
            if len(self.obstacles) == 0:
                obstacle_type = random.randint(0, 2)
                if obstacle_type == 0:
                    self.obstacles.append(SmallCactus(SMALL_CACTUS))
                elif obstacle_type == 1:
                    self.obstacles.append(LargeCactus(LARGE_CACTUS))
                else:
                    self.obstacles.append(Bird(BIRD))
                
                # Increment obstacle counter and check for gift box spawn
                self.obstacle_count += 1
                if self.obstacle_count >= OBSTACLE_COUNT_FOR_GIFT:
                    if len(self.gift_boxes) == 0 and random.random() < GIFT_SPAWN_CHANCE:
                        safe_x = self.get_safe_gift_position()
                        if safe_x is not None:
                            gift = GiftBox()
                            gift.rect.x = safe_x
                            self.gift_boxes.append(gift)
                            self.obstacle_count = 0

            # Update and check gift box collisions
            self.gift_boxes = [gift for gift in self.gift_boxes if not gift.update(self.game_speed)]
            for gift in self.gift_boxes[:]:
                gift.draw(SCREEN)
                if self.player.dino_rect.colliderect(gift.rect):
                    self.player.add_bullets()
                    self.gift_boxes.remove(gift)

            self.background()
            self.cloud.draw(SCREEN)
            self.cloud.update(self.game_speed)
            self.score()  # Update score last
        else:
            self.draw_pause_screen()
        return True

    def handle_game_over_state(self):
        if self.user_manager.current_user and not self.current_score_saved:
            self.user_manager.add_score(self.points)
            self.current_score_saved = True
        
        top_scores = self.user_manager.get_top_scores()
        
        SCREEN.fill((173, 216, 230))
        font = pygame.font.Font('freesansbold.ttf', 30)

        # Move dinosaur icon to 1/8 of screen height (about 75px from top)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 8))

        # Game over and current score - keep other positions the same
        game_over_text = font.render("GAME OVER", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

        # Show current user
        user_text = font.render(f"Player: {self.user_manager.current_user}", True, (0, 0, 0))
        user_rect = user_text.get_rect()
        user_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)

        score_text = font.render(f"Your Score: {self.points}", True, (0, 0, 0))
        score_rect = score_text.get_rect()
        score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)

        # Game over options
        options = [
            ("R - Restart", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)),
            ("L - Switch User", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)),
            ("Q - Quit", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        ]

        for text, pos in options:
            option_text = font.render(text, True, (0, 0, 0))
            option_rect = option_text.get_rect()
            option_rect.center = pos
            SCREEN.blit(option_text, option_rect)

        SCREEN.blit(game_over_text, game_over_rect)
        SCREEN.blit(user_text, user_rect)
        SCREEN.blit(score_text, score_rect)

        # Draw scores section with adjusted position
        y_offset = SCREEN_HEIGHT // 2 + 140
        score_font = pygame.font.Font('freesansbold.ttf', 20)
        
        # Global scores (left side)
        title_text = score_font.render("Global Top 5:", True, (0, 0, 0))
        SCREEN.blit(title_text, (SCREEN_WIDTH // 4 - 100, y_offset))
        
        for i, score in enumerate(top_scores):
            score_text = score_font.render(
                f"{i+1}. {score['username']}: {score['score']}", 
                True, (0, 0, 0)
            )
            SCREEN.blit(score_text, (SCREEN_WIDTH // 4 - 100, y_offset + 25 * (i+1)))

        # Personal scores (right side)
        if self.user_manager.current_user:
            user_scores = self.user_manager.get_user_scores(self.user_manager.current_user)
            title_text = score_font.render("Your Top 5:", True, (0, 0, 0))
            SCREEN.blit(title_text, (3 * SCREEN_WIDTH // 4 - 100, y_offset))
            
            for i, score in enumerate(user_scores):
                score_text = score_font.render(
                    f"{i+1}. {score}", 
                    True, (0, 0, 0)
                )
                SCREEN.blit(score_text, (3 * SCREEN_WIDTH // 4 - 100, y_offset + 25 * (i+1)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.current_score_saved = False
                    self.reset_game()
                    self.game_state = GAME_STATE
                elif event.key == pygame.K_l:  # Switch user
                    self.user_manager.logout()
                    # Clear login credentials
                    self.login_username = ""
                    self.login_password = ""
                    self.game_state = LOGIN_STATE
                elif event.key == pygame.K_q:
                    return False
        return True

    def handle_login_state(self):
        SCREEN.fill((173, 216, 230))
        font = pygame.font.Font('freesansbold.ttf', 30)
        
        active_color = (0, 180, 0)  # Green for active field
        inactive_color = (0, 0, 0)  # Black for inactive field
        
        title = font.render("Chrome Dino Game", True, (0, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        SCREEN.blit(title, title_rect)

        # Draw username field with active indicator
        username_text = font.render(f"Username: {self.login_username}", True, 
                                  active_color if self.input_state == "username" else inactive_color)
        SCREEN.blit(username_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        # Draw password field with active indicator
        password_display = '*' * len(self.login_password)
        password_text = font.render(f"Password: {password_display}", True,
                                  active_color if self.input_state == "password" else inactive_color)
        SCREEN.blit(password_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        if self.error_message:
            error_text = font.render(self.error_message, True, (255, 0, 0))
            SCREEN.blit(error_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))

        inst_font = pygame.font.Font('freesansbold.ttf', 20)
        instructions = [
            "Press TAB to switch between username and password",
            "Press ENTER to login",
            "Press / to register new account"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = inst_font.render(instruction, True, (0, 0, 0))
            SCREEN.blit(inst_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 100 + i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.input_state = "password" if self.input_state == "username" else "username"
                elif event.key == pygame.K_RETURN:
                    success, message = self.user_manager.login_user(self.login_username, self.login_password)
                    if success:
                        self.game_state = MENU_STATE
                        self.error_message = ""
                        self.reset_game()
                    else:
                        self.error_message = message
                elif event.key == pygame.K_SLASH:
                    self.game_state = REGISTER_STATE
                    self.login_username = ""
                    self.login_password = ""
                elif event.key == pygame.K_BACKSPACE:
                    if self.input_state == "username":
                        self.login_username = self.login_username[:-1]
                    else:
                        self.login_password = self.login_password[:-1]
                elif event.unicode.isprintable():
                    if self.input_state == "username":
                        self.login_username += event.unicode
                    else:
                        self.login_password += event.unicode
        
        return True

    def handle_register_state(self):
        SCREEN.fill((173, 216, 230))
        font = pygame.font.Font('freesansbold.ttf', 30)
        
        active_color = (0, 180, 0)
        inactive_color = (0, 0, 0)
        
        title = font.render("Register New Account", True, (0, 0, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        SCREEN.blit(title, title_rect)

        username_text = font.render(f"Username: {self.login_username}", True,
                                  active_color if self.input_state == "username" else inactive_color)
        SCREEN.blit(username_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        password_display = '*' * len(self.login_password)
        password_text = font.render(f"Password: {password_display}", True,
                                  active_color if self.input_state == "password" else inactive_color)
        SCREEN.blit(password_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        if self.error_message:
            error_text = font.render(self.error_message, True, (255, 0, 0))
            SCREEN.blit(error_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))

        inst_font = pygame.font.Font('freesansbold.ttf', 20)
        instructions = [
            "Press TAB to switch between username and password",
            "Press ENTER to register",
            "Press / to go back to login"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = inst_font.render(instruction, True, (0, 0, 0))
            SCREEN.blit(inst_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 100 + i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.input_state = "password" if self.input_state == "username" else "username"
                elif event.key == pygame.K_RETURN:
                    success, message = self.user_manager.register_user(self.login_username, self.login_password)
                    if success:
                        self.error_message = "Registration successful! Press / to login"
                    else:
                        self.error_message = message
                elif event.key == pygame.K_SLASH:
                    self.game_state = LOGIN_STATE
                    self.error_message = ""
                    # Clear login credentials
                    self.login_username = ""
                    self.login_password = ""
                elif event.key == pygame.K_BACKSPACE:
                    if self.input_state == "username":
                        self.login_username = self.login_username[:-1]
                    else:
                        self.login_password = self.login_password[:-1]
                elif event.unicode.isprintable():
                    if self.input_state == "username":
                        self.login_username += event.unicode
                    else:
                        self.login_password += event.unicode
        
        return True

    def run(self):
        while True:
            if self.game_state == LOGIN_STATE:
                if not self.handle_login_state():
                    break
            elif self.game_state == REGISTER_STATE:
                if not self.handle_register_state():
                    break
            elif self.game_state == MENU_STATE:
                if not self.handle_menu_state():
                    break
            elif self.game_state == GAME_STATE:
                if not self.handle_game_state():
                    break
            elif self.game_state == GAME_OVER_STATE:
                if not self.handle_game_over_state():
                    break

            self.clock.tick(30)
            pygame.display.update()

        pygame.quit()
        exit()

    def is_safe_to_spawn_gift(self):
        # Check distance from all obstacles
        for obstacle in self.obstacles:
            distance = abs(obstacle.rect.x - SCREEN_WIDTH)
            if distance < MIN_OBSTACLE_DISTANCE:
                return False
        return True


class GiftBox:
    def __init__(self):
        self.image = GIFT_BOX  # 100x100 image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH  # This will be overridden by safe position
        # Random height between max (higher) and min (lower)
        self.rect.y = random.randint(GIFT_MAX_HEIGHT, GIFT_MIN_HEIGHT)

    def update(self, game_speed):
        self.rect.x -= game_speed
        return self.rect.x < -self.rect.width

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)


if __name__ == "__main__":
    game = Game()
    game.run()
