#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a project powered by Codecademy students.
The project features a modified single-player version of the classic game: battleships.

Game based on tutorials by Al Sweigart in his book 'Making Games with Python
& Pygame"
http://inventwithpython.com/pygame/chapters/

The game requires python 2 and the pygame modules.
The game is a battleship puzzle game. The objective is to sink all the ships in as few shots as possible.
The markers on the edges of the game board tell you how many ship pieces are in each column and row.
"""
# Importing pygame modules
import random, sys, os, pygame
from pygame.locals import *

# Set variables, like screen width and height
# globals
FPS = 30 #Determines the number of frames per second
REVEALSPEED = 8 #Determines the speed at which the squares reveals after being clicked
WINDOWWIDTH = 800 #Width of game window
WINDOWHEIGHT = 600 #Height of game window
TILESIZE = 40 #Size of the squares in each grid(tile)
MARKERSIZE = 40 #Size of the box which contatins the number that indicates how many ships in this row/col
BUTTONHEIGHT = 20 #Height of a standard button
BUTTONWIDTH = 40 #Width of a standard button
TEXT_HEIGHT = 25 #Size of the text
TEXT_LEFT_POSN = 10 #Where the text will be positioned
BOARDWIDTH = 10 #Number of grids horizontally
BOARDHEIGHT = 10 #Number of grids vertically
DISPLAYWIDTH = 200 #Width of the game board
EXPLOSIONSPEED = 10 #How fast the explosion graphics will play

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * TILESIZE) - DISPLAYWIDTH - MARKERSIZE) / 2) #x-position of the top left corner of board
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * TILESIZE) - MARKERSIZE) / 2) #y-position of the top left corner of board

# Warm sunset/military colour palette (matches bg.eps)
BLACK       = (  0,   0,   0)
WHITE       = (255, 255, 255)
CREAM       = (255, 235, 200)
DARK_BROWN  = ( 50,  30,  15)
AMBER       = (230, 160,  30)
DEEP_ORANGE = (200,  90,  20)
BURNT_SIENNA= (160,  60,  20)
OLIVE_GREEN = ( 60,  70,  30)
DARK_OLIVE  = ( 40,  45,  20)
SUNSET_GOLD = (255, 200,  60)

#Determine what to colour each element of the game
BGCOLOR = DARK_BROWN
BUTTONCOLOR = DEEP_ORANGE
TEXTCOLOR = CREAM
TILECOLOR = OLIVE_GREEN
BORDERCOLOR = AMBER
TEXTSHADOWCOLOR = BURNT_SIENNA
SHIPCOLOR = AMBER
MARKCOLOR = DARK_OLIVE
HIGHLIGHTCOLOR = SUNSET_GOLD
GRIDLINECOLOR = (30, 20, 10)

# HUD layout constants
HUD_TOP = 8
HUD_ICON_SIZE = 36
HUD_LEFT = 15
HUD_BAR_HEIGHT = 52

# Background mode: "image" (default bg), "custom" (user-chosen), "none" (solid color)
DEFAULT_BG_PATH = "img/bg.png"


def main():
    """
    The main function intializes the variables which will be used by the game.
    """
    global DISPLAYSURF, FPSCLOCK, BASICFONT, HELP_SURF, HELP_RECT, NEW_SURF, \
           NEW_RECT, BIGFONT, EXPLOSION_IMAGES, CANON_IMG, SHIP_IMG, \
           INSTR_SURF, INSTR_RECT, BG_IMG, BG_MODE, HUDFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    #Fonts used by the game
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 50)
    HUDFONT = pygame.font.Font('freesansbold.ttf', 24)

    # Load and scale background image
    BG_IMG = load_bg_image(DEFAULT_BG_PATH)
    BG_MODE = "image" if BG_IMG else "none"

    # Create and label the buttons - positioned in the right panel
    panel_x = XMARGIN + MARKERSIZE + BOARDWIDTH * TILESIZE + 20
    HELP_SURF, HELP_RECT = make_button("HELP", panel_x, WINDOWHEIGHT // 2 - 30)
    NEW_SURF, NEW_RECT = make_button("NEW GAME", panel_x, WINDOWHEIGHT // 2 + 30)

    # Load the explosion graphics from the /img folder
    EXPLOSION_IMAGES = [
        pygame.image.load("img/blowup1.png"), pygame.image.load("img/blowup2.png"),
        pygame.image.load("img/blowup3.png"),pygame.image.load("img/blowup4.png"),
        pygame.image.load("img/blowup5.png"),pygame.image.load("img/blowup6.png")]

    # Load images for counters
    CANON_IMG = pygame.image.load("img/canon.png")
    CANON_IMG = pygame.transform.scale(CANON_IMG, (HUD_ICON_SIZE, HUD_ICON_SIZE))
    SHIP_IMG = pygame.image.load("img/ship.png")
    SHIP_IMG = pygame.transform.scale(SHIP_IMG, (HUD_ICON_SIZE, HUD_ICON_SIZE))

    # Instructions text (includes B key for background toggle)
    INSTR_SURF = BASICFONT.render("L-Click/Enter: Reveal | R-Click/C: Mark | Arrows: Move | B: Background | ESC: Quit", True, CREAM)
    INSTR_RECT = INSTR_SURF.get_rect()
    INSTR_RECT.midbottom = (WINDOWWIDTH // 2, WINDOWHEIGHT - 8)

    # Set the title in the menu bar to 'Battleship'
    pygame.display.set_caption('Battleship')

    # Keep the game running at all times
    while True:
        shots_taken = run_game() #Run the game until it stops and save the result in shots_taken
        play_again = show_gameover_screen(shots_taken) #Display a gameover screen and get user's choice
        if not play_again:
            pygame.quit()
            sys.exit()


def make_button(text, x, y):
    """
    Creates a styled button surface and rect.
    """
    font = pygame.font.Font('freesansbold.ttf', 18)
    text_surf = font.render(text, True, CREAM)
    padding_x, padding_y = 20, 10
    w = text_surf.get_width() + padding_x * 2
    h = text_surf.get_height() + padding_y * 2
    btn_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(btn_surf, DEEP_ORANGE, (0, 0, w, h), border_radius=6)
    pygame.draw.rect(btn_surf, AMBER, (0, 0, w, h), 2, border_radius=6)
    btn_surf.blit(text_surf, (padding_x, padding_y))
    btn_rect = btn_surf.get_rect()
    btn_rect.topleft = (x, y)
    return btn_surf, btn_rect


def load_bg_image(path):
    """
    Loads and scales a background image. Returns None if the file doesn't exist
    or can't be loaded.
    """
    if not path or not os.path.isfile(path):
        return None
    try:
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, (WINDOWWIDTH, WINDOWHEIGHT))
    except pygame.error:
        return None


def cycle_background():
    """
    Cycles background mode: image -> none -> custom (file picker) -> image -> ...
    """
    global BG_MODE, BG_IMG
    if BG_MODE == "image":
        BG_MODE = "none"
    elif BG_MODE == "none":
        # Try to open a file picker for custom image
        custom_path = open_file_dialog()
        if custom_path:
            img = load_bg_image(custom_path)
            if img:
                BG_IMG = img
                BG_MODE = "custom"
            else:
                # Failed to load, fall back to default
                BG_IMG = load_bg_image(DEFAULT_BG_PATH)
                BG_MODE = "image" if BG_IMG else "none"
        else:
            # User cancelled, go back to default image
            BG_IMG = load_bg_image(DEFAULT_BG_PATH)
            BG_MODE = "image" if BG_IMG else "none"
    elif BG_MODE == "custom":
        BG_IMG = load_bg_image(DEFAULT_BG_PATH)
        BG_MODE = "image" if BG_IMG else "none"


def open_file_dialog():
    """
    Opens a file dialog using tkinter to let the user pick a background image.
    Returns the selected file path, or None if cancelled.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = filedialog.askopenfilename(
            title="Choose a background image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tga"),
                       ("All files", "*.*")])
        root.destroy()
        return file_path if file_path else None
    except Exception:
        return None


