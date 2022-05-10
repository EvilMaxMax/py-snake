import os
import pygame
import random
import tkinter
import tkinter.simpledialog

from food import Food
from snake import Snake
from world import Create, Block

pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()

effect_sound = pygame.mixer.Sound("Resources/effect.wav")
main_sound = pygame.mixer.Sound("Resources/main.wav")
game_sound = pygame.mixer.Sound("Resources/game.wav")
pause_sound = pygame.mixer.Sound("Resources/pause.wav")

effect_sound.set_volume(0.5)
main_sound.set_volume(0.25)
game_sound.set_volume(0.5)
pause_sound.set_volume(0.5)

width = 1000
height = 600

game_display = pygame.display.set_mode((width, height))
game_display.fill((255, 255, 255))

pygame.display.set_caption("Py | Snake Game")
img = pygame.image.load("Resources/head.png")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 35)

FPS = 15

level = 0

scoresFile = open("scores.txt", "r")

scores = {str(x[0: x.rfind(':')]): int(x[x.rfind(':') + 1:]) for x in scoresFile.readlines()}

scoresFile.close()


def draw_text(text, color, interval=0):
    text = font.render(text, True, color)

    game_display.blit(text,
                      (width / 2 - text.get_rect().width / 2, height / 2 - text.get_rect().height / 2 + interval))


def collides_any_block(food_rect, blocks):
    for block in blocks:
        if food_rect.colliderect(block.GetRect()):
            return True

    return False


def game_menu():
    global level

    main_sound.play(-1)

    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    active = False
                    level = 0

                if event.key == pygame.K_2:
                    active = False
                    level = 1

                if event.key == pygame.K_3:
                    active = False
                    level = 2

        draw_text("The Snakes Game", (255, 0, 0), -100)
        draw_text("Press 1 to start EASY!", (0, 0, 255), 50)
        draw_text("Press 2 to start MEDIUM!", (0, 0, 255), 100)
        draw_text("Press 3 to start HARD!", (0, 0, 255), 150)

        draw_text("Press P to pause!", (0, 0, 255), 250)

        pygame.display.update()
        clock.tick(15)


def pause_game(scorestr):
    game_sound.stop()

    pause_sound.play(-1)
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    paused = False

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        draw_text("Paused", (255, 0, 0), -50)
        draw_text("Press SPACE to continue, Q to Quit!", (0, 0, 255), 100)

        pygame.display.update()
        clock.tick(5)

    if not paused:
        pause_sound.stop()
        game_sound.play(-1)


def get_blocks(food_rect, n):
    blocks = list()

    for i in range(n):
        block_x = round(random.randrange(0, width) / 20.0) * 20
        block_y = round(random.randrange(0, height) / 20.0) * 20

        block_width, block_height = 20, 20
        block = Block(block_x, block_y, block_width, block_height)

        if food_rect.colliderect(block.GetRect()):
            i -= 1
        else:
            blocks.append(block)

    return blocks


def game_loop():
    global direction, k, high_score, hs_name, level

    exit_game = False
    over = False

    main_sound.stop()
    game_sound.play(-1)
    score = 0

    snake = Snake(260, 260, img)
    food = Food(int(width / 2), int(height / 2))
    blocks = Create(width, height, level)

    dx, dy = 0, 0
    loss_reason = ""

    direction = "up"

    while not exit_game:
        if over:
            main_sound.play(-1)
        while over:
            draw_text("Press SPACE to retry Q to Quit!", (255, 0, 0), -25)
            draw_text(loss_reason, (255, 0, 0), 30)

            draw_text("Your score: " + str(score), (255, 0, 0), 80)

            if len(scores) == 0:
                max_score = -1
            else:
                max_score = scores[max(scores, key=scores.get)]

            if score > max_score:
                def save_score():
                    name = v.get()
                    scores[name] = score

                    scores_file = open("scores.txt", "w")

                    for key, value in scores.items():
                        scores_file.write(key + ":" + str(value) + "\n")

                    score_window.destroy()

                    scores_file.close()

                score_window = tkinter.Tk()
                score_window.geometry("325x125")
                frame = tkinter.Frame(score_window, width=100, height=100)
                frame.pack()
                score_window.title("New record!")

                tkinter.Label(frame, text="Enter your name below").pack(side="top")
                v = tkinter.StringVar()
                v.set(os.getlogin())
                textbox = tkinter.Entry(frame, textvariable=v)
                textbox.pack(side="top")

                ok_button = tkinter.Button(frame, text="OK", fg="black", bg="white", command=save_score)
                ok_button.pack(side="bottom")

                score_window.mainloop()

                over = True
            else:
                max_score = max(scores, key=scores.get)

                draw_text("Best score by " + max_score + ": " + str(scores[max_score]), (255, 0, 0), 120)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

                    if event.key == pygame.K_SPACE or pygame.K_p:
                        over = False
                        main_sound.stop()
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "right":
                    direction = "left"
                    dx = -1
                    dy = 0

                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "left":
                    direction = "right"
                    dx = 1
                    dy = 0

                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "down":
                    direction = "up"
                    dy = -1
                    dx = 0

                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "up":
                    direction = "down"
                    dy = 1
                    dx = 0

                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    pause_game("Your score: " + str(score))

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit(0)

        snake.Move(dx, dy)
        snake.CheckBoundary(width, height)

        snake_rect = snake.GetRect()
        food_rect = food.GetRect()

        if snake.CheckSelfCollision():
            game_sound.stop()
            over = True
            loss_reason = "Game over!"

        for block in blocks:
            block_rect = block.GetRect()
            if block_rect.colliderect(snake_rect):
                game_sound.stop()
                over = True
                loss_reason = "Game over!"

        if food_rect.colliderect(snake_rect):
            score += 1
            snake.AddBody()

            effect_sound.play()

            food.Create(width, height)

            while collides_any_block(food.GetRect(), blocks):
                food.Create(width - food.size, height - food.size)

        game_display.fill((255, 255, 255))

        snake.Draw(game_display, direction, (0, 255, 0))
        food.Draw(game_display, (255, 0, 0))

        for block in blocks:
            block.Draw(game_display, (0, 0, 0))

        pygame.display.set_caption("Score: " + str(score))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit(0)


game_menu()
game_loop()
