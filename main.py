import pygame
import requests
import time

def solve(bo):
    tmp = [[bo[x][y] for y in range(len(bo[0]))] for x in range(len(bo))]
    find = find_empty(tmp)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(tmp, i, (row, col)):
            tmp[row][col] = i

            if solve(tmp):
                return True

            tmp[row][col] = 0

    return False


def solve2(bo, win, sketch_board, original_board, err, level):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        draw_board(win, bo, sketch_board, original_board, err, level)
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve2(bo, win, sketch_board, original_board, err, level):
                return True

            bo[row][col] = 0
    draw_board(win, bo, sketch_board, original_board, err, level)
    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


WIDTH = 800
background_color = (44,44,44)
sketch_color = (150,150,150)
element_color = (230,230,230)
buffer = 5


def get_board(level=1):
    if level == 1:
        level = "easy"
    elif level == 2:
        level = "medium"
    elif level == 3:
        level = "hard"

    link ="https://sugoku.onrender.com/board?difficulty=" + level
    response = requests.get(link)
    board = response.json()['board']
    original_board = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
    sketch_board = [[original_board[x][y] for y in range(len(original_board[0]))] for x in range(len(original_board))]
    return board, original_board, sketch_board


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_board(win, board, sketch_board, original_board, err, level=1):
    mainFont = pygame.font.SysFont('roboto', 40)
    sketchFont = pygame.font.SysFont('roboto', 30)
    gameStartFont = pygame.font.SysFont('roboto', 27)
    green = (50, 205, 50)
    red = (255, 0, 0)

    # DRAW LINES
    win.fill(background_color)
    for i in range(10):
        if i % 3 == 0:
            width = 5
        else:
            width = 2

        pygame.draw.line(win, (212,175,55), (50 + 50*i, 50), (50 + 50*i, 500), width)
        pygame.draw.line(win, (212,175,55), (48, 50 + 50*i), (502, 50 + 50*i), width)

    # FILL BOARD
    for i in range(9):
        for j in range(9):
            if 0 < board[i][j] < 10 and original_board[i][j] == 0 and board[i][j] != original_board[i][j]:
                value = mainFont.render(str(board[i][j]), True, green)
                win.blit(value, ((j + 1) * 50 + 18, (i + 1) * 50 + 15))
            elif 0 < board[i][j] < 10:
                value = mainFont.render(str(board[i][j]), True, element_color)
                win.blit(value, ((j + 1) * 50 + 18, (i + 1) * 50 + 15))

            if board[i][j] == 0 and 0 < sketch_board[i][j] < 10:
                value = sketchFont.render(str(sketch_board[i][j]), True, sketch_color)
                win.blit(value, ((j + 1) * 50 + 5, (i + 1) * 50 + 5))

    # DRAW ERRORS
    for i in range(err):
        value = mainFont.render("X", True, red)
        win.blit(value, (12, 60 + 50*i))

    draw_rect_alpha(win, (212,175,55, 70), (550, 100, 200, 30))
    pygame.draw.rect(win, (212,175,55), (550, 100, 200, 30), 2)
    value = gameStartFont.render("        DIFFICULTY", True, (1,1,1))
    win.blit(value, (556, 106))

    # DRAW SELECT DIFFICULTY
    if level == 1:
        draw_rect_alpha(win, (212, 175, 55, 190), (550, 130, 67, 25))
        draw_rect_alpha(win, (212, 175, 55, 70), (617, 130, 67, 25))
        draw_rect_alpha(win, (212, 175, 55, 70), (684, 130, 66, 25))

    elif level == 2:
        draw_rect_alpha(win, (212, 175, 55, 70), (550, 130, 67, 25))
        draw_rect_alpha(win, (212, 175, 55, 190), (617, 130, 67, 25))
        draw_rect_alpha(win, (212, 175, 55, 70), (684, 130, 66, 25))

    elif level == 3:
        draw_rect_alpha(win, (212, 175, 55, 70), (550, 130, 67, 25))
        draw_rect_alpha(win, (212, 175, 55, 70), (617, 130, 67, 25))
        draw_rect_alpha(win, (212, 175, 55, 190), (684, 130, 66, 25))

    pygame.draw.rect(win, (212, 175, 55), (550, 130, 67, 25), 2)
    value = gameStartFont.render("  easy", True, (1, 1, 1))
    win.blit(value, (554, 134))

    pygame.draw.rect(win, (212, 175, 55), (617, 130, 67, 25), 2)
    value = gameStartFont.render("   mid", True, (1, 1, 1))
    win.blit(value, (621, 134))

    pygame.draw.rect(win, (212, 175, 55), (684, 130, 66, 25), 2)
    value = gameStartFont.render("  hard", True, (1, 1, 1))
    win.blit(value, (688, 134))

    draw_rect_alpha(win, (212, 175, 55, 70), (625, 170, 50, 30))
    pygame.draw.rect(win, (212, 175, 55), (625, 170, 50, 30), 2)
    value = gameStartFont.render(" OK", True, (1, 1, 1))
    win.blit(value, (631, 176))

    value = gameStartFont.render("  GENERATE SUDOKU", True, (212, 175, 55))
    win.blit(value, (545, 70))

    draw_rect_alpha(win, (255, 0, 0, 70), (575, 250, 150, 60))
    pygame.draw.rect(win, red, (575, 250, 150, 60), 2)
    value = mainFont.render("SOLVE  ", True, (1, 1, 1))
    win.blit(value, (606, 267))

    pygame.display.update()


