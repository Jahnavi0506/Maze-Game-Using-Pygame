import pygame
import random
import time
from sys import exit
import numpy as np

pygame.init()

screen=pygame.display.set_mode((600,400))
pygame.display.set_caption("Maze Game")
clock=pygame.time.Clock()
test_font=pygame.font.Font(None,50)
test_font1=pygame.font.Font(None,30)

Gray = (50, 50, 50)
White = (255, 255, 255)
Black= (0, 0, 0)
Green=(34, 139, 34)

Directions = [(0, -1), (-1, 0), (0, 1),(1, 0)]
obstacles = []  
obstacle_toggle_time = 1500
obstacle_visible = True
last_toggle_time = pygame.time.get_ticks()

difficulty_levels={
    'Easy':10,  #10*10
    'Medium':20, #20*20
    'Hard':30    #30*30
    }
start_time=0

def draw_text(text,x,y,size=50,color=(255, 255, 255)):
    test_font=pygame.font.Font(None,size)
    label=test_font.render(text,True,White)
    screen.blit(label,(x,y))
def design():
    pygame.draw.rect(screen, (255, 255, 255), screen.get_rect(), width=8)
    blob = pygame.Surface((150, 150), pygame.SRCALPHA)

    pygame.draw.circle(blob, (0, 255, 100, 40), (75, 75), 75)
    screen.blit(blob, (50, 100))
    screen.blit(blob, (500, 200))
    corner = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(corner, (255, 255, 255, 40), (0, 0), 80)
    screen.blit(corner, (0, 0))
    screen.blit(corner, (screen.get_width()-100, 0))
    screen.blit(corner, (0, screen.get_height()-100))
    screen.blit(corner, (screen.get_width()-100, screen.get_height()-100))    

def display_score():
    current_time=int(pygame.time.get_ticks()/500)-start_time
    score_surface=test_font.render(f'Score: {current_time}',False,(34, 139, 34))
    score_rect=score_surface.get_rect(center=(500,100))
    pygame.draw.rect(screen, Gray, score_rect)
    screen.blit(score_surface,score_rect)
    return current_time
def start_screen():
    while True:
        screen.fill(Gray)
        draw_text("Welcome To",150,100,size=60)
        draw_text("MAZE GAME",200,150,size=70)
        proceed=pygame.draw.rect(screen,(34, 139, 34),(350, 350, 250, 50))
        draw_text("Continue....",350,350,size=50)
        design()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=event.pos
                if proceed.collidepoint(x, y):  
                   return

def players():
    while True:
        screen.fill(Black)
        draw_text("SELECT NO OF PLAYERS", 100, 50)
        design()

        one_rect = pygame.draw.rect(screen, (34, 139, 34), (200, 150, 200, 50), border_radius=10)
        two_rect = pygame.draw.rect(screen, (34, 139, 34), (200, 250, 200, 50), border_radius=10)

        draw_text("1 Player", 250, 160, 40)
        draw_text("2 players", 240, 260, 40)

        pygame.draw.rect(screen, (255, 255, 255), one_rect, width=4, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), two_rect, width=4, border_radius=10)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if one_rect.collidepoint(x, y):
                    return 1
                elif two_rect.collidepoint(x, y):
                    return 2

def difficulty_selection():
    global start_time
    while True:
        screen.fill(Black)
        design()

        draw_text("SELECT DIFFICULTY", 130, 50)  

        easy_rect = pygame.draw.rect(screen, (34, 139, 34), (200, 120, 200, 50), border_radius=10)
        medium_rect = pygame.draw.rect(screen, (34, 139, 34), (200, 190, 200, 50), border_radius=10)
        hard_rect = pygame.draw.rect(screen, (34, 139, 34), (200, 260, 200, 50), border_radius=10)

        pygame.draw.rect(screen, (255, 255, 255), easy_rect, width=4, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), medium_rect, width=4, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), hard_rect, width=4, border_radius=10)

        draw_text("Easy", 270, 130)
        draw_text("Medium", 250, 200)
        draw_text("Hard", 270, 270)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if easy_rect.collidepoint(x,y):  
                    start_time = int(pygame.time.get_ticks() / 500)
                    return difficulty_levels['Easy']
                elif medium_rect.collidepoint(x,y):  
                    start_time = int(pygame.time.get_ticks() / 500)
                    return difficulty_levels['Medium']
                elif hard_rect.collidepoint(x,y):  
                    start_time = int(pygame.time.get_ticks() / 500)
                    return difficulty_levels['Hard']
        
        
