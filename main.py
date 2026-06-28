import pygame
import sys  
  
# Initialize Pygame  
pygame.init()  
  
# Set up the display  
screen_width, screen_height = 640, 480  
screen = pygame.display.set_mode((screen_width, screen_height))  
  
# Define colors  
white = (255, 255, 255) 
green = (0, 255, 0)
red = (255, 0, 0) 
background_color = (0, 0, 0)  
  
# Set initial position and velocity of the pixel  
x, y = screen_width // 2, screen_height // 2  
speed_x, speed_y = 2, 2  
  
# Define the size of the pixel  
pixel_size = 8  
  
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

player = Player(300, 400, 50, 10, green)  # Create a player instance

class Ball(Object):
    def __init__(self, x, y, speed_x, speed_y, width, height, color):  
        super().__init__(x, y, width, height, color)  
        self.speed_x = speed_x  
        self.speed_y = speed_y
    
    def move(self,player):
        if self.is_colliding_with(player):
            if self.speed_y > 0:
                self.speed_y *= -1
        if self.is_touching_horizontal_walls(screen_width, screen_height):
            self.speed_x *= -1
        if self.is_touching_vertical_walls(screen_width, screen_height):
            self.speed_y *= -1
        super().move(self.speed_x, self.speed_y)

ball = Ball(x, y,speed_x, speed_y, pixel_size, pixel_size, red)  # Create a ball instance

def check_collision_with_cursor(x, y, cursor_pos):  
    """Check if the pixel is within the cursor's area."""  
    cursor_x, cursor_y = cursor_pos  
    if cursor_x - pixel_size <= x <= cursor_x and cursor_y - pixel_size <= y <= cursor_y:  
        return True  
    return False

def main_game_loop():
    cursor_pos = pygame.mouse.get_pos() 

    # Handle events  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()  
            sys.exit()  
 
    if check_collision_with_cursor(ball.rect.x, ball.rect.y, cursor_pos):  
        ball.speed_x *= -1  
        ball.speed_y *= -1
        player.teleport(cursor_pos[0], cursor_pos[1])  # Teleport the player to the cursor position

    # Update pixel position  
    ball.move(player)  # Move the ball and check for collisions with the player and walls
    player.teleport(cursor_pos[0], 400)  # Player doesn't move on its own, but we can keep this for future movement logic

    #Draw everything

    # Fill the background  
    screen.fill(background_color)  
  
    
    ball.draw(screen)  # Draw the ball on the screen
    player.draw(screen)  # Draw the player on the screen   
  
    # Update the display  
    pygame.display.flip()  
  
    # Limit the frame rate  
    clock.tick(60)


while True:
    main_game_loop()