def draw_background():
    """
    Draws the background based on current BG_MODE.
    """
    if BG_MODE in ("image", "custom") and BG_IMG is not None:
        DISPLAYSURF.blit(BG_IMG, (0, 0))
        # Heavy overlay to reduce distraction
        overlay = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        DISPLAYSURF.blit(overlay, (0, 0))
    else:
        DISPLAYSURF.fill(BGCOLOR)


def draw_hud(shot_count, ships_hit, total_ship_tiles):
    """
    Draws the heads-up display with shot count and ship hit count,
    properly aligned with icons.
    """
    # Semi-transparent HUD background bar
    hud_bar = pygame.Surface((WINDOWWIDTH, HUD_BAR_HEIGHT), pygame.SRCALPHA)
    hud_bar.fill((0, 0, 0, 160))
    DISPLAYSURF.blit(hud_bar, (0, 0))

    icon_y = HUD_TOP + (HUD_BAR_HEIGHT - HUD_TOP * 2 - HUD_ICON_SIZE) // 2 + HUD_TOP
    text_center_y = icon_y + HUD_ICON_SIZE // 2
    x = HUD_LEFT

    # Canon icon + shots count
    DISPLAYSURF.blit(CANON_IMG, (x, icon_y))
    x += HUD_ICON_SIZE + 8
    shots_surf = HUDFONT.render(f"Shots: {shot_count}", True, CREAM)
    shots_rect = shots_surf.get_rect()
    shots_rect.midleft = (x, text_center_y)
    DISPLAYSURF.blit(shots_surf, shots_rect)

    x += shots_rect.width + 40

    # Separator line
    pygame.draw.line(DISPLAYSURF, AMBER, (x, icon_y + 2), (x, icon_y + HUD_ICON_SIZE - 2), 2)
    x += 20

    # Ship icon + hits count
    DISPLAYSURF.blit(SHIP_IMG, (x, icon_y))
    x += HUD_ICON_SIZE + 8
    ships_surf = HUDFONT.render(f"Hits: {ships_hit}/{total_ship_tiles}", True, CREAM)
    ships_rect = ships_surf.get_rect()
    ships_rect.midleft = (x, text_center_y)
    DISPLAYSURF.blit(ships_surf, ships_rect)

    # Background mode indicator on the right side of HUD
    mode_label = {"image": "BG: Default", "custom": "BG: Custom", "none": "BG: Off"}
    mode_surf = BASICFONT.render(mode_label[BG_MODE], True, AMBER)
    mode_rect = mode_surf.get_rect()
    mode_rect.midright = (WINDOWWIDTH - 15, text_center_y)
    DISPLAYSURF.blit(mode_surf, mode_rect)


