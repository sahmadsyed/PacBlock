import pygame, sys, random, math
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((800,700))
pygame.display.set_caption('Pacman 2')

FPS = 3
fpsClock = pygame.time.Clock()

GRID_HEIGHT = 650
GRID_WIDTH = 750

SQUARE_LENGTH = 50

BLACK = (0,0,0)
GREY = (205,201,201)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

MAIN_X = 400
MAIN_Y = 450
ENEMY_X = 500
ENEMY_Y = 450
SCORE = 0

PATH_BUILD_CHECK = False 
TOTAL_FOOD_COUNT = 0 

FRAME_COUNT = 0 

CURR_X = -1 
PREV_X = -1 
CURR_Y = -1 
PREV_Y = -1 

POS_DICT = {'first':False,'second':False,'third':False,'fourth':False} 
MOBILE = False 

def build_path(block_dict):
    path_dict = {0:[],
                 1:[],
                 2:[],
                 3:[],
                 4:[],
                 5:[],
                 6:[],
                 7:[],
                 8:[],
                 9:[],
                 10:[],
                 11:[],
                 12:[]}
    sixteen_list = range(16)
    for row in path_dict:
        for num in sixteen_list:
            if not(num in block_dict[row]):
                path_dict[row].append(num)
    return path_dict

def build_grid():
    for row in range(13):
        SCREEN_Y = row * SQUARE_LENGTH
        for col in range(16):
            SCREEN_X = col * SQUARE_LENGTH
            pygame.draw.rect(DISPLAYSURF, BLACK, (SCREEN_X,SCREEN_Y,SQUARE_LENGTH,SQUARE_LENGTH))
    SCORE_BOX_LENGTH = 800
    SCORE_BOX_WIDTH = SQUARE_LENGTH
    pygame.draw.rect(DISPLAYSURF, BLACK, (0,13*SCORE_BOX_WIDTH,SCORE_BOX_LENGTH,SCORE_BOX_WIDTH))
    pygame.draw.rect(DISPLAYSURF, GREY, (0,13*SCORE_BOX_WIDTH,SCORE_BOX_LENGTH,SCORE_BOX_WIDTH), 1)

def draw_food(PATH):
    for row in PATH:
        for column in PATH[row]:
            pygame.draw.circle(DISPLAYSURF,YELLOW,((column*SQUARE_LENGTH)+25,(row*SQUARE_LENGTH)+25),5)

def draw_blocks(BLOCKS):
    #13 rows, 16 columns
    for row in BLOCKS:
        for column in BLOCKS[row]:
            pygame.draw.rect(DISPLAYSURF, RED, (column*SQUARE_LENGTH,row*SQUARE_LENGTH,SQUARE_LENGTH,SQUARE_LENGTH))
            pygame.draw.rect(DISPLAYSURF, BLACK, (column*SQUARE_LENGTH,row*SQUARE_LENGTH,SQUARE_LENGTH,SQUARE_LENGTH),2)
			
def draw_main():
    pygame.draw.rect(DISPLAYSURF,YELLOW,(MAIN_X+5,MAIN_Y+5, SQUARE_LENGTH-10,SQUARE_LENGTH-10))
	
def draw_ghost():
    pygame.draw.rect(DISPLAYSURF,BLUE,(ENEMY_X+5,ENEMY_Y+5, SQUARE_LENGTH-10,SQUARE_LENGTH-10))

def draw_score_text(SCORE):
    broadway_obj = pygame.font.SysFont('broadway',30,bold=False,italic=False)
    score_text = broadway_obj.render('Score: %s' % str(SCORE), True, RED)
    text_rect_obj = score_text.get_rect()
    text_rect_obj.center = (400,670)
    DISPLAYSURF.blit(score_text,text_rect_obj)

def draw_game_win_text():	
    DISPLAYSURF.fill(BLACK)
    verdana_obj = pygame.font.SysFont('verdana', 120, bold = True, italic = False)
    lose_game_text = verdana_obj.render('YOU WIN', True, GREEN)
    text_rect_obj = lose_game_text.get_rect()
    text_rect_obj.center = (400,270)
    DISPLAYSURF.blit(lose_game_text,text_rect_obj)

