import pygame


class Block(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def Draw(self, game_display, color):
        pygame.draw.rect(game_display, color, (self.x, self.y, self.width, self.height))

    def GetPos(self):
        return self.x, self.y

    def GetRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def Create(width, height, level):
    blocks = list()

    if level == 1:
        blocks.append(Block(0, 0, int(width / 3), 20))
        blocks.append(Block(0, 0, 20, int(height / 3)))
        blocks.append(Block(width - int(width / 3), 0, int(width / 3), 20))
        blocks.append(Block(width - 20, 0, 20, int(height / 3)))
        blocks.append(Block(0, height - 20, int(width / 3), 20))
        blocks.append(Block(0, height - int(height / 3), 20, int(height / 3)))
        blocks.append(Block(width - int(width / 3), height - 20, int(width / 3), 20))
        blocks.append(Block(width - 20, height - int(height / 3), 20, int(height / 3)))
    elif level == 2:
        blocks.append(Block(0, 0, width, 20))
        blocks.append(Block(0, 0, 20, height))
        blocks.append(Block(0, height - 20, width, 20))
        blocks.append(Block(width - 20, 0, 20, height))

    return blocks
