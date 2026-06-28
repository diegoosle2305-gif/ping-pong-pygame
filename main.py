import pygame
import sys  
  
# Initialize Pygame  
pygame.init()  
  
# Set up the display  
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480  
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
  
# Define colors  
WHITE = (255, 255, 255) 
GREEN = (0, 255, 0)
RED = (255, 0, 0) 
BACKGROUND_COLOR = (0, 0, 0)  
  
# Set initial position and velocity of the ball
STARTING_X, STARTING_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  
STARTING_SPEED_X, STARTING_SPEED_Y = 2, 2  
  
# Define the size of the ball
pixel_ball_size = 12  
  
# Set up the clock for frame rate control  
clock = pygame.time.Clock()  

class Object:

    def __init__(self, x, y, width, height, color):  
        self.rect = pygame.Rect(x, y, width, height)  
        self.color = color  
  
    def draw(self, surface):  
        pygame.draw.rect(surface, self.color, self.rect)  
  
    def move(self, dx, dy):  
        self.rect.x += dx  
        self.rect.y += dy
    
    def is_colliding_with(self, other):  
        return self.rect.colliderect(other.rect)
    
    def is_touching_horizontal_walls(self, screen_width, screen_height):  
        if self.rect.x <= 0 or self.rect.x + self.rect.width >= screen_width:  
            return True  
        return False
    
    def is_touching_vertical_walls(self, screen_width, screen_height):  
        if self.rect.y <= 0 or self.rect.y + self.rect.height >= screen_height:  
            return True  
        return False

class Player(Object):
    def teleport(self, x, y):  
        self.rect.x = x  
        self.rect.y = y

class Ball(Object):
    def __init__(self, x, y, speed_x, speed_y, width, height, color):  
        super().__init__(x, y, width, height, color)  
        self.speed_x = speed_x  
        self.speed_y = speed_y
    
    def move(self,player,enemie):
        if self.is_colliding_with(player):
            if self.speed_y > 0:
                self.speed_y *= -1
                self.speed_y *= 1.05
                self.speed_x *= 1.05
        if self.is_colliding_with(enemie):
            if self.speed_y < 0:
                self.speed_y *= -1
                self.speed_y *= 1.05
                self.speed_x *= 1.05
        if self.is_touching_horizontal_walls(SCREEN_WIDTH, SCREEN_HEIGHT):
            self.speed_x *= -1
        if self.is_touching_vertical_walls(SCREEN_WIDTH, SCREEN_HEIGHT):
            self.speed_y *= -1
        super().move(self.speed_x, self.speed_y)

class Enemie(Object):

    def __init__(self, x, y, width, height, color,speed_x,ball):  
        super().__init__(x, y, width, height, color)  
        self.speed_x = speed_x
        self.ball = ball
    
    def move(self):
        velocity_enemie = self.speed_x / ((self.ball.rect.y + 50) / self.rect.y)
        if self.rect.x + self.rect.width / 2 < self.ball.rect.x:
            super().move(velocity_enemie, 0)
        else:
            super().move(-velocity_enemie, 0)

player = Player(300, SCREEN_HEIGHT - 50, 50, 10, GREEN)  # Create a player instanceç

ball = Ball(STARTING_X, STARTING_Y,STARTING_SPEED_X, STARTING_SPEED_Y, pixel_ball_size, pixel_ball_size, RED)  # Create a ball instance

enemie = Enemie(300, 50, 50, 10, WHITE, 10, ball)  # Create an enemy instance


def main_game_loop():
    cursor_pos = pygame.mouse.get_pos() 

    # Handle events  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()  
            sys.exit()  


    if ball.is_touching_vertical_walls(SCREEN_WIDTH, SCREEN_HEIGHT):
        print("Game Over")


    player.teleport(cursor_pos[0] - player.rect.width / 2, 400)  # Player movement
    enemie.move()  # Move the enemy based on the ball's position
    ball.move(player, enemie)  # Move the ball and check for collisions with the player and enemy

    #Draw everything

    # Fill the background  
    SCREEN.fill(BACKGROUND_COLOR)  
  
    
    ball.draw(SCREEN)  # Draw the ball on the screen
    player.draw(SCREEN)  # Draw the player on the screen   
    enemie.draw(SCREEN)  # Draw the enemy on the screen
  
    # Update the display  
    pygame.display.flip()  
  
    # Limit the frame rate  
    clock.tick(60)


while True:
    main_game_loop()