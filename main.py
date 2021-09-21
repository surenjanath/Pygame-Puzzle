'''
Game Development

Author : Surenjanath Singh
Course : Game Development with Pygame | Real World Game
Game   : Puzzle
'''
# Libraries
import pygame as py
import os
import cfg
import sys
import random

class Puzzle():
    def __init__(self):
        self.BOARD = []
        py.init()
        self.clock = py.time.Clock()
        self.game_pic = py.image.load(self.GetImagePaths(cfg.PICTURE_PATH))
        self.game_pic = py.transform.scale(self.game_pic,cfg.SCREENSIZE)
        self.game_pic_rect = self.game_pic.get_rect()
        self.SCREEN = py.display.set_mode(cfg.SCREENSIZE)
        py.display.set_caption('PUZZLE GAME')
        self.width  = self.game_pic_rect.width
        self.height = self.game_pic_rect.height
        size = self.ShowStartInterface()
        assert isinstance(size, int)
        num_rows, num_cols  = size, size
        num_cells           = size * size
        cell_width = self.game_pic_rect.width//num_cols
        cell_height = self.game_pic_rect.height//num_rows

        while True:
            blank_cell_idx = self.CreateBOARD(num_rows, num_cols, num_cells)
            if not self.isGameOver(size):
                break
        is_running = True
        while is_running :
            for event in py.event.get():
                if (event.type == py.QUIT) or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                    py.quit()
                    sys.exit()

                elif event.type == py.KEYDOWN:
                    if event.key == py.K_LEFT or event.key == ord('a'):
                        blank_cell_idx = self.moveL(blank_cell_idx, num_cols)
                    elif event.key == py.K_RIGHT or event.key == ord('d'):
                        blank_cell_idx = self.moveR(blank_cell_idx, num_cols)
                    elif event.key == py.K_UP or event.key == ord('w'):
                        blank_cell_idx = self.moveU(blank_cell_idx, num_rows, num_cols)
                    elif event.key == py.K_DOWN or event.key == ord('s'):
                        blank_cell_idx = self.moveD(blank_cell_idx, num_cols)

                elif event.type == py.MOUSEBUTTONDOWN and event.button == 1 :
                    x, y = py.mouse.get_pos()
                    x_pos = x//cell_width
                    y_pos = y//cell_height
                    idx = x_pos + y_pos * num_cols

                    if idx == blank_cell_idx - 1:
                        blank_cell_idx = self.moveR(blank_cell_idx, num_cols)
                    elif idx == blank_cell_idx + 1:
                        blank_cell_idx = self.moveL(blank_cell_idx, num_cols)
                    elif idx == blank_cell_idx + num_cols:
                        blank_cell_idx = self.moveU(blank_cell_idx, num_rows, num_cols)
                    elif idx == blank_cell_idx - num_cols:
                        blank_cell_idx = self.moveD(blank_cell_idx, num_cols)
            if self.isGameOver(size):
                self.BOARD[blank_cell_idx] = num_cells - 1
                is_running = False
            self.SCREEN.fill(cfg.BACKGROUNDCOLOR)
            for i in range(num_cells):
                if self.BOARD[i] == -1:
                    continue
                x_pos = i//num_cols
                y_pos = i% num_cols

                rect = py.Rect(y_pos * cell_width, x_pos * cell_height, cell_width, cell_height)
                img_area = py.Rect(
                    (self.BOARD[i] % num_cols) * cell_width,
                    (self.BOARD[i] // num_cols) * cell_height,
                    cell_width,
                    cell_height)
                self.SCREEN.blit(self.game_pic, rect, img_area)
            for i in range(num_cols + 1):
                py.draw.line(self.SCREEN,
                             cfg.BLACK,
                             (i*cell_width,0),
                             (i*cell_width,self.game_pic_rect.height))

            for i in range(num_rows + 1):
                py.draw.line(self.SCREEN,
                             cfg.BLACK,
                             (0, i*cell_height),
                             (self.game_pic_rect.width,i*cell_height))
            py.display.update()
            self.clock.tick(cfg.FPS)
        self.ShowEndInterface()

    def ShowStartInterface(self):
        self.SCREEN.fill(cfg.BACKGROUNDCOLOR)
        tfont       = py.font.Font(cfg.FONT1_PATH, self.width//4)
        cfont       = py.font.Font(cfg.FONT2_PATH, self.width//20)
        title       = tfont.render('Puzzle',True, cfg.RED)
        content1    = cfont.render('PRESS H, M or L to choose your puzzle',
                                   True,
                                   cfg.BLUE)
        Level1    = cfont.render('H : 10 x 10',
                                   True,
                                   cfg.BLUE)


        Level2    = cfont.render('M :  5 x  5',
                                   True,
                                   cfg.BLUE)

        Level3    = cfont.render('L :  3 x  3',
                                   True,
                                   cfg.BLUE)


        trect       = title.get_rect()
        trect.midtop= (self.width/2, self.height/10)
        crect1 = content1.get_rect()
        crect1.midtop =  (self.width/2, self.height/2.2)

        lrect1 = Level1.get_rect()
        lrect1.midtop =  (self.width/2, self.height/1.8)
        lrect2 = Level2.get_rect()
        lrect2.midtop =  (self.width/2, self.height/1.6)
        lrect3 = Level3.get_rect()
        lrect3.midtop =  (self.width/2, self.height/1.4)


        self.SCREEN.blit(title, trect)
        self.SCREEN.blit(content1, crect1)
        self.SCREEN.blit(Level1, lrect1)
        self.SCREEN.blit(Level2, lrect2)
        self.SCREEN.blit(Level3, lrect3)

        while True:
            for event in py.event.get():
                if (event.type == py.QUIT) or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                    py.quit()
                    sys.exit()
                elif event.type == py.KEYDOWN :
                    if event.key == ord('l') : return 3
                    if event.key == ord('m') : return 4
                    if event.key == ord('h') : return 5

            py.display.update()

    def isGameOver(self, size):
        assert isinstance(size,int)
        num_cells = size * size
        for i in range(num_cells - 1):
            if self.BOARD[i] != i : return False
        return True

    def moveR(self,blank_cell_idx,num_cols):
        if blank_cell_idx % num_cols == 0 : return blank_cell_idx
        self.BOARD[blank_cell_idx - 1], self.BOARD[blank_cell_idx] = self.BOARD[blank_cell_idx], self.BOARD[blank_cell_idx - 1]
        return blank_cell_idx - 1

    def moveL(self, blank_cell_idx,num_cols):
        if (blank_cell_idx + 1) % num_cols == 0 : return blank_cell_idx
        self.BOARD[blank_cell_idx + 1], self.BOARD[blank_cell_idx] = self.BOARD[blank_cell_idx], self.BOARD[blank_cell_idx + 1]
        return blank_cell_idx + 1

    def moveD(self, blank_cell_idx,num_cols):
        if blank_cell_idx < num_cols  : return blank_cell_idx
        self.BOARD[blank_cell_idx - num_cols], self.BOARD[blank_cell_idx] = self.BOARD[blank_cell_idx], self.BOARD[blank_cell_idx - num_cols]
        return blank_cell_idx - num_cols

    def moveU(self, blank_cell_idx, num_rows, num_cols):
        if blank_cell_idx >= (num_rows - 1) * num_cols : return blank_cell_idx
        self.BOARD[blank_cell_idx + num_cols], self.BOARD[blank_cell_idx] = self.BOARD[blank_cell_idx], self.BOARD[blank_cell_idx + num_cols]

        return blank_cell_idx + num_cols

    def CreateBOARD(self, num_rows, num_cols, num_cells):

        for i in range(num_cells):
            self.BOARD.append(i)

        blank_cell_idx          = num_cells - 1

        self.BOARD[blank_cell_idx]   = -1

        for i in range(cfg.RANDNUM):
            direction = random.randint(0,3)
            if direction == 0 :
                blank_cell_idx = self.moveL(blank_cell_idx, num_cols)
            elif direction == 1 :
                blank_cell_idx = self.moveR(blank_cell_idx, num_cols)
            elif direction == 2 :
                blank_cell_idx = self.moveU(blank_cell_idx, num_rows, num_cols)
            elif direction == 3 :
                blank_cell_idx = self.moveD(blank_cell_idx, num_cols)

        return blank_cell_idx

    def GetImagePaths(self,rootdir):
        imageNames = os.listdir(rootdir)
        assert len(imageNames) > 0
        return os.path.join(rootdir,random.choice(imageNames))

    def ShowEndInterface(self):
        self.SCREEN.fill(cfg.BACKGROUNDCOLOR)
        font            = py.font.Font(cfg.FONT4_PATH, self.width//10)
        title           = font.render('GOOD JOB YOU WON !', True, (133,150,122))
        rect            = title.get_rect()
        rect.midtop     = (self.width/2, self.height/2.5)
        self.SCREEN.blit(title, rect)
        py.display.update()
        while True :
            for event in py.event.get():
                if (event.type == py.QUIT) or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                    py.quit()
                    sys.exit()
            py.display.update()

if __name__=='__main__':
    game = Puzzle()
