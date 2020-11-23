import pygame
import sys
import random


from pygame.locals import *
from constants import *


def main():
    show_start_menu()
    global time, time1, time2, time3, round_number, timer_time, stage

    stage = 0
    time = None
    points = 0
    round_number = 0
    start_time = None
    lost = False

    three = render_text("3", BLACK, ARIAL, 90)
    two = render_text("2", BLACK, ARIAL, 90)
    one = render_text("1", BLACK, ARIAL, 90)

    pygame.event.set_blocked(MOUSEBUTTONDOWN)

    while running:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate_game()
            elif event.type == KEYDOWN:
                if event.key == K_s and stage == 0:
                    pygame.event.set_blocked(KEYDOWN)
                    root.fill(SILVER)
                    root.blit(three, centre_text(three.get_size()))
                    time = pygame.time.get_ticks()
                    time1 = time + 1000
                    time2 = time + 2000
                    time3 = time + 3000
                elif event.key == K_t and stage == 1:
                    main()
            elif event.type == MOUSEBUTTONDOWN:
                colour_clicked = root.get_at(pygame.mouse.get_pos())[0:-1]
                if colour_clicked != correct_colour_tuple:
                    lost = True
                    show_game_over()
                else:
                    root.fill(SILVER)
                    points += 1
                    round_number += 1
                    if points == POINTS_TO_WIN:  # The number of rounds needed to win
                        show_congrats(timer_time)
                        timer_time = 0
                    else:
                        draw_corner_squares()

        if isinstance(time, (int, float)):
            if pygame.time.get_ticks() >= time3:
                time = None
                root.fill(SILVER)
                draw_corner_squares()
                round_number = 1
                pygame.event.set_allowed(MOUSEBUTTONDOWN)
            elif pygame.time.get_ticks() >= time2:
                root.fill(SILVER)
                root.blit(one, centre_text(one.get_size()))
            elif pygame.time.get_ticks() >= time1:
                root.fill(SILVER)
                root.blit(two, centre_text(two.get_size()))

        if  (0 < round_number < POINTS_TO_WIN + 1) and not lost:
            if not isinstance(start_time, (int, float)):
                start_time = pygame.time.get_ticks()
            timer_time = pygame.time.get_ticks() - start_time
            root.fill(SILVER, rect=[SQUARE_LENGTH, 0, WINDOW_WIDTH - SQUARE_LENGTH*2, SQUARE_LENGTH])
            timer = render_text(f"Time: {timer_time / 1000}", NAVY, ARIAL, 40)
            timer_coords = centre_text(timer.get_size(), pady=-260)
            root.blit(timer, timer_coords)

        pygame.display.update()


def show_congrats(time):
    global stage
    stage = 1
    pygame.event.set_allowed(KEYDOWN)

    game_over_text = render_text("Congratulations!", RED, ARIAL, 60)
    game_over_coords = centre_text(game_over_text.get_size(), pady=-140)

    reason_text = render_text("You clicked all the correct squares", NAVY, ARIAL, 40)
    reason_coords = centre_text(reason_text.get_size(), pady=-40)

    time_text = render_text(f"in {time / 1000} seconds!", NAVY, ARIAL, 40)
    time_coords = centre_text(time_text.get_size(), pady=20)

    challenge_text = render_text(f"Want to improve on your reaction time?", MAROON, ARIAL, 40)
    challenge_coords = centre_text(challenge_text.get_size(), pady=100)

    press_text = render_text("Press the \"t\" key to try again!", YELLOW, ARIAL, 40)
    press_text_coords = centre_text(press_text.get_size(), pady=200)

    root.fill(SILVER)
    root.blit(game_over_text, game_over_coords)
    root.blit(reason_text, reason_coords)
    root.blit(time_text, time_coords)
    root.blit(challenge_text, challenge_coords)
    root.blit(press_text, press_text_coords)


def show_game_over():
    global stage
    stage = 1
    pygame.event.set_allowed(KEYDOWN)

    game_over_text = render_text("GAME OVER !!!", RED, ARIAL, 60)
    game_over_coords = centre_text(game_over_text.get_size(), pady=-80)

    reason_text = render_text("You clicked the wrong square!", NAVY, ARIAL, 45)
    reason_coords = centre_text(reason_text.get_size(), pady=20)

    press_text = render_text("Press the \"t\" key to try again!", YELLOW, ARIAL, 40)
    press_text_coords = centre_text(press_text.get_size(), pady=200)

    root.fill(SILVER)
    root.blit(game_over_text, game_over_coords)
    root.blit(reason_text, reason_coords)
    root.blit(press_text, press_text_coords)


def draw_corner_squares():
    global correct_colour_tuple, correct_colour_text
    correct_colour_tuple = random.choice(ALL_SQUARE_COLOURS)
    correct_colour_text = colours_dict[correct_colour_tuple]

    colour = render_text(correct_colour_text, random.choice(ALL_SQUARE_COLOURS), ARIAL, 50)
    colour_coords = centre_text(colour.get_size(), pady=-50)
    root.blit(colour, colour_coords)

    round_text = render_text(f"Round: {round_number}", OLIVE, ARIAL, 50)
    round_coords = centre_text(round_text.get_size(), pady=230)

    random.shuffle(ALL_SQUARE_COLOURS)
    for i in range(4):
        root.fill(ALL_SQUARE_COLOURS[i], rect=ALL_SQUARES[i])

    pygame.mouse.set_pos(WINDOW_MIDPOINT)
    root.blit(round_text, round_coords)


def show_start_menu():
    root.fill(SILVER)

    title = render_text("Welcome To Click The Square!", RED, ARIAL, 40)
    title_coords = centre_text(title.get_size(), pady=-50)

    press_text = render_text("Press the \"s\" key to play the game.", MAROON, ARIAL, 40)
    press_text_coords = centre_text(press_text.get_size(), pady=80)

    root.blit(title, title_coords)
    root.blit(press_text, press_text_coords)

def centre_text(text_size, padx=0, pady=0, centre=WINDOW_MIDPOINT):
    return centre[0] - text_size[0] // 2 + padx, centre[1] - text_size[1] // 2 + pady


def render_text(text, colour, font_type, font_size, antialiasing=True):
    font_type = pygame.font.SysFont(font_type, font_size)
    return font_type.render(text, antialiasing, colour)


def terminate_game():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    stage = 0
    pygame.init()
    root = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Click The Square")
    main()
