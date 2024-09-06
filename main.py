import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Feed-the-cat")

#Load images
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (700, 450))  # Scale the image to fit the screen

cat_image = pygame.image.load('feedthecat1.png')
cat_image = pygame.transform.scale(cat_image, (80, 80))

mole_image_files = [f'feedthecat{i}.png' for i in range(1, 11)]  # Change the range to upload new images
mole_images = [pygame.image.load(file) for file in mole_image_files]
mole_images = [pygame.transform.scale(image, (80, 80)) for image in mole_images]

cursor_image_files = [f'cursor{i}.png' for i in range(1, 17)]  # Change the range to upload new images
cursor_images = [pygame.image.load(file) for file in cursor_image_files]
cursor_images = [pygame.transform.scale(image, (30, 30)) for image in cursor_images]
cursor_index = 0
cursor_image = cursor_images[cursor_index]
cursor_rect = cursor_image.get_rect()

# Set the cursor image as the system cursor
pygame.mouse.set_visible(False)

# Set up the font for the score
font1 = pygame.font.Font("PAC.TTF", 30)
font2 = pygame.font.Font("INVASION2000.TTF", 18)

# Set up the score
score = 0

# Set up the frame
frame_rect = pygame.Rect(50, 100, 700, 450)

# Set up the mole's initial position and state
mole_image = random.choice(mole_images)
mole_width, mole_height = mole_image.get_size()
mole_x = random.randint(frame_rect.left, frame_rect.right - mole_width)
mole_y = random.randint(frame_rect.top, frame_rect.bottom - mole_height)
mole_visible = False
mole_spawn_time = pygame.time.get_ticks()
mole_hide_time = 0

start_screen = True

while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_screen = False

    screen.fill((0, 0, 0))  # Fill the screen with black
    start_text = font1.render("Feed-the-cat", True, (255, 255, 255))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
    start_help = font2.render("Click to start the game.", True, (255, 255, 255))
    screen.blit(start_help, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2 + 50))
    screen.blit(cat_image, (WIDTH // 2 - start_text.get_width() // 2 - 100, HEIGHT // 2 - start_text.get_height() // 2 - 10))
    pygame.display.flip()
    pygame.time.Clock().tick(60)

#Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if player clicked on the mole
            if mole_visible and event.pos[0] > mole_x and event.pos[0] < mole_x + mole_width and event.pos[
                1] > mole_y and event.pos[1] < mole_y + mole_height:
                score += 1
                if score >= 100:
                    screen.fill((0, 0, 0))  # Fill the screen with black
                    you_won_text = font2.render("Meow-velous job! The cat is now officially stuffed!", True, (255, 255, 255))
                    screen.blit(you_won_text, (
                    WIDTH // 2 - you_won_text.get_width() // 2, HEIGHT // 2 - you_won_text.get_height() // 2))
                    x = WIDTH // 2 - (len(cursor_images) * (cursor_images[0].get_width() + 10)) // 2
                    y = HEIGHT // 2 + 50
                    for i, image in enumerate(cursor_images):
                        screen.blit(image, (x, y))
                        x += image.get_width() + 10
                        if x > WIDTH - image.get_width():
                            x = WIDTH // 2 - (len(cursor_images) * (cursor_images[0].get_width() + 10)) // 2
                            y += image.get_height() + 10
                    pygame.display.flip()
                    pygame.time.wait(6000)  # Wait for 2 seconds
                    pygame.quit()
                    quit()
                mole_visible = False
                mole_spawn_time = pygame.time.get_ticks()
                cursor_index = (cursor_index + 1) % len(cursor_images)  # Switch to the next cursor image
                cursor_image = cursor_images[cursor_index]  # Update the cursor image

    # Update the mole's state
    current_time = pygame.time.get_ticks()
    if not mole_visible and current_time - mole_spawn_time > max(500, 1000 - (score * 10)):
        mole_image = random.choice(mole_images)  # Choose a random image
        mole_x = random.randint(frame_rect.left, frame_rect.right - mole_width)
        mole_y = random.randint(frame_rect.top, frame_rect.bottom - mole_height)
        mole_visible = True
        mole_hide_time = current_time
    elif mole_visible and current_time - mole_hide_time > max(500, 1000 - (score * 10)):
        mole_visible = False
        mole_spawn_time = current_time

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 0), frame_rect, 2)  # Draw the frame
    screen.blit(background_image, (50, 100))  # Draw the background image

    # Draw the title and score outside the frame
    title_text = font1.render("FEED-THE-CAT", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))

    tagline_text = font2.render("Feed the cat, save the furniture!", True, (255, 255, 255))
    screen.blit(tagline_text, (WIDTH // 2 - tagline_text.get_width() // 2, 50))

    score_text = font2.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (50, 50))

    # Draw the moles inside the frame
    if mole_visible:
        screen.blit(mole_image, (mole_x, mole_y))

    # Draw the cursor image
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(cursor_image, (mouse_x, mouse_y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)