def run_game():
    """
    Function is executed while a game is running.

    returns the amount of shots taken
    """
    revealed_tiles = generate_default_tiles(False)
    marked_tiles = generate_default_tiles(False)
    main_board = generate_default_tiles(None)
    ship_objs = ['battleship','cruiser1','cruiser2','destroyer1','destroyer2',
                 'destroyer3','submarine1','submarine2','submarine3','submarine4'] # List of the ships available
    main_board = add_ships_to_board(main_board, ship_objs) #call add_ships_to_board to add the list of ships to the main_board
    mousex, mousey = 0, 0
    kb_tilex, kb_tiley = 0, 0
    counter = []
    xmarkers, ymarkers = set_markers(main_board)
    last_move_time = 0
    move_delay = 150

    while True:
        ships_hit = sum(1 for x in range(BOARDWIDTH) for y in range(BOARDHEIGHT)
                       if revealed_tiles[x][y] and main_board[x][y] is not None)
        total_ship_tiles = sum(1 for x in range(BOARDWIDTH) for y in range(BOARDHEIGHT)
                              if main_board[x][y] is not None)

        # Draw background (image or solid, depending on mode)
        draw_background()

        # Draw semi-transparent overlay behind the board area for readability
        board_bg = pygame.Surface(
            (MARKERSIZE + BOARDWIDTH * TILESIZE + 10,
             MARKERSIZE + BOARDHEIGHT * TILESIZE + 10),
            pygame.SRCALPHA)
        board_bg.fill((0, 0, 0, 200))
        DISPLAYSURF.blit(board_bg, (XMARGIN - 5, YMARGIN - 5))

        # draw the buttons
        DISPLAYSURF.blit(HELP_SURF, HELP_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)

        # Draw the HUD (shots + ships) properly aligned
        draw_hud(len(counter), ships_hit, total_ship_tiles)

        # Instructions bar at bottom
        instr_bar = pygame.Surface((WINDOWWIDTH, 32), pygame.SRCALPHA)
        instr_bar.fill((0, 0, 0, 140))
        DISPLAYSURF.blit(instr_bar, (0, WINDOWHEIGHT - 32))
        DISPLAYSURF.blit(INSTR_SURF, INSTR_RECT)

        draw_board(main_board, revealed_tiles, marked_tiles)
        draw_markers(xmarkers, ymarkers)

        mouse_clicked = False

        check_for_quit()
        #Check for pygame events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if HELP_RECT.collidepoint(event.pos):
                    draw_background()
                    show_help_screen()
                elif NEW_RECT.collidepoint(event.pos):
                    main()
                elif event.button == 3:
                    tilex, tiley = get_tile_at_pixel(event.pos[0], event.pos[1])
                    if tilex is not None and tiley is not None and not revealed_tiles[tilex][tiley]:
                        marked_tiles[tilex][tiley] = not marked_tiles[tilex][tiley]
                else:
                    mousex, mousey = event.pos
                    mouse_clicked = True
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key in (K_RETURN, K_SPACE):
                    if not revealed_tiles[kb_tilex][kb_tiley]:
                        tilex, tiley = kb_tilex, kb_tiley
                        mouse_clicked = True
                elif event.key == K_c:
                    if not revealed_tiles[kb_tilex][kb_tiley]:
                        marked_tiles[kb_tilex][kb_tiley] = not marked_tiles[kb_tilex][kb_tiley]
                elif event.key == K_b:
                    cycle_background()

        # Handle continuous arrow key movement with delay
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > move_delay:
            moved = False
            if keys[K_LEFT] and kb_tilex > 0:
                kb_tilex -= 1
                moved = True
            elif keys[K_RIGHT] and kb_tilex < BOARDWIDTH - 1:
                kb_tilex += 1
                moved = True
            elif keys[K_UP] and kb_tiley > 0:
                kb_tiley -= 1
                moved = True
            elif keys[K_DOWN] and kb_tiley < BOARDHEIGHT - 1:
                kb_tiley += 1
                moved = True

            if moved:
                last_move_time = current_time

        #Check if the mouse is clicked at a position with a ship piece
        tilex, tiley = get_tile_at_pixel(mousex, mousey)
        if tilex is None or tiley is None:
            tilex, tiley = kb_tilex, kb_tiley
        if tilex is not None and tiley is not None:
            if not revealed_tiles[tilex][tiley]:
                draw_highlight_tile(tilex, tiley)
            if not revealed_tiles[tilex][tiley] and mouse_clicked:
                reveal_tile_animation(main_board, [(tilex, tiley)])
                revealed_tiles[tilex][tiley] = True #set the tile to now be revealed
                if check_revealed_tile(main_board, [(tilex, tiley)]): # if the clicked position contains a ship piece
                    left, top = left_top_coords_tile(tilex, tiley)
                    blowup_animation((left, top))
                    if check_for_win(main_board, revealed_tiles): # check for a win
                        counter.append((tilex, tiley))
                        return len(counter) # return the amount of shots taken
                counter.append((tilex, tiley))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_default_tiles(default_value):
    """
    Function generates a list of 10 x 10 tiles. The list will contain tuples
    ('shipName', boolShot) set to their (default_value).

    default_value -> boolean which tells what the value to set to
    returns the list of tuples
    """
    default_tiles = [[default_value]*BOARDHEIGHT for i in range(BOARDWIDTH)]

    return default_tiles


