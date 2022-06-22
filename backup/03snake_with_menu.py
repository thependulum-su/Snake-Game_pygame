import pygame, sys, time, random
from pygame import mixer
speed = 10
# windows sizes
frame_size_x = 1380
frame_size_y = 840
check_errors = pygame.init()

if(check_errors[1] > 0):
    print("Error " + check_errors[1])
else:
    print("Game Succesfully initialized")

# initialise game window
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# colors
snake_color = (242, 242, 242)
food_color = (242, 183, 5)
white = (255, 255, 255)
bgcol = (38, 38, 38)
pause_bg = (21, 21, 21)
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

font = pygame.font.SysFont('Arial', 40)

fps_controller = pygame.time.Clock()

# one snake square size
square_size = 30
score = 0

def play_background_music():
    mixer.init()
    mixer.music.load('resources/music.mp3')
    mixer.music.play(-1)

def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, direction, running, gameover
    running = True
    gameover = False
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                random.randrange(1, (frame_size_y // square_size)) * square_size]
    food_spawn = True
    

def paused():
    if gameover == 0:  # fix the overlay into the gameover screen and pause
        mixer.music.pause()
        loop = 1
        game_window.fill(pause_bg)
        font_pause=pygame.font.SysFont('times new roman',80)
        pause_surface = font_pause.render('PAUSE', True, snake_color)
        pause_rect = pause_surface.get_rect()
        pause_rect.midtop = (frame_size_x/2, frame_size_y/2)
        game_window.blit(pause_surface, pause_rect)
        
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loop = 0
                        mixer.music.unpause()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            fps_controller.tick(60)

init_vars()

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
        
    game_window.blit(score_surface, score_rect)
play_background_music()

# game loop
while running:
    if not gameover:
        if direction == "UP":
            head_pos[1] -= square_size
        elif direction == "DOWN":
            head_pos[1] += square_size
        elif direction == "LEFT":
            head_pos[0] -= square_size
        else:
            head_pos[0] += square_size

        if head_pos[0] < 0:
            head_pos[0] = frame_size_x - square_size
        elif head_pos[0] > frame_size_x - square_size:
            head_pos[0] = 0
        elif head_pos[1] < 0:
            head_pos[1] = frame_size_y - square_size
        elif head_pos[1] > frame_size_y - square_size:
            head_pos[1] = 0

        # eating apple
        snake_body.insert(0, list(head_pos))
        if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # spawn food
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                        random.randrange(1, (frame_size_y // square_size)) * square_size]
            food_spawn = True

        # food and snake screen draw
        game_window.fill(bgcol)
        for pos in snake_body:
            pygame.draw.rect(game_window, snake_color, pygame.Rect(
                pos[0] + 2, pos[1] + 2, square_size - 2, square_size - 2))
        pygame.draw.rect(game_window, food_color, pygame.Rect(
            food_pos[0], food_pos[1], square_size, square_size))

        # game over condiditons
        for block in snake_body[1:]:
            if head_pos[0] == block[0] and head_pos[1] == block[1]:
                gameover = True
                mixer.music.stop()
        show_score(1, white, 'consolas', 20)
    else:
        show_score(0,red,'Arial', 40)
        option_surface = font.render('You lost! Press \'Q\' to quit, or Spacebar to play again', True, food_color)
        option_rect = option_surface.get_rect()
        option_rect.midtop = (frame_size_x/2, frame_size_y/2+200)
        game_window.blit(option_surface, option_rect)
        
    pygame.display.update()
    fps_controller.tick(speed)
    
    # Event Loop
    # Get the next events from the queue
    # For each event returned from get(),
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == ord("w")
                        and direction != "DOWN"):
                    direction = "UP"
                if (event.key == pygame.K_DOWN or event.key == ord("s")
                        and direction != "UP"):
                    direction = "DOWN"
                if (event.key == pygame.K_LEFT or event.key == ord("a")
                        and direction != "RIGHT"):
                    direction = "LEFT"
                if (event.key == pygame.K_RIGHT or event.key == ord("d")
                        and direction != "LEFT"):
                    direction = "RIGHT"
                if (event.key == pygame.K_ESCAPE):
                    mixer.music.pause()
                    paused()
                    
                if event.key == pygame.K_SPACE:
                    init_vars()
                if event.key == pygame.K_q:
                    running = False