def format_time(win, secs, zeros=0):
    sec = secs % 60
    minute = secs//60
    hour = minute//60

    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)

    if sec < 10:
        sec = "0" + str(sec)
    else:
        sec = str(sec)

    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)

    mat = " " + hour + ":" + minute + ":" + sec

    # Draw time
    draw_rect_alpha(win, (44,
                          44, 44, 255), (540-160, 560, 400, 100))
    fnt = pygame.font.SysFont("roboto", 40)
    if zeros >= 0:
        text = fnt.render("Time: " + mat, True, (0, 0, 0))
    if zeros < 0:
        text = fnt.render("Time: " + mat, True, (50, 205, 50))
    win.blit(text, (540 - 160, 560))

    pygame.display.update()


def insert(win, position, board, original_board, sketch_board, err, level, start):
    i,j = position[1], position[0]
    mainFont = pygame.font.SysFont('roboto', 30)
    while True:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                i, j = pos[1], pos[0]
                draw_board(win, board, sketch_board, original_board, err, level)
                pygame.draw.rect(win, (230, 230, 230), (j * 50, i * 50, 50, 50), 4)
                pygame.display.update()
                return err

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                if valid(board, sketch_board[i - 1][j - 1], (i - 1, j - 1)):
                    board[i - 1][j - 1] = sketch_board[i - 1][j - 1]
                    if solve(board):
                        draw_board(win, board, sketch_board, original_board, err, level)
                        pygame.display.update()
                        return err
                    else:
                        err += 1
                        board[i - 1][j - 1] = 0
                        sketch_board[i - 1][j - 1] = 0
                        draw_board(win, board, sketch_board, original_board, err, level)
                        pygame.display.update()
                        return err
                else:
                    err += 1
                    sketch_board[i - 1][j - 1] = 0
                    draw_board(win, board, sketch_board, original_board, err, level)
                    pygame.display.update()
                    return err

            if event.type == pygame.QUIT:
                pygame.quit()
                return err
            if event.type == pygame.KEYDOWN:
                if original_board[i-1][j-1] != 0:
                    return err

                if event.key == 8 : #checking with backspace
                    sketch_board[i-1][j-1] = 0
                    draw_board(win, board, sketch_board, original_board, err, level)
                    pygame.draw.rect(win, (230, 230, 230), (j * 50, i * 50, 50, 50), 4)
                    pygame.display.update()

                if 0 < event.key - 48 <10:  #We are checking for valid input
                    sketch_board[i-1][j-1] = event.key - 48
                    draw_board(win, board, sketch_board, original_board, err, level)
                    pygame.draw.rect(win, (230, 230, 230), (j * 50, i * 50, 50, 50), 4)
                    pygame.display.update()

                if event.key == 27: #checking with esc
                    draw_board(win, board, sketch_board, original_board, err, level)
                    return err

                if event.key == 13 and 0 < sketch_board[i - 1][j - 1] < 10:
                    if valid(board, sketch_board[i - 1][j - 1], (i-1,j-1)):
                        board[i - 1][j - 1] = sketch_board[i - 1][j - 1]
                        if solve(board):
                            draw_board(win, board, sketch_board, original_board, err, level)
                            pygame.display.update()
                            return err
                        else:
                            err += 1
                            board[i - 1][j - 1] = 0
                            sketch_board[i-1][j-1] = 0
                            draw_board(win, board, sketch_board, original_board, err, level)
                            pygame.display.update()
                            return err
                    else:
                        err += 1
                        sketch_board[i - 1][j - 1] = 0
                        draw_board(win, board, sketch_board, original_board, err, level)
                        pygame.display.update()
                        return err

        format_time(win, play_time)


