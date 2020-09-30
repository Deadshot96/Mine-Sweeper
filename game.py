import pygame, os, random

# COLORS
BLACK = (20, 20, 20)
WHITE = (250, 250, 250)
GREY = (170, 170, 170)
GREY_LINE = (100, 100, 100)
RED = (240, 20, 20)
GREEN = (20, 240, 20)
BLUE = (20, 20, 240)
YELLOW = (240, 240, 20)

class Spot:
  def __init__(self, row, col, size):
    self.row = row
    self.col = col
    self.size = size
    self.color = GREY
    self.x = self.col * self.size
    self.y = self.row * self.size
    self.isMine = False
    self.reveled = False
    self.isTagged = False
    self.images = None
    self.neighbours = 0
    self.isDetonated = False
    
  def make_mine(self):
    self.isMine = True
        
  def is_mine(self):
    return self.isMine

  def get_row(self):
    return self.row

  def get_col(self):
    return self.col

  def get_dims(self):
    return self.row, self.col

  def is_reveled(self):
    return self.reveled

  def is_empty(self):
    return self.neighbours == 0

  def reveal(self):
    self.reveled = True
    self.untag()
    self.color = GREY_LINE

  def get_neighbours(self):
    return self.neighbours

  def is_tagged(self):
    return self.isTagged

  def tag(self):
    self.isTagged = True

  def untag(self):
    self.isTagged = False

  def set_neighbours(self, neighbours):
    self.neighbours = neighbours

  def inc_neighbours(self):
    self.neighbours += 1

  def detonate(self):
    self.isDetonated = True

  def is_detonated(self):
    return self.isDetonated
  
  def draw(self, win, imgs):

    if not self.is_reveled():
      if self.is_tagged():
        win.blit(imgs[11], (self.x, self.y))
      else:
        win.blit(imgs[10], (self.x, self.y))

    else:
      if self.is_mine():
        if self.is_detonated():
          win.blit(imgs[12], (self.x, self.y))
        else:
          win.blit(imgs[9], (self.x, self.y))
      else:
        win.blit(imgs[self.neighbours], (self.x, self.y))


        
