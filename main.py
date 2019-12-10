import random
import pygame
from utils import *

pygame.font.init()

pygame.mixer.init()
pygame.mixer.music.load(BACKGROUND_MUSIC)

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = get_shape_repr(shape)
        self.color = get_shape_color(shape)
        self.rotation = 0
        
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2 , pos[1] - 4)
    
    return positions

def valid_space(piece, grid):
    accepted_pos = [(j, i) for j in range(10) for i in range(20) if grid[i][j] == BLACK]
    formatted = convert_shape_format(piece)

    return all(pos in accepted_pos or pos[1] < 0 for pos in formatted)

def check_lost(positions):
    return any(y < 1 for (x, y) in positions)

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):  
    pass
   
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y

    for i in range(row):
        pygame.draw.line(surface, GRAY, (sx, sy + i * BLOCK_SIZE), (sx + PLAY_WIDTH, sy + i * BLOCK_SIZE))
    for j in range(col):
        pygame.draw.line(surface, GRAY, (sx + j * BLOCK_SIZE, sy), (sx + j * BLOCK_SIZE, sy + PLAY_HEIGHT))

def clear_rows(grid, locked):
    pass

def draw_next_shape(shape, surface):
    pass

def redraw_window(surface, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
            (top_left_x + j * BLOCK_SIZE, 
            top_left_y + i * BLOCK_SIZE,
            BLOCK_SIZE, BLOCK_SIZE), 0)
    
    draw_grid(surface, PLAY_HEIGHT // BLOCK_SIZE, PLAY_WIDTH // BLOCK_SIZE)
    pygame.draw.rect(surface, RED, (top_left_x, top_left_y, PLAY_WIDTH, PLAY_HEIGHT), 4)
    pygame.display.update()

def main(win):
    pygame.mixer.music.play(MUSIC_PLAY_OPTION)
    win.fill(BLACK)
    font = pygame.font.SysFont("comicsans", 60)
    label = font.render(HEADING, 1, WHITE)
    win.blit(label, (top_left_x + PLAY_WIDTH/2 - label.get_width() / 2, BLOCK_SIZE))
    
    current_piece = get_shape()
    next_piece = get_shape()
    locked_positions = {} # (x, y) -> (255, 0, 0)
    
    clock = pygame.time.Clock()
    fall_time = 0
    change_piece = False

    run = True
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() 
        clock.tick()

        if fall_time/1000 > FALL_SPEED:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for (x,y) in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color
        
        if change_piece:
            for p in shape_pos:
                locked_positions[p] = current_piece.color
            
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            
        redraw_window(win, grid)

        if check_lost(locked_positions):
            run = False


if __name__ == "__main__":
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    main(window)
