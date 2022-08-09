import pygame
import random

pygame.init()
pygame.display.set_caption('PyTetris')
programIcon = pygame.image.load('Assets/7349954867626017792_1.png')
pygame.display.set_icon(programIcon)
mixer = pygame.mixer
mixer.init()
mixer.music.load('Assets/Music.wav')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Set Screen
Screen = Width, Height = 300, 500
Window = pygame.display.set_mode(Screen)
FPS = 60
Clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 12)

# Cell
Cellsize = 20
Rows = (Height - 130) // Cellsize
Coloumns = Width // Cellsize

# Debug
# print(Rows, Coloumns)


# Define Colors
Tiel = (0, 30, 100)

#Font
font = pygame.font.Font('Fonts/Alternity-8w7J.ttf', 10)
font3 = pygame.font.Font('Fonts/Alternity-8w7J.ttf', 50)
font2 = pygame.font.SysFont('cursive', 25)
font4 = pygame.font.Font('Fonts/CadillacPersonalUseItalic-K7pny.ttf', 10)

# Images
img1 = pygame.image.load('Assets/1.png')
img2 = pygame.image.load('Assets/2.png')
img3 = pygame.image.load('Assets/3.png')
img4 = pygame.image.load('Assets/4.png')

# Dict Of Assets
Assets = {
    1: img1,
    2: img2,
    3: img3,
    4: img4,
}


class Tetramino:
    # matrix
    # 0   1   2   3
    # 4   5   6   7
    # 8   9   10  11
    # 12  13  14  15

    FIGURES = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    }

    TYPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.level = 1
        self.type = random.choice(self.TYPES)
        self.shape = self.FIGURES[self.type]
        self.color = random.randint(1, 4)
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)


class Tetris:
    gridon = False

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.Level = 1
        self.board = [[0 for j in range(cols)] for i in range(rows)]
        self.next = None
        self.gameover = False
        self.newFig()

    def drawgrid(self):
        if (self.gridon == True):
            for i in range(self.rows + 1):
                pygame.draw.line(Window, Tiel, (0, Cellsize * i), (Width, Cellsize * i))
            for J in range(self.cols):
                pygame.draw.line(Window, Tiel, (Cellsize * J, 0), (Cellsize * J, Height), 1)
        else:
            pass

    def newFig(self):
        if not self.next:
            self.next = Tetramino(5, 0)
        self.figure = self.next
        self.next = Tetramino(5, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.rows - 1 or \
                            j + self.figure.x > self.cols - 1 or \
                            j + self.figure.x < 0 or \
                            self.board[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def remove_line(self):
        rerun = False
        for y in range(self.rows - 1, 0, -1):
            is_full = True
            for x in range(0, self.cols):
                if self.board[y][x] == 0:
                    is_full = False

            if is_full:
                del self.board[y]
                self.board.insert(0, [0 for i in range(self.cols)])
                self.score += 1
                if self.score % 10 == 0:
                    self.Level += 1
                rerun = True
        if rerun:
            self.remove_line()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('Assets/Break.wav'))

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.remove_line()
        self.newFig()
        if self.intersects():
            self.gameover = True

    def jump(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def Down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def side(self, dx):
        self.figure.x += dx
        if self.intersects():
            self.figure.x -= dx

    def rotate(self):
        rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = rotation


Counter = 0

movedown = False

tetris = Tetris(Rows, Coloumns)
CanMove = True


# FPS LOOP https://pythonprogramming.altervista.org/pygame-how-to-display-the-frame-rate-fps-on-the-screen/
def UpdateFps():
    fps = 'FPS:' + str(int(Clock.get_fps()))
    Fpstext = font.render(fps, True, pygame.Color('white'))
    return Fpstext


# keep Window Open
Running = True

while Running:
    Window.fill('black')

    tetris.drawgrid()
    Counter += 1
    if Counter >= 10000:
        Counter = 0
    if CanMove:
        if Counter % (FPS // (tetris.Level * 2)) == 0 or movedown:
            if not tetris.gameover:
                tetris.Down()

    # exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Running = False
            if event.key == pygame.K_LEFT:
                tetris.side(-1)
            if event.key == pygame.K_RIGHT:
                tetris.side(1)
            if event.key == pygame.K_UP:
                tetris.rotate()
            if event.key == pygame.K_DOWN:
                movedown = True
            if event.key == pygame.K_SPACE and tetris.gameover == False:
                tetris.jump()
            if event.key == pygame.K_g:
                tetris.gridon = True
            if event.key == pygame.K_p:
                CanMove = not CanMove
            if event.key == pygame.K_r:
                tetris.__init__(Rows, Coloumns)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                movedown = False

    for x in range(Rows):
        for y in range(Coloumns):
            if tetris.board[x][y] > 0:
                val = tetris.board[x][y]
                img = Assets[val]
                Window.blit(img, (y * Cellsize, x * Cellsize))
                pygame.draw.rect(Window,'White', (y * Cellsize, x * Cellsize,
                                              Cellsize, Cellsize), 1)

    for i in range(4):
        for j in range(4):
            if i * 4 + j in tetris.figure.image():
                x = Cellsize * (tetris.figure.x + j)
                y = Cellsize * (tetris.figure.y + i)
                img = Assets[tetris.figure.color]
                Window.blit(img, (x, y))
                pygame.draw.rect(Window, 'White', (x, y, Cellsize, Cellsize), 1)

        # Draw
    pygame.draw.rect(Window, 'blue', (0, Height - 140, Width, 140))
    pygame.draw.rect(Window, 'blue', (0, 0, Width, Height), 3)
    pygame.draw.rect(Window, Tiel, (7, Height - 135, Width - 15, 130))
    Window.blit(UpdateFps(), (245, 370))
    #Screen
    if tetris.gameover:
        rect = pygame.Rect((50, 140, Width - 100, Height - 400))
        pygame.draw.rect(Window, 'BLACK', rect)
        pygame.draw.rect(Window, 'Blue', rect, 2)

        over = font2.render('Game Over', True, 'WHITE')
        msg1 = font2.render('Press R To Restart', True, 'Blue')
        msg2 = font2.render('Press ESC To Quit', True, 'Blue')

        Window.blit(over, (rect.centerx - over.get_width() / 2, rect.y + 10))
        Window.blit(msg1, (rect.centerx - msg1.get_width() / 2, rect.y + 35))
        Window.blit(msg2, (rect.centerx - msg2.get_width() / 2, rect.y + 60))

    # hud
    if tetris.next:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetris.next.image():
                    img = Assets[tetris.next.color]
                    x = Cellsize * (tetris.next.x + j - 4)
                    y = Height - 100 + Cellsize * (tetris.next.y + i)
                    Window.blit(img, (x + 10, y))
                    pygame.draw.rect(Window, 'White', (x + 10, y, Cellsize, Cellsize), 1)

    scoreimg = font3.render(f'{tetris.score}', True, 'white')
    levelimg = font2.render(f'Level : {tetris.Level}', True, 'white')
    Creator = font4.render(f'Lime/Pyro/Creed#9739', True, 'white')

    Window.blit(scoreimg, (250 - scoreimg.get_width() // 2, Height - 110))
    Window.blit(levelimg, (250 - levelimg.get_width() // 2, Height - 30))

    Clock.tick(FPS)
    pygame.display.update()

pygame.quit()
