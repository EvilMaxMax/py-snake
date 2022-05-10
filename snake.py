import pygame


class Snake(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.length = 1
        self.size = 20
        self.body = [(x, y)]
        self.head_img = img

    def GetHeadPos(self):
        return self.x, self.y

    def GetLength(self):
        return self.length

    def Move(self, x, y):
        speed = self.size

        dx = x * speed
        dy = y * speed

        self.x += dx
        self.y += dy

        self.body.append((self.x, self.y))

        if len(self.body) > self.length:
            del self.body[0]

    def CheckBoundary(self, width, height):
        self.x = self.x % (width - self.size)
        self.y = self.y % height

    def CheckSelfCollision(self):
        head = (self.x, self.y)

        for part in self.body[:-1]:
            if head == part:
                return True

        return False

    def Draw(self, game_display, direction, color):
        head = self.head_img

        if direction == "right":
            head = pygame.transform.rotate(self.head_img, 270)
        if direction == "left":
            head = pygame.transform.rotate(self.head_img, 90)
        if direction == "down":
            head = pygame.transform.rotate(self.head_img, 180)

        game_display.blit(head, (self.body[-1][0], self.body[-1][1]))

        for x in self.body[:-1]:
            pygame.draw.rect(game_display, color, (x[0], x[1], self.size, self.size))

    def AddBody(self):
        self.length += 1

    def GetRect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