def blowup_animation(coord):
    """
    Function creates the explosition played if a ship is shot.

    coord -> tuple of tile coords to apply the blowup animation
    """
    for image in EXPLOSION_IMAGES: # go through the list of images in the list of pictures and play them in sequence
        #Determine the location and size to display the image
        image = pygame.transform.scale(image, (TILESIZE+10, TILESIZE+10))
        DISPLAYSURF.blit(image, coord)
        pygame.display.flip()
        FPSCLOCK.tick(EXPLOSIONSPEED) #Determine the delay to play the image with


def check_revealed_tile(board, tile):
    """
    Function checks if a tile location contains a ship piece.

    board -> the tiled board either a ship piece or none
    tile -> location of tile
    returns True if ship piece exists at tile location
    """
    return board[tile[0][0]][tile[0][1]] != None


def reveal_tile_animation(board, tile_to_reveal):
    """
    Function creates an animation which plays when the mouse is clicked on a tile, and whatever is
    behind the tile needs to be revealed.

    board -> list of board tile tuples ('shipName', boolShot)
    tile_to_reveal -> tuple of tile coords to apply the reveal animation to
    """
    for coverage in range(TILESIZE, (-REVEALSPEED) - 1, -REVEALSPEED): #Plays animation based on reveal speed
        draw_tile_covers(board, tile_to_reveal, coverage)


