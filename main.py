import pygame
import sys  
  
# Initialize Pygame  
pygame.init()  
  
# Set up the display  
screen_width, screen_height = 640, 480  
screen = pygame.display.set_mode((screen_width, screen_height))  
  
# Define colors  
white = (255, 255, 255)  
background_color = (0, 0, 0)  
  
# Set initial position and velocity of the pixel  
x, y = screen_width // 2, screen_height // 2  
speed_x, speed_y = 2, 2  
  
# Define the size of the pixel  
pixel_size = 8  
  
# Set up the clock for frame rate control  
clock = pygame.time.Clock()  

def check_collision_with_cursor(x, y, cursor_pos):  
    """Check if the pixel is within the cursor's area."""  
    cursor_x, cursor_y = cursor_pos  
    if cursor_x - pixel_size <= x <= cursor_x and cursor_y - pixel_size <= y <= cursor_y:  
        return True  
    return False

# Main game loop  
while True:  
    # Handle events  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()  
            sys.exit()  

    cursor_pos = pygame.mouse.get_pos()  
    if check_collision_with_cursor(x, y, cursor_pos):  
        speed_x *= -1  
        speed_y *= -1

    # Update pixel position  
    x += speed_x  
    y += speed_y  
  
    # Bounce the pixel off the edges of the screen  
    if x <= 0 or x + pixel_size >= screen_width:  
        speed_x *= -1  
    if y <= 0 or y + pixel_size >= screen_height:  
        speed_y *= -1  
  
    # Fill the background  
    screen.fill(background_color)  
  
    # Draw the pixel  
    screen.fill(white, (x, y, pixel_size, pixel_size))  
  
    # Update the display  
    pygame.display.flip()  
  
    # Limit the frame rate  
    clock.tick(60)