class Game:
    
  asset_dir = os.path.join(os.getcwd(), 'assets_minesweeper')
  FPS = 60
  IMG_LIST = ['0.png', '1.png', '2.png', '3.png', '4.png',
        '5.png', '6.png', '7.png', '8.png', 'bomb.png',
        'facingDown.png', 'flagged.png', 'boom.png']

  def __init__(self):

    self.width = 600
    self.height = 600
    self.gameWidth = 500
    self.gameHeight = 500
    self.size = 25
    self.xoff = (self.width - self.gameWidth) // 2
    self.yoff = int((self.height - self.gameHeight) * 0.8)
    self.grid = None
    self.titleFont = None
    self.textFont = None
    self.rows = self.gameHeight // self.size
    self.cols = self.gameWidth // self.size
    self.win = None
    self.gameWin = None
    self.clock = None
    self.images = None
    self.numMines = 50
    self.mines = list()
    self.lost = False
    self.won = False
    self.checkedMines = 0

    self.load_images()

  def newGame(self):
    self.grid_init()
    self.mine_init()
    self.update_neighbours()
    self.checkedMines = 0
    self.lost = False


  def game_init(self):

    self.newGame()
    pygame.init()
    pygame.font.init()

    self.win = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("Minesweeper")

    self.gameWin = self.win.subsurface((self.xoff, self.yoff, self.gameWidth, self.gameHeight))

    self.win.fill(BLACK)
    self.gameWin.fill(GREY_LINE)
    pygame.display.update()

    self.clock = pygame.time.Clock()
    self.titleFont = pygame.font.SysFont('comicsansms', 50)
    self.textFont = pygame.font.SysFont('comicsans', self.size)


  def draw(self, win):
    self.draw_grid(win)
    #self.draw_lines(win)
    pygame.display.update()

  def load_images(self):

    self.images = list()
    for imgName in self.IMG_LIST:
      img = pygame.image.load(os.path.join(self.asset_dir, imgName))
      img = pygame.transform.scale(img, (self.size, self.size))
      self.images.append(img)

  def grid_init(self):
    self.grid = list()
    for row in range(self.rows):
      self.grid.append(list())
      for col in range(self.cols):
        spot = Spot(row, col, self.size)
        #spot.reveal()
        self.grid[row].append(spot)


  def mine_init(self):

    if self.grid is None:
      self.grid_init()

    xRange = range(0, self.cols)
    yRange = range(0, self.rows)
    self.mines = list()

    while len(self.mines) != self.numMines:

      row = random.choice(yRange)
      col = random.choice(xRange)

      spot = self.grid[row][col]

      if spot not in self.mines:
        spot.make_mine()
        #spot.reveal()
        self.mines.append(spot)


  def update_neighbours(self):

  # Update Neighbours
    for mine in self.mines:
      row, col = mine.get_dims()

      for i in (-1, 0, 1):
        for j in (-1, 0, 1):

          if self.isValidDims(row + i, col + j):
            spot = self.grid[row + i][col + j]
            if not spot.is_mine():
              spot.inc_neighbours()


  def isValidDims(self, row, col):
    if row in range(0, self.rows) and col in range(0, self.cols):
      return True
    return False


  def draw_grid(self, win):
    for row in self.grid:
      for spot in row:
        spot.draw(win, self.images)


  def reveal(self, row, col):
    spot = self.grid[row][col]
    row, col = spot.get_dims()

    if not spot.is_mine() and not spot.is_tagged():
      spot.reveal()

      if spot.is_empty():
        for i in (-1, 0, 1):
          for j in (-1, 0, 1):
            newRow = row + i
            newCol = col + j
            if self.isValidDims(newRow, newCol):
              newSpot = self.grid[newRow][newCol]

              if not newSpot.is_reveled():
                self.reveal(newRow, newCol)


  def checkFlag(self, row, col):
    spot = self.grid[row][col]
    if not spot.is_reveled():
      if spot.is_tagged():
        spot.untag()

        if spot.is_mine():
          self.checkedMines -= 1

      else:
        spot.tag()

        if spot.is_mine():
          self.checkedMines += 1


  def get_loc(self, pos):
    x, y = pos

    x -= self.xoff
    y -= self.yoff

    row = y // self.size
    col = x // self.size
    return row, col

  def lose(self):
    for mine in self.mines:
      mine.reveal()


  def draw_lines(self, win):

    color = GREY_LINE
    width, height = win.get_size()
    gapX = width // self.rows
    gapY = height // self.cols

    for x in range(0, width, gapX):
      pygame.draw.line(win, color, (x, 0), (x, height), 2)

    for y in range(0, height, gapY):
      pygame.draw.line(win, color, (0, y), (width, y), 2)


    pygame.draw.line(win, color, (0, height - 2), (width, height - 2), 2)
    pygame.draw.line(win, color, (width - 2, 0), (width - 2, height), 2)


  def run(self):

    self.game_init()

    # Title
    text = self.titleFont.render("Minesweeper Developer", 1, YELLOW)
    self.win.blit(text, ((self.width - text.get_width()) // 2, 
                       (self.yoff - 5 - text.get_height()) // 2))
    pygame.display.update()



    run = True
    while run:
      self.clock.tick(self.FPS)


      for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

          keys = pygame.key.get_pressed()

          if keys[pygame.K_ESCAPE]:
            self.newGame()

        if event.type == pygame.MOUSEBUTTONDOWN and not self.lost:

          pressed = pygame.mouse.get_pressed()
          pos = pygame.mouse.get_pos()
          row, col = self.get_loc(pos)

          #print(row, col, sep='\t\t')

          if self.isValidDims(row, col):
            if pressed[0]:
              spot = self.grid[row][col]

              if spot.is_mine() and not spot.is_tagged():
                self.lost = True
                spot.detonate()
                self.lose()
                self.draw(self.gameWin)
              elif not spot.is_tagged():
                self.reveal(row, col)

            elif pressed[2]:
              self.checkFlag(row, col)

      if self.lost:
        continue

      if self.numMines == self.checkedMines:
        self.won = True

      self.draw(self.gameWin)

    pygame.font.quit()
    pygame.quit()
    
X = Game()
X.run()