def generate_maze(rows,cols):
    stack=[]
    visited=set()
    maze = np.zeros((rows,cols),dtype='int')
    maze[1][1]=1
    x,y=1,1
    stack.append((x,y))
    visited.add((x,y))
    maze[y][x] = 1
    while stack:
        neighbours=[]
        x,y=stack[-1]
        for dx,dy in Directions:
            nx, ny = x + dx * 2, y + dy * 2
            
            if (nx,ny) not in visited and 0<=nx<cols and 0<=ny<rows:
                neighbours.append((nx,ny,dx,dy))

        if neighbours:
            nx, ny,dx,dy = random.choice(neighbours)
            maze[y + dy][x + dx] = 1  
            maze[ny][nx] = 1 
            visited.add((nx, ny))  
            stack.append((nx, ny))  
        else:
            stack.pop()
    return maze

def generate_obstacles(maze, num_obstacles):
    rows, cols = maze.shape
    possible_positions = [(x, y) for y in range(rows) for x in range(cols)
                          if maze[y][x] == 1 and (x, y) != (1, 1) and (x, y) != (cols-1, rows-1)]
    random.shuffle(possible_positions)
    return possible_positions[:num_obstacles]
            
def draw_maze(maze,cell_size,px,py,path,obstacles,obstacle_visible):

    rows,cols=maze.shape
    for y in range(rows):
        for x in range(cols):
            if maze[y][x]==0:
                pygame.draw.rect(screen,(34, 139, 34),(x*cell_size,y*cell_size,cell_size,cell_size))
                pygame.draw.rect(screen, (0, 0, 0),(x * cell_size+2 , y * cell_size+2 , cell_size-5 , cell_size-5))

            else:
                pygame.draw.rect(screen,White,(x*cell_size,y*cell_size,cell_size,cell_size))

    exit_x, exit_y = (cols-1)*cell_size, (rows-1)*cell_size
    pygame.draw.rect(screen, (255, 255, 0), (exit_x , exit_y , cell_size, cell_size))

    if len(path) > 1:
        pygame.draw.lines(screen, "Blue", False, [(x * cell_size + cell_size//2 , y * cell_size + cell_size//2) for x, y in path], 3)
    if obstacle_visible:
        for ox, oy in obstacles:
            
            pygame.draw.rect(screen, (255, 0, 0), (ox * cell_size, oy * cell_size, cell_size, cell_size))

    pygame.draw.circle(screen,"Blue",(int(px*cell_size+ cell_size / 2),int(py * cell_size + cell_size / 2)),cell_size/4)      
    pause_rect=pygame.Rect(430,150,140,40)
    pygame.draw.rect(screen,(0,100,0),pause_rect,border_radius=10)
    draw_text("Pause", 465, 155, 40, color=(34, 139, 34))
    design()
    return pause_rect

def show_collision_screen():
    while True:
        screen.fill((0, 0, 0))
        draw_text("You collided with an obstacle!", 120, 150, 40, color=(255, 0, 0))

        replay_rect = pygame.Rect(240, 200, 140, 40)
        exit_rect = pygame.Rect(260, 300, 100, 40)
        pygame.draw.rect(screen, (0, 128, 0), replay_rect, border_radius=10)
        pygame.draw.rect(screen, (128, 0, 0), exit_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), replay_rect, width=5, border_radius=10)  
        pygame.draw.rect(screen, (255, 255, 255), exit_rect, width=5, border_radius=10) 
        draw_text("Restart", 260, 210, 40)
        draw_text("Exit", 280, 310, 40)
        design()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.collidepoint(event.pos):
                    main()  
                    return
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def show_player_fail_screen(player_num):
    while True:
        screen.fill((0, 0, 0))
        draw_text(f"Player {player_num} collided!", 150, 150, 40, color=(255, 0, 0))
        draw_text(f"Player {player_num} fails!", 170, 200, 40, color=(255, 0, 0))

        continue_rect = pygame.Rect(200, 300, 200, 50)
        pygame.draw.rect(screen, (0, 128, 0), continue_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), continue_rect, width=5, border_radius=10)
        draw_text("Continue", 240, 310, 40)
        design()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_rect.collidepoint(event.pos):
                    return

def show_both_fail_screen():
    while True:
        screen.fill((0, 0, 0))
        draw_text("Both players collided!", 120, 150, 40, color=(255, 0, 0))
        draw_text("Game Over!", 200, 200, 40, color=(255, 0, 0))

        replay_rect = pygame.Rect(200, 300, 200, 50)
        pygame.draw.rect(screen, (0, 128, 0), replay_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), replay_rect, width=5, border_radius=10)
        draw_text("Replay", 250, 310, 40)
        design()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.collidepoint(event.pos):
                    main()
                    return