def draw_tile_covers(board, tile, coverage):
    """
    Function draws the tiles according to a set of variables.

    board -> list; of board tiles
    tile -> tuple; of tile coords to reveal
    coverage -> int; amount of the tile that is covered
    """
    left, top = left_top_coords_tile(tile[0][0], tile[0][1])
    if check_revealed_tile(board, tile):
        pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (left, top, TILESIZE,
                                                  TILESIZE))
    else:
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, TILESIZE,
                                                TILESIZE))
    if coverage > 0:
        pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, coverage,
                                                  TILESIZE))

    pygame.display.update()
    FPSCLOCK.tick(FPS)


def check_for_quit():
    """
    Function checks if the user has attempted to quit the game.
    """
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()


def check_for_win(board, revealed):
    """
    Function checks if the current board state is a winning state.

    board -> the board which contains the ship pieces
    revealed -> list of revealed tiles
    returns True if all the ships are revealed
    """
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            if board[tilex][tiley] != None and not revealed[tilex][tiley]: # check if every board with a ship is revealed, return false if not
                return False
    return True


def draw_board(board, revealed, marked):
    """
    Function draws the game board.

    board -> list of board tiles
    revealed -> list of revealed tiles
    marked -> list of marked tiles (not ship)
    """
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = left_top_coords_tile(tilex, tiley)
            if not revealed[tilex][tiley]:
                if marked[tilex][tiley]:
                    pygame.draw.rect(DISPLAYSURF, MARKCOLOR, (left, top, TILESIZE, TILESIZE))
                    pygame.draw.line(DISPLAYSURF, BURNT_SIENNA, (left + 5, top + 5), (left + TILESIZE - 5, top + TILESIZE - 5), 3)
                    pygame.draw.line(DISPLAYSURF, BURNT_SIENNA, (left + TILESIZE - 5, top + 5), (left + 5, top + TILESIZE - 5), 3)
                else:
                    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left, top, TILESIZE, TILESIZE))
            else:
                if board[tilex][tiley] != None:
                    pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (left, top, TILESIZE, TILESIZE))
                else:
                    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, TILESIZE, TILESIZE))
    #draws the vertical lines
    for x in range(0, (BOARDWIDTH + 1) * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (x + XMARGIN + MARKERSIZE,
            YMARGIN + MARKERSIZE), (x + XMARGIN + MARKERSIZE,
            WINDOWHEIGHT - YMARGIN))
    #draws the horizontal lines
    for y in range(0, (BOARDHEIGHT + 1) * TILESIZE, TILESIZE):
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (XMARGIN + MARKERSIZE, y +
            YMARGIN + MARKERSIZE), (WINDOWWIDTH - (DISPLAYWIDTH + MARKERSIZE *
            2), y + YMARGIN + MARKERSIZE))


def set_markers(board):
    """
    Function creates the lists of the markers to the side of the game board which indicates
    the number of ship pieces in each row and column.

    board: list of board tiles
    returns the 2 lists of markers with number of ship pieces in each row (xmarkers)
        and column (ymarkers)
    """
    xmarkers = [0 for i in range(BOARDWIDTH)]
    ymarkers = [0 for i in range(BOARDHEIGHT)]
    #Loop through the tiles
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            if board[tilex][tiley] != None: #if the tile is a ship piece, then increment the markers
                xmarkers[tilex] += 1
                ymarkers[tiley] += 1

    return xmarkers, ymarkers