def main():
    lvl = 1
    errors = 0
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    mainFont = pygame.font.SysFont('roboto', 40)
    errorFont = pygame.font.SysFont('roboto', 30)
    board, original_board, sketch_board = get_board(lvl)

    start = time.time()
    draw_board(win, board, sketch_board, original_board, errors, lvl)
    zeros = 0
    while True:
        play_time = round(time.time() - start)
        run = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and run == False:
                pos = pygame.mouse.get_pos()

                if 49 < pos[0] < 499 and 49 < pos[1] < 499 and zeros >= 0:
                    pygame.draw.rect(win, (230, 230, 230), ((pos[0] // 50) * 50, (pos[1] // 50) * 50, 50, 50), 4)
                    pygame.display.update()
                    errors = insert(win, (pos[0] // 50, pos[1] // 50), board, original_board, sketch_board, errors, lvl, start)
                elif 552 < pos[0] < 613 and 132 < pos[1] < 152:
                    lvl = 1
                    draw_board(win, board, sketch_board, original_board, errors, lvl)
                elif 619 < pos[0] < 680 and 132 < pos[1] < 152:
                    lvl = 2
                    draw_board(win, board, sketch_board, original_board, errors, lvl)
                elif 686 < pos[0] < 747 and 132 < pos[1] < 152:
                    lvl = 3
                    draw_board(win, board, sketch_board, original_board, errors, lvl)
                elif 627 < pos[0] < 672 and 171 < pos[1] < 198:
                    errors = 0
                    start = time.time()
                    play_time = round(time.time() - start)
                    board, original_board, sketch_board = get_board(lvl)
                    draw_board(win, board, sketch_board, original_board, errors, lvl)
                elif 577 < pos[0] < 722 and 258 < pos[1] < 308:
                    for i in range(9):
                        for j in range(9):
                            sketch_board[i][j] = 0
                    run = True

                    while run:
                        solve2(board, win, sketch_board, original_board, errors, lvl)
                        zeros = 0
                        for i in board:
                            zeros = zeros + i.count(0)
                        if zeros == 0:
                            run = False
                        play_time = round(time.time() - start)
                        format_time(win, play_time)
                        beg = time.time()
                        end = 0
                        while end < 1:
                            end = round(time.time() - beg)
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        for i in board:
            zeros = zeros + i.count(0)
        if zeros > 0:
            zeros = 0
            format_time(win, play_time)
        elif zeros == 0:
            draw_board(win, board, sketch_board, original_board, errors, lvl)
            zeros = -1
            end = round(time.time() - start)
        elif zeros == -1:
            format_time(win, end, zeros)
            fnt = pygame.font.SysFont("roboto", 80)
            text = fnt.render("WIN!!!", True, (50, 205, 50))
            win.blit(text, (200, 700))
            pygame.display.update()
main()