def play_turn(turn, maze, cell_size, rows, cols):
    global start_time, obstacle_visible, last_toggle_time, obstacles

    px, py = 1, 1
    path = [(px, py)]
    start_time = int(pygame.time.get_ticks() / 500)
    movement = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0)
    }

    running = True

    while running:
        screen.fill(Gray)
        pause_rect = draw_maze(maze, cell_size, px, py, path, obstacles, obstacle_visible)
        draw_text(f"Player '{turn}'", 450, 30, 40)
        display_score()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key in movement:
                dx, dy = movement[event.key]
                newx, newy = px + dx, py + dy
                if 0 <= newx < cols and 0 <= newy < rows and maze[newy][newx] == 1:
                    px, py = newx, newy
                    path.append((px, py))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    pause_menu()

        current_time = pygame.time.get_ticks()
        if current_time - last_toggle_time >= obstacle_toggle_time:
            obstacle_visible = not obstacle_visible
            last_toggle_time = current_time

        if obstacle_visible and (px, py) in obstacles:
            return "collision"  

        if (px, py) == (cols - 1, rows - 1):
            scores[turn] = int(pygame.time.get_ticks() / 500) - start_time
            return "success"  

        clock.tick(60)
  

def show_results(player1_score, player2_score):
    global rows,cols,running
    maze = generate_maze(rows, cols)
    screen.fill((94, 150, 120))
    design()
    pygame.draw.rect(screen, (255, 255, 255), screen.get_rect(), width=6, border_radius=25)

    draw_text("Congratulations", 180, 20, 40)

    draw_text(f'Player 1 Score: {player1_score}', 200, 200, 30)
    draw_text(f'Player 2 Score: {player2_score}', 200, 230, 30)

    if scores[1] < scores[2]:
        draw_text("Player 1 Wins", 200, 260, 40, color=(0, 0, 0))
    elif scores[2] < scores[1]:
        draw_text("Player 2 Wins", 200, 260, 40, color=(0, 0, 0))
    else:
        draw_text("It is a Tie", 220, 260, 40, color=(0, 0, 0))

    draw_text('Press R to Replay', 200, 300, 30)
    draw_text('Press B to go Back', 200, 350, 30)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "replay"
                    
                elif event.key == pygame.K_b:
                    waiting = False
                    return "back"

def replay_game(rows,cols):
    global px, py ,start_time, maze,path
    rows=cols
    cell_size=400//cols
    px, py = 1, 1
    path = [(px, py)]    
    maze = generate_maze(rows, cols)
    start_time = int(pygame.time.get_ticks() / 500)

def restart_game():
    global rows, cols, maze, cell_size
    rows = difficulty_selection()
    cols = rows
    cell_size = 400 // cols
    maze = generate_maze(rows, cols)

def pause_menu():
    global start_time
    paused_time=pygame.time.get_ticks()  

    while True:
        screen.fill((50, 50, 50))
        design()
        draw_text("PAUSED", 230, 150, size=50)
        resume_button = pygame.draw.rect(screen, (34, 139, 34), (200, 250, 200, 50),border_radius=10)
        draw_text("Resume", 240, 260, size=40)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if resume_button.collidepoint(x, y):
                    resumed_time = pygame.time.get_ticks()
                    paused_duration = (resumed_time - paused_time) // 500
                    start_time += paused_duration  
                    return


