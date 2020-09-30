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

   