def draw_game_lose_text(SCORE):	
    DISPLAYSURF.fill(BLACK)
    verdana_obj = pygame.font.SysFont('verdana', 110, bold = True, italic = False)
    lose_game_text = verdana_obj.render('YOU LOSE', True, GREEN)
    text_rect_obj = lose_game_text.get_rect()
    text_rect_obj.center = (400,270)
    DISPLAYSURF.blit(lose_game_text,text_rect_obj)
    
    verdana_obj = pygame.font.SysFont('verdana', 50, bold = True, italic = True)
    lose_game_text = verdana_obj.render('Score: %s' %str(SCORE), True, GREEN)
    text_rect_obj = lose_game_text.get_rect()
    text_rect_obj.center = (400,375)
    DISPLAYSURF.blit(lose_game_text,text_rect_obj)
	
def start_count_down(digit):
    verdana_obj = pygame.font.SysFont('verdana', 40, bold = True, italic = False)
    count_down_text = verdana_obj.render('Ghost Attack Countdown', True, GREEN)
    text_rect_obj = count_down_text.get_rect()
    text_rect_obj.center = (400,270)
    DISPLAYSURF.blit(count_down_text,text_rect_obj)
    
    verdana_obj = pygame.font.SysFont('verdana', 150, bold = True, italic = True)
    count_down_text = verdana_obj.render(str(digit), True, GREEN)
    text_rect_obj = count_down_text.get_rect()
    text_rect_obj.center = (400,375)
    DISPLAYSURF.blit(count_down_text,text_rect_obj)

def term_program():
    pygame.quit()
    sys.exit()

def lose_game_check():
    return MAIN_X == ENEMY_X and MAIN_Y == ENEMY_Y

def win_game_check():
    return SCORE == 6050
        
def cover_tracks(X,Y):
    pygame.draw.rect(DISPLAYSURF,BLACK,(X,Y, SQUARE_LENGTH,SQUARE_LENGTH))

def empty_spot_check_main(BLOCKS):
    return ((MAIN_X/SQUARE_LENGTH) in BLOCKS[MAIN_Y/SQUARE_LENGTH])

def empty_spot_check_ghost(BLOCKS):
    return ((ENEMY_X/SQUARE_LENGTH) in BLOCKS[ENEMY_Y/SQUARE_LENGTH])
 