def main():
    global player_turn, scores, rows, cols, obstacles, obstacle_visible
    while True:
        start_screen()
        num_players = players()

        while True:
            scores = {}
            screen.fill(Gray)
            rows = difficulty_selection()
            cols = rows
            cell_size = 400 // cols
            maze = generate_maze(rows, cols)
        
            if rows == 10:  
                difficulty = "Easy"
                num_obstacles = 7
            elif rows == 20:  
                difficulty = "Medium"
                num_obstacles = 14
            elif rows == 30:  
                difficulty = "Hard"
                num_obstacles = 21
            else:
                difficulty = "Easy"
                num_obstacles = 7

            obstacles = generate_obstacles(maze, num_obstacles)

            player_turn = 1
            result1 = play_turn(player_turn, maze, cell_size, rows, cols)

            if num_players == 1:
                if result1 == "collision":
                    show_collision_screen()
                    continue
                else:
                    screen.fill((94, 150, 120))
                    design()

                    draw_text("Game Over!", 200, 60, 50)
                    draw_text(f"Your Time: {scores[1]}", 200, 200, 40)
                    draw_text("Congratulations", 200, 20, 40)

                    draw_text('Press R to Replay', 200, 300, 30)
                    draw_text('Press B to go Back', 200, 350, 30)

                    pygame.display.update()

                    waiting = True
                    result = None  
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:
                                    result = "replay"
                                    waiting = False
                                elif event.key == pygame.K_b:
                                    result = "back"
                                    waiting = False

                    if result == "replay":
                        continue  
                    elif result == "back":
                        break  
                    else:
                        pygame.quit()
                        exit()

            else:  
                if result1 == "collision":
                    show_player_fail_screen(1)
                    player_turn = 2
                    result2 = play_turn(player_turn, maze, cell_size, rows, cols)
                    
                    if result2 == "collision":
                        show_both_fail_screen()
                        continue
                    else:
                        scores[1] = float('inf')  
                        show_results(scores[1], scores[2])
                else:
    
                    play_button_clicked = False
                    while not play_button_clicked:
                        screen.fill(Gray)
                        design()
                        pygame.draw.rect(screen, (255, 255, 255), screen.get_rect(), width=8)
                        pygame.draw.rect(screen, (255, 255, 255), screen.get_rect(), width=8, border_radius=20)
                        draw_text("Player 1 Finished!", 170, 120, 40)
                        draw_text(f"Time: {scores[1]}", 230, 170, 40)
                        play_button = pygame.Rect(200, 250, 200, 50)
                        pygame.draw.rect(screen, (34, 139, 34), play_button, border_radius=20)
                        draw_text("Player 2 Turn", 215, 260, 35)
                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if play_button.collidepoint(event.pos):
                                    play_button_clicked = True

                    player_turn = 2
                    result2 = play_turn(player_turn, maze, cell_size, rows, cols)
                    
                    if result2 == "collision":
                        show_player_fail_screen(2)
                        scores[2] = float('inf')  
                    else:
                        continue_clicked = False
                        while not continue_clicked:
                            screen.fill(Gray)
                            design()
                            pygame.draw.rect(screen, (255, 255, 255), screen.get_rect(), width=8)
                            draw_text("Player 2 Finished!", 170, 120, 40)
                            draw_text(f"Time: {scores[2]}", 230, 170, 40)
                            continue_button = pygame.Rect(200, 250, 200, 50)
                            pygame.draw.rect(screen, (34, 139, 34), continue_button, border_radius=10)
                            draw_text("Continue", 240, 260, 35)
                            design()
                            pygame.display.update()

                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    if continue_button.collidepoint(event.pos):
                                        continue_clicked = True

                    result = show_results(scores.get(1, float('inf')), scores.get(2, float('inf')))
                    if result == "replay":
                        replay_game(rows, cols)
                        continue  
                    elif result == "back":
                        break  
                    else:
                        pygame.quit()
                        exit()
                        
main()
pytho