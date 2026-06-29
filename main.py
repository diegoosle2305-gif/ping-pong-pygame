import pygame
import sys  
import os
import random
  
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
PIXEL_BALL_SIZE = 12  

#This sould be in 0 for starting the game in the title screen, but for testing purposes it is set to 1
state_of_game = 0

# Set up the clock for frame rate control  
clock = pygame.time.Clock()  

def load_image(path):
    try:
        image = pygame.image.load(os.path.join(path))
        return image
    except Exception as e:
        print(f"Unable to load image at {path}: {e}")
        image = pygame.image.load(r"data\images\noTextureImg.png")
        return image

#Game classes
class Object:

    def __init__(self, x, y, width, height, image):  
        self.rect = pygame.Rect(x, y, width, height)  
        self.image = pygame.transform.scale(image, (width, height))  
  
    def draw(self):  
        SCREEN.blit(self.image, self.rect)  
  
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
    def __init__(self, x, y, speed_x, speed_y, width, height, image):  
        super().__init__(x, y, width, height, image)  
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

    def __init__(self, x, y, width, height, image,speed_x,ball):  
        super().__init__(x, y, width, height, image)  
        self.speed_x = speed_x
        self.ball = ball
    
    def move(self):
        velocity_enemie = self.speed_x / ((self.ball.rect.y + 50) / self.rect.y)
        if self.rect.x + self.rect.width / 2 < self.ball.rect.x:
            super().move(velocity_enemie, 0)
        else:
            super().move(-velocity_enemie, 0)

player = Player(300, SCREEN_HEIGHT - 50, 50, 10, load_image("player.png"))  # Create a player instance

ball = Ball(STARTING_X, STARTING_Y,STARTING_SPEED_X, STARTING_SPEED_Y, PIXEL_BALL_SIZE, PIXEL_BALL_SIZE, load_image("data/images/ball.png"))  # Create a ball instance

enemie = Enemie(300, 50, 50, 10, load_image("data/images/enemie.png"), 10, ball)  # Create an enemy instance

def reset_game():
    global ball, player, enemie
    player = Player(300, SCREEN_HEIGHT - 50, 50, 10, load_image("data/images/player.png"))  # Reset the player instance
    ball = Ball(STARTING_X, STARTING_Y,STARTING_SPEED_X, STARTING_SPEED_Y, PIXEL_BALL_SIZE, PIXEL_BALL_SIZE, load_image("data/images/ball.png"))  # Reset the ball instance
    enemie = Enemie(300, 50, 50, 10, load_image("data/images/enemie.png"), 10, ball)  # Reset the enemy instance

# UI Clases
class Button(Object):
    def is_cursor_over(self, cursor_pos):
        if cursor_pos[0] >= self.rect.x and cursor_pos[0] <= self.rect.x + self.rect.width and cursor_pos[1] >= self.rect.y and cursor_pos[1] <= self.rect.y + self.rect.height:
            return True
        return False

button = Button(200, 200, 100, 50, load_image("data/images/titleImg/SettingImg.jpg"))  # Create a button instance

#Game Update Loops

def main_game_loop():

    if ball.is_touching_vertical_walls(SCREEN_WIDTH, SCREEN_HEIGHT):
        print("Game Over")


    player.teleport(cursor_pos[0] - player.rect.width / 2, 400)  # Player movement
    enemie.move()  # Move the enemy based on the ball's position
    ball.move(player, enemie)  # Move the ball and check for collisions with the player and enemy

    #Draw everything

    # Fill the background  
    SCREEN.fill(BACKGROUND_COLOR)  
  
    
    ball.draw()  # Draw the ball on the screen
    player.draw()  # Draw the player on the screen   
    enemie.draw()  # Draw the enemy on the screen



print("Game started")
while True:
    cursor_pos = pygame.mouse.get_pos() 
    # Handle events     
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()  
            sys.exit()  
    
    
    SCREEN.fill(BACKGROUND_COLOR)
    
    #Chose what update loop to run based on the state of the game
    if state_of_game == 0:
        button.draw()
    elif state_of_game == 1:
        #Game update
        main_game_loop()
    
    # Update the display  
    pygame.display.flip()  
    # Limit the frame rate  
    clock.tick(60)