def draw_markers(xlist, ylist):
    """
    Function draws the two list of markers to the side of the board.

    xlist -> list of row markers
    ylist -> list of column markers
    """
    for i in range(len(xlist)): #Draw the x-marker list
        left = i * MARKERSIZE + XMARGIN + MARKERSIZE + (TILESIZE / 2)
        top = YMARGIN + (MARKERSIZE / 2)
        marker_surf, marker_rect = make_text_objs(str(xlist[i]),
                                                    BASICFONT, TEXTCOLOR)
        marker_rect.center = (left, top)
        DISPLAYSURF.blit(marker_surf, marker_rect)
    for i in range(len(ylist)): #Draw the y-marker list
        left = XMARGIN + (MARKERSIZE / 2)
        top = i * MARKERSIZE + YMARGIN + MARKERSIZE + (TILESIZE / 2)
        marker_surf, marker_rect = make_text_objs(str(ylist[i]),
                                                    BASICFONT, TEXTCOLOR)
        marker_rect.center = (left, top)
        DISPLAYSURF.blit(marker_surf, marker_rect)



def add_ships_to_board(board, ships):
    """
    Function goes through a list of ships and add them randomly into a board.

    board -> list of board tiles
    ships -> list of ships to place on board
    returns list of board tiles with ships placed on certain tiles
    """
    new_board = board[:]
    ship_length = 0
    for ship in ships: #go through each ship declared in the list
        #Randomly find a valid position that fits the ship
        valid_ship_position = False
        while not valid_ship_position:
            xStartpos = random.randint(0, 9)
            yStartpos = random.randint(0, 9)
            isHorizontal = random.randint(0, 1) #vertical or horizontal positioning
            #Type of ship and their respective length
            if 'battleship' in ship:
                ship_length = 4
            elif 'cruiser' in ship:
                ship_length = 3
            elif 'destroyer'in ship:
                ship_length = 2
            elif 'submarine' in ship:
                ship_length = 1

            #check if position is valid
            valid_ship_position, ship_coords = make_ship_position(new_board,
                xStartpos, yStartpos, isHorizontal, ship_length, ship)
            #add the ship if it is valid
            if valid_ship_position:
                for coord in ship_coords:
                    new_board[coord[0]][coord[1]] = ship
    return new_board


def make_ship_position(board, xPos, yPos, isHorizontal, length, ship):
    """
    Function makes a ship on a board given a set of variables

    board -> list of board tiles
    xPos -> x-coordinate of first ship piece
    yPos -> y-coordinate of first ship piece
    isHorizontal -> True if ship is horizontal
    length -> length of ship
    returns tuple: True if ship position is valid and list ship coordinates
    """
    ship_coordinates = [] #the coordinates the ship will occupy
    if isHorizontal:
        for i in range(length):
            if (i+xPos > 9) or (board[i+xPos][yPos] != None) or \
                hasAdjacent(board, i+xPos, yPos, ship): #if the ship goes out of bound, hits another ship, or is adjacent to another ship
                return (False, ship_coordinates) #then return false
            else:
                ship_coordinates.append((i+xPos, yPos))
    else:
        for i in range(length):
            if (i+yPos > 9) or (board[xPos][i+yPos] != None) or \
                hasAdjacent(board, xPos, i+yPos, ship): #if the ship goes out of bound, hits another ship, or is adjacent to another ship
                return (False, ship_coordinates) #then return false
            else:
                ship_coordinates.append((xPos, i+yPos))
    return (True, ship_coordinates) #ship is successfully added


def hasAdjacent(board, xPos, yPos, ship):
    """
    Funtion checks if a ship has adjacent ships

    board -> list of board tiles
    xPos -> x-coordinate of first ship piece
    yPos -> y-coordinate of first ship piece
    ship -> the ship being checked for adjacency
    returns true if there are adjacent ships and false if there are no adjacent ships
    """
    for x in range(xPos-1,xPos+2):
        for y in range(yPos-1,yPos+2):
            if (x in range (10)) and (y in range (10)) and \
                (board[x][y] not in (ship, None)):
                return True
    return False