while True:
        build_grid()
        
        BLOCKS = {0:[],
                          1:[1,2,4,5,6,8,9,10,11,13,14],
                          2:[1,2,8,9,10,11,13,14],
                          3:[4,5,6],
                          4:[1,2,4,5,6,8,9,11,13,14],
                          5:[1,2,4,5,6,8,9,11,13,14],
                          6:[1,2],
                          7:[1,2,4,5,6,8,9,10,11,13,14],
                          8:[1,2,4,5,6,8,9,10,11,13,14],
                          9:[],
                          10:[1,2,4,5,6,8,10,11,13,14],
                          11:[1,2,4,5,6,8,10,11,13,14],
                          12:[]}

        if PATH_BUILD_CHECK == False:
                PATH = build_path(BLOCKS)
                PATH[9].remove(8)
                PATH_BUILD_CHECK = True
                for food in PATH:
                        TOTAL_FOOD_COUNT = TOTAL_FOOD_COUNT + len(PATH[food])
                
        draw_food(PATH)                        
        draw_blocks(BLOCKS)
        draw_main()
        draw_ghost()
        draw_score_text(SCORE)    
        
        if FRAME_COUNT < 5:
                start_count_down(5-FRAME_COUNT)
        
        PLAYER_MOVE = False
        for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        term_program()
                if event.type == KEYDOWN:
                        if event.key == K_UP:
                                PLAYER_MOVE = True
                                cover_tracks(MAIN_X,MAIN_Y)
                           
                                MAIN_Y = MAIN_Y - SQUARE_LENGTH
                                if MAIN_Y < 0 or empty_spot_check_main(BLOCKS):
                                        MAIN_Y = MAIN_Y + SQUARE_LENGTH
                        elif event.key == K_DOWN:
                                PLAYER_MOVE = True
                                cover_tracks(MAIN_X,MAIN_Y)
                           
                                MAIN_Y = MAIN_Y + SQUARE_LENGTH
                                if MAIN_Y > 600 or empty_spot_check_main(BLOCKS):
                                        MAIN_Y = MAIN_Y - SQUARE_LENGTH
                        elif event.key == K_RIGHT:
                                PLAYER_MOVE = True
                                cover_tracks(MAIN_X,MAIN_Y)
                           
                                MAIN_X = MAIN_X + SQUARE_LENGTH
                                if MAIN_X > GRID_WIDTH or empty_spot_check_main(BLOCKS):
                                        MAIN_X = MAIN_X - SQUARE_LENGTH
                        elif event.key == K_LEFT:
                                PLAYER_MOVE = True
                                cover_tracks(MAIN_X,MAIN_Y)
                                
                                MAIN_X = MAIN_X - SQUARE_LENGTH
                                if MAIN_X < 0 or empty_spot_check_main(BLOCKS):
                                        MAIN_X = MAIN_X + SQUARE_LENGTH
                                        
                        if PLAYER_MOVE == True:
                                draw_main()
                                if int(MAIN_X/SQUARE_LENGTH) in PATH[MAIN_Y/SQUARE_LENGTH]:
                                        PATH[MAIN_Y/SQUARE_LENGTH].remove(int(MAIN_X/SQUARE_LENGTH))
                                        TOTAL_FOOD_COUNT = TOTAL_FOOD_COUNT - 1
                                        SCORE = SCORE + 50
                  
        FRAME_COUNT = FRAME_COUNT + 1
        if FRAME_COUNT >=7:
                PREV_X = CURR_X
                CURR_X = MAIN_X
                PREV_Y = CURR_Y
                CURR_Y = MAIN_Y
                if CURR_X == PREV_X and CURR_Y == PREV_Y and MOBILE == True:
                        cover_tracks(ENEMY_X,ENEMY_Y)
                        if POS_DICT['first'] == True:
                                ENEMY_X = ENEMY_X + SQUARE_LENGTH
                                if not(empty_spot_check_ghost(BLOCKS)) and ENEMY_X < GRID_WIDTH:
                                        MOBILE = False
                                else:
                                        ENEMY_X = ENEMY_X - SQUARE_LENGTH
                                        ENEMY_Y = ENEMY_Y + SQUARE_LENGTH
                        elif POS_DICT['second'] == True:
                                ENEMY_X = ENEMY_X - SQUARE_LENGTH
                                if not(empty_spot_check_ghost(BLOCKS)) and ENEMY_X > 0:
                                        MOBILE = False
                                else:
                                        ENEMY_X = ENEMY_X + SQUARE_LENGTH
                                        ENEMY_Y = ENEMY_Y + SQUARE_LENGTH
                        elif POS_DICT['third'] == True:
                                ENEMY_Y = ENEMY_Y + SQUARE_LENGTH
                                if not(empty_spot_check_ghost(BLOCKS)) and ENEMY_Y < GRID_HEIGHT:
                                        MOBILE = False
                                else:
                                        ENEMY_Y = ENEMY_Y - SQUARE_LENGTH
                                        ENEMY_X = ENEMY_X + SQUARE_LENGTH
                        elif POS_DICT['fourth'] == True:
                                ENEMY_Y = ENEMY_Y - SQUARE_LENGTH
                                if not(empty_spot_check_ghost(BLOCKS)) and ENEMY_Y > 0:
                                        MOBILE = False
                                else:
                                        ENEMY_Y = ENEMY_Y + SQUARE_LENGTH
                                        ENEMY_X = ENEMY_X + SQUARE_LENGTH    
                        draw_ghost()
                else:
                        if MAIN_Y == ENEMY_Y:
                                cover_tracks(ENEMY_X,ENEMY_Y)             
                                if MAIN_X > ENEMY_X:
                                        for pos in POS_DICT:
                                                POS_DICT[pos] = False
                                        POS_DICT['first'] = True
                                        ENEMY_X = ENEMY_X + SQUARE_LENGTH
                                        if empty_spot_check_ghost(BLOCKS) or ENEMY_X > GRID_WIDTH:
                                                ENEMY_X = ENEMY_X - SQUARE_LENGTH
                                                MOBILE = True     
                                elif MAIN_X < ENEMY_X:
                                        for pos in POS_DICT:
                                                POS_DICT[pos] = False
                                        POS_DICT['second'] = True
                                        ENEMY_X = ENEMY_X - SQUARE_LENGTH
                                        if empty_spot_check_ghost(BLOCKS) or ENEMY_X < 0:
                                                ENEMY_X = ENEMY_X + SQUARE_LENGTH
                                                MOBILE = True
                                draw_ghost()
                        elif MAIN_X == ENEMY_X:
                                cover_tracks(ENEMY_X,ENEMY_Y)              
                                if MAIN_Y > ENEMY_Y:
                                        for pos in POS_DICT:
                                                POS_DICT[pos] = False
                                        POS_DICT['third'] = True
                                        ENEMY_Y = ENEMY_Y + SQUARE_LENGTH
                                        if empty_spot_check_ghost(BLOCKS) or ENEMY_Y > GRID_HEIGHT:
                                                ENEMY_Y = ENEMY_Y - SQUARE_LENGTH
                                                MOBILE = True           
                                elif MAIN_Y < ENEMY_Y:
                                        for pos in POS_DICT:
                                                POS_DICT[pos] = False
                                        POS_DICT['fourth'] = True
                                        ENEMY_Y = ENEMY_Y - SQUARE_LENGTH
                                        if empty_spot_check_ghost(BLOCKS) or ENEMY_Y < 0:
                                                ENEMY_Y = ENEMY_Y + SQUARE_LENGTH
                                                MOBILE = True
                                draw_ghost()
                        else:
                                MOVE = True
                                cover_tracks(ENEMY_X,ENEMY_Y)
                                if (MAIN_X - ENEMY_X) > 0:
                                        ENEMY_X = ENEMY_X + SQUARE_LENGTH
                                        if empty_spot_check_ghost(BLOCKS) or ENEMY_X > GRID_WIDTH:
                                                ENEMY_X = ENEMY_X - SQUARE_LENGTH
                                        else:
                                                MOVE = False
                                elif (MAIN_X - ENEMY_X) < 0:
                                        ENEMY_X = ENEMY_X - SQUARE_LENGTH
                                        if empty_spot_check_ghost(BLOCKS) or ENEMY_X < 0:
                                                ENEMY_X = ENEMY_X + SQUARE_LENGTH
                                        else:
                                                MOVE = False
                                if MOVE == True:
                                        if (MAIN_Y - ENEMY_Y) > 0:
                                                ENEMY_Y = ENEMY_Y + SQUARE_LENGTH
                                                if empty_spot_check_ghost(BLOCKS) or ENEMY_Y > GRID_HEIGHT:
                                                        ENEMY_Y = ENEMY_Y - SQUARE_LENGTH

                                        elif (MAIN_Y - ENEMY_Y) < 0:
                                                ENEMY_Y = ENEMY_Y - SQUARE_LENGTH
                                                if empty_spot_check_ghost(BLOCKS) or ENEMY_Y < 0:
                                                        ENEMY_Y = ENEMY_Y + SQUARE_LENGTH     
                                        MOVE = False
                                draw_ghost()
        pygame.display.update()
        fpsClock.tick(FPS)
        if win_game_check():
                draw_game_win_text()
                pygame.display.update()
                fpsClock.tick(FPS)
                break  
        if lose_game_check():
                draw_game_lose_text(SCORE)
                pygame.display.update()
                fpsClock.tick(FPS)
                break    
                
while True:
        for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        term_program()





