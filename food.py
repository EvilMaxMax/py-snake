import pygame
import random


class Food(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20

    def Create(self, width, height):
        self.x = round(random.randrange(20, width - 20) / 20) * 20
        self.y = round(random.randrange(20, height - 20) / 20) * 20

        return self.x, self.y

    def Draw(self, game_display, color):
        pygame.draw.rect(game_display, color, (self.x, self.y, self.size, self.size))

    def GetPos(self):
        return self.x, self.y

    def GetRect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