def left_top_coords_tile(tilex, tiley):
    """
    Function calculates and returns the pixel of the tile in the top left corner

    tilex -> int; x position of tile
    tiley -> int; y position of tile
    returns tuple (int, int) which indicates top-left pixel coordinates of tile
    """
    left = tilex * TILESIZE + XMARGIN + MARKERSIZE
    top = tiley * TILESIZE + YMARGIN + MARKERSIZE
    return (left, top)


def get_tile_at_pixel(x, y):
    """
    Function finds the corresponding tile coordinates of pixel at top left, defaults to (None, None) given a coordinate.

    x -> int; x position of pixel
    y -> int; y position of pixel
    returns tuple (tilex, tiley)
    """
    for tilex in range(BOARDWIDTH):
        for tiley in range(BOARDHEIGHT):
            left, top = left_top_coords_tile(tilex, tiley)
            tile_rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tile_rect.collidepoint(x, y):
                return (tilex, tiley)
    return (None, None)


def draw_highlight_tile(tilex, tiley):
    """
    Function draws the hovering highlight over the tile.

    tilex -> int; x position of tile
    tiley -> int; y position of tile
    """
    left, top = left_top_coords_tile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR,
                    (left, top, TILESIZE, TILESIZE), 4)


def show_help_screen():
    """
    Function display a help screen until any button is pressed.
    """
    # Draw dark overlay on background
    overlay = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 220))
    DISPLAYSURF.blit(overlay, (0, 0))

    line1_surf, line1_rect = make_text_objs('Press a key to return to the game',
                                            BASICFONT, TEXTCOLOR)
    line1_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT)
    DISPLAYSURF.blit(line1_surf, line1_rect)

    line2_surf, line2_rect = make_text_objs(
        'This is a battleship puzzle game. Your objective is ' \
        'to sink all the ships in as few', BASICFONT, TEXTCOLOR)
    line2_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 3)
    DISPLAYSURF.blit(line2_surf, line2_rect)

    line3_surf, line3_rect = make_text_objs('shots as possible. The markers on'\
        ' the edges of the game board tell you how', BASICFONT, TEXTCOLOR)
    line3_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 4)
    DISPLAYSURF.blit(line3_surf, line3_rect)

    line4_surf, line4_rect = make_text_objs('many ship pieces are in each'\
        ' column and row. To reset your game click on', BASICFONT, TEXTCOLOR)
    line4_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 5)
    DISPLAYSURF.blit(line4_surf, line4_rect)

    line5_surf, line5_rect = make_text_objs('the "New Game" button.',
        BASICFONT, TEXTCOLOR)
    line5_rect.topleft = (TEXT_LEFT_POSN, TEXT_HEIGHT * 6)
    DISPLAYSURF.blit(line5_surf, line5_rect)

    while check_for_keypress() == None: #Check if the user has pressed keys, if so go back to the game
        pygame.display.update()
        FPSCLOCK.tick()


def check_for_keypress():
    """
    Function checks for any key presses by pulling out KEYUP events from queue.

    returns any KEYUP events, otherwise return None
    """
    for event in pygame.event.get([KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]):
        if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION):
            continue
        return event.key
    return None


def make_text_objs(text, font, color):
    """
    Function creates a text.

    text -> string; content of text
    font -> Font object; face of font
    color -> tuple of color (red, green blue); colour of text
    returns the surface object, rectangle object
    """
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def show_gameover_screen(shots_fired):
    """
    Function display a gameover screen when the user has successfully shot at every ship pieces.

    shots_fired -> the number of shots taken before game is over
    returns True if user wants to play again, False if they want to quit
    """
    draw_background()

    titleSurf, titleRect = make_text_objs('Congrats! Puzzle solved in:',
                                            BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2 - 50))
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = make_text_objs('Congrats! Puzzle solved in:',
                                            BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2 - 50) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = make_text_objs(str(shots_fired) + ' shots',
                                            BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = make_text_objs(str(shots_fired) + ' shots',
                                            BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = make_text_objs(
        'Press Y to play again or N to quit', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while True:
        key = check_for_keypress()
        if key is not None:
            if key == K_y:
                return True
            elif key == K_n or key == K_ESCAPE:
                return False
        pygame.display.update()
        FPSCLOCK.tick()


if __name__ == "__main__": #This calls the game loop
    main()
