import pygame
import math
import random
import json

# Initializing game and window dimensions
pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# Fonts 

LETTER_FONT = pygame.font.SysFont("Arial", 30)
WORD_FONT = pygame.font.SysFont("Arial", 40)
TITLE_FONT = pygame.font.SysFont("Arial", 60)

# Button Variables
RADIUS = 20
GAP = 15
letters = []
A = 65 # ASCII
startx = round((WIDTH - (RADIUS*2 + GAP) * 13) // 2)
starty = 400
for i in range(26):
    x = startx + (GAP * 2) + ((RADIUS*2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS*2))
    letters.append([x, y, chr(A+i), True])

# Loading images
images = []
for i in range(7):
    image = pygame.image.load("./hangman_images/hangman" + str(i) +".png")
    images.append(image)


# Game Variables
hangman_status = 0
with open("word_list.json", "r") as file:
    word_list = json.load(file)
guessed = []

# Colours 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw(window, word) -> None:
    """The main draw function for this program.
    """
    window.fill(WHITE)
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))
    display_word = ""
    for letter in word:
        if letter in guessed and letter != " ":
            display_word += letter + " "
        elif letter == " ":
            display_word += "  "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    window.blit(text, (400, 200))

    # Draw Buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            window.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    window.blit(images[hangman_status], (150, 100))
    pygame.display.update()

def final_message(window, message) -> None:
    """Draws a new screen with <message>"""
    window.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def play_again(window, clock) -> bool:
    """Draws a new screen, asking the player if they want to play again.

    Return True if the player clicks "Yes" and False if the player clicks "No"
    """
    wait = True
    option = True
    window.fill(WHITE)
    text = WORD_FONT.render("Would you like to play again?", 1, BLACK)
    window.blit(text, (WIDTH // 2 - text.get_width()/2, HEIGHT/2 - text.get_height() // 2))
    yes = WORD_FONT.render("Yes", 1, BLACK)
    yes_x = round(WIDTH // 3 - yes.get_width() // 2)
    yes_y = round(3*HEIGHT // 4 - yes.get_height() // 2)
    window.blit(yes, (yes_x, yes_y))
    no = WORD_FONT.render("No", 1, BLACK)
    no_x = round(2*WIDTH // 3 - no.get_width() // 2)
    no_y = round(3*HEIGHT // 4 - no.get_height() // 2)
    window.blit(no, (no_x, no_y))
    pygame.display.update()
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if yes_x <= pos_x <= yes_x + yes.get_width() and yes_y <= pos_y <= yes_y + yes.get_height():
                    wait = False
                    option = True
                elif no_x <= pos_x <= no_x + no.get_width() and no_y <= pos_y <= no_y + no.get_height():
                    wait = False
                    option = False
    if not option:
        pygame.quit()
    return option

def start_screen(window) -> None:
    """Draws the starting screen when the program starts.
    """
    window.fill(WHITE)
    title_text = TITLE_FONT.render("Welcome to Hangman!", 1, BLACK)
    text = WORD_FONT.render("Press any key to continue", 1, BLACK)
    window.blit(title_text, (WIDTH // 2 - (title_text.get_width() // 2), 40))
    window.blit(text, (WIDTH // 2 - (text.get_width() // 2), 300))
    pygame.display.update()
    wait_for_key()


def wait_for_key():
    """Waits for the player to press a key for the game to begin.
    """
    clock = pygame.time.Clock()
    wait = True
    while wait:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wait = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                wait = False

def correct_word(window, word: str) -> None:
    """Draws a screen displaying the correct word if the player loses the game.
    """
    window.fill(WHITE)
    text = WORD_FONT.render(f"The correct word was {word}.", 1, BLACK)
    window.blit(text, (WIDTH/2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2500)


def main():
    """The main function of the program.
    """
    global hangman_status
    # Setting up the game loop
    word = random.choice(word_list).upper()
    FPS = 60
    clock = pygame.time.Clock()
    run = True

    start_screen(window)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        d = math.sqrt((x-mouse_x)**2 + (y-mouse_y)**2)
                        if d <= RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word.replace(" ", ""):
                                hangman_status += 1
        draw(window, word)
        
        won = True
        for letter in word.replace(" ", ""):
            if letter not in guessed:
                won = False
                break   

        if won:
            run = False
            pygame.time.delay(1000)
            final_message(window, "You Won!")
            if play_again(clock):
                won = False
                run = True
                hangman_status = 0
                word = random.choice(word_list).upper()
                guessed.clear()
                for letter in letters:
                    letter[3] = True


        
        if hangman_status == 6:
            run = False
            pygame.time.delay(1000)
            final_message(window, "You Lost!")
            correct_word(window, word)

            if play_again(window, clock):
                won = False
                run = True
                hangman_status = 0
                word = random.choice(word_list).upper()
                guessed.clear()
                for letter in letters:
                    letter[3] = True
            

main()
pygame.quit()
