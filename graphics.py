import pygame
import design
import main
import time

BUTTON_HEIGHT = 50
BUTTON_WIDTH = 100
BUTTON_INACTIVE_COLOR = (53, 59, 87)
BUTTON_ACTIVE_COLOR = (98, 12, 37)
FONT_SIZE = 32

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

pygame.init()

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
gameDisplay.fill((255, 255, 255))
pygame.display.set_caption("Cannibals and Missionaries")

gameExit = False

hoveringAction = None
difficultySelected = False
algorithmSelected = False

font = pygame.font.Font("/home/razvan/Desktop/LaburiIA/proiect/8bitlim.ttf", FONT_SIZE)

problema = None
difficulty = None
algorithm = None
solution = []

def textObjects(text, color):
    textSurface = font.render(text, True, color)
    textRectangle = textSurface.get_rect()

    return textSurface, textRectangle

def displayMessage(text, color, x, y, inButton, centered):
    textSurface, textRectangle = textObjects(text, color)

    if inButton:
        textRectangle.center = x + BUTTON_WIDTH / 2, y + BUTTON_HEIGHT / 2
    elif centered:
        textRectangle.center = x, y
    else:
        textRectangle.topleft = x, y

    gameDisplay.blit(textSurface, textRectangle)

def hovering(action):
    global hoveringAction

    if hoveringAction is None:
        hoveringAction = action

def notHovering(action):
    global hoveringAction

    if hoveringAction is action:
        hoveringAction = None

def generateButton(text, x, y, action=None):
    global algorithm, difficulty, problema

    mousePosition = pygame.mouse.get_pos()
    mouseClicked = pygame.mouse.get_pressed()

    global hoveringAction, difficultySelected, algorithmSelected, solution

    if x + BUTTON_WIDTH > mousePosition[0] > x and y + BUTTON_HEIGHT > mousePosition[1] > y:
        pygame.draw.rect(gameDisplay, BUTTON_ACTIVE_COLOR, [x, y, BUTTON_WIDTH, BUTTON_HEIGHT])

        if not difficultySelected:
            if action == "Easy":
                displayMessage("Three cannibals, three missionaries,",(0, 0, 0), WINDOW_WIDTH / 2, 150, False, True)
                displayMessage("boat of two", (0, 0, 0), WINDOW_WIDTH / 2, 200, False, True)
                hovering(action)
            elif action == "Medium":
                displayMessage("Five cannibals, five missionaries,", (0, 0, 0), WINDOW_WIDTH / 2, 150, False, True)
                displayMessage("boat of three", (0, 0, 0), WINDOW_WIDTH / 2, 200, False, True)
                hovering(action)
            elif action == "Hard":
                displayMessage("Eight cannibals, eight missionaries,", (0, 0, 0), WINDOW_WIDTH / 2, 150, False, True)
                displayMessage("boat of four", (0, 0, 0), WINDOW_WIDTH / 2, 200, False, True)
                hovering(action)

        if mouseClicked[0] == 1 and action is not None:
            if action == "goToMenu":
                menu()
            elif action == "startSimulation":
                problema = main.cannibalsProblem(difficulty)

                if algorithm == "DFS":
                    solution = main.depthFirstSearch(problema)
                elif algorithm == "BFS":
                    solution = main.breadthFirstSearch(problema)
                elif algorithm == "UCS":
                    solution = main.uniformCostSearch(problema)
                elif algorithm == "AStar":
                    solution = main.aStarSearch(problema)

                animation()

            if not difficultySelected:
                if action == "Easy":
                    difficulty = 0
                    gameDisplay.fill((255, 255, 255), (0, 125, WINDOW_WIDTH, 275))
                    displayMessage("Easy difficulty selected", (0, 0, 0), WINDOW_WIDTH / 2, 150, False, True)
                    difficultySelected = True
                if action == "Medium":
                    difficulty = 1
                    gameDisplay.fill((255, 255, 255), (0, 125, WINDOW_WIDTH, 275))
                    displayMessage("Medium difficulty selected", (0, 0, 0), WINDOW_WIDTH / 2, 150, False, True)
                    difficultySelected = True
                if action == "Hard":
                    difficulty = 2
                    gameDisplay.fill((255, 255, 255), (0, 125, WINDOW_WIDTH, 275))
                    displayMessage("Hard difficulty selected", (0, 0, 0), WINDOW_WIDTH / 2, 150, False, True)
                    difficultySelected = True

            if not algorithmSelected:
                if action == "DFS":
                    algorithm = "DFS"
                    displayMessage("DFS algorithm selected", (0, 0, 0), WINDOW_WIDTH / 2, 325, False, True)
                    algorithmSelected = True
                if action == "BFS":
                    algorithm = "BFS"
                    displayMessage("BFS algorithm selected", (0, 0, 0), WINDOW_WIDTH / 2, 325, False, True)
                    algorithmSelected = True
                if action == "UCS":
                    algorithm = "UCS"
                    displayMessage("UCS algorithm selected", (0, 0, 0), WINDOW_WIDTH / 2, 325, False, True)
                    algorithmSelected = True
                if action == "AStar":
                    algorithm = "AStar"
                    displayMessage("AStar algorithm selected", (0, 0, 0), WINDOW_WIDTH / 2, 325, False, True)
                    algorithmSelected = True

    else:
        pygame.draw.rect(gameDisplay, BUTTON_INACTIVE_COLOR, [x, y, BUTTON_WIDTH, BUTTON_HEIGHT])

        notHovering(action)

        if hoveringAction is None and (action == "Easy" or action == "Hard" or action == "Medium") and not difficultySelected:
            gameDisplay.fill((255, 255, 255), (0, 125, WINDOW_WIDTH, 275))

    displayMessage(text, (255, 255, 255), x, y, True, False)


def intro():
    displayMessage("Made by Pinzariu Razvan and Pop Vlad", (166, 162, 168), 60, 450, False, False)
    gameDisplay.blit(design.titleImage, (90, 140))

    isIntro = True

    while isIntro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        generateButton("Begin", WINDOW_WIDTH / 2 - 50, 350, action = "goToMenu")

        clock.tick(30)
        pygame.display.update()


def menu():

    isMenu = True
    gameDisplay.fill((255, 255, 255))
    displayMessage("Select a difficulty",BUTTON_INACTIVE_COLOR, WINDOW_WIDTH / 2, 25, False, True)

    global difficultySelected

    while isMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        generateButton("Easy", WINDOW_WIDTH / 2 - 200, 60, action="Easy")
        generateButton("Medium", WINDOW_WIDTH / 2 - 50, 60, action="Medium")
        generateButton("Hard", WINDOW_WIDTH / 2 + 100, 60, action="Hard")

        if difficultySelected:
            displayMessage("Select an algorithm", BUTTON_INACTIVE_COLOR, WINDOW_WIDTH / 2, 205, False, True)

            generateButton("DFS", WINDOW_WIDTH / 2 - 275, 240, action="DFS")
            generateButton("BFS", WINDOW_WIDTH / 2 - 125, 240, action="BFS")
            generateButton("UCS", WINDOW_WIDTH / 2 + 25, 240, action="UCS")
            generateButton("AStar", WINDOW_WIDTH / 2 + 175, 240, action="AStar")

        if algorithmSelected:
            generateButton("Begin", WINDOW_WIDTH / 2 - 50, 360, action="startSimulation")

        clock.tick(30)
        pygame.display.update()


boat = design.boat_two_missionaries
arrow = design.arrow_right
boat_x = 100
boat_y = 150
increaseBoatX = 10
increaseBoatY = 0
isAnimation = True
nrCanLeft = 0
nrMisLeft = 0
nrCanRight = 0
nrMisRight = 0

def animation():

    gameDisplay.blit(design.background, (0, 0))

    global boat_x, boat_y, isAnimation, boat, nrCanLeft, nrMisLeft, nrCanRight, nrMisRight, difficulty

    nrCanLeft = problema.getNrIndividuals()
    nrMisLeft = problema.getNrIndividuals()

    for action in solution:
        misMoved = action.count('m')
        canMoved = action.count('c')
        direction = action[len(action) - 1]
        selectBoat(misMoved, canMoved)

        if direction == '>':
            nrMisLeft -= misMoved
            nrCanLeft -= canMoved
        else:
            nrMisRight -= misMoved
            nrCanRight -= canMoved
        isAnimation = True
        while isAnimation:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            gameDisplay.blit(design.background, (0, 0))

            gameDisplay.blit(design.missionary_right, (25, 25))
            gameDisplay.blit(design.cannibal_right, (25, 260))
            displayMessage("x" + str(nrMisLeft), BUTTON_INACTIVE_COLOR, 60, 225, False, True)
            displayMessage("x" + str(nrCanLeft), BUTTON_INACTIVE_COLOR, 60, 475, False, True)

            gameDisplay.blit(design.missionary_left, (530, 25))
            gameDisplay.blit(design.cannibal_left, (530, 260))
            displayMessage("x" + str(nrMisRight), BUTTON_INACTIVE_COLOR, 640, 225, False, True)
            displayMessage("x" + str(nrCanRight), BUTTON_INACTIVE_COLOR, 640, 475, False, True)

            gameDisplay.blit(arrow, (WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT - 100))
            gameDisplay.blit(boat, (boat_x, boat_y))

            if difficulty > 0:
                displayMessage("x" + str(misMoved), BUTTON_INACTIVE_COLOR, boat_x + 150, boat_y, False, True)
                displayMessage("x" + str(canMoved), BUTTON_INACTIVE_COLOR, boat_x + 75, boat_y, False, True)

            boatMovement(misMoved, canMoved)

            clock.tick(15)
            pygame.display.update()

    isAnimation = True
    while isAnimation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.blit(design.background, (0, 0))

        gameDisplay.blit(design.missionary_right, (25, 25))
        gameDisplay.blit(design.cannibal_right, (25, 260))
        displayMessage("x" + str(nrMisLeft), BUTTON_INACTIVE_COLOR, 60, 225, False, True)
        displayMessage("x" + str(nrCanLeft), BUTTON_INACTIVE_COLOR, 60, 475, False, True)

        gameDisplay.blit(design.missionary_left, (530, 25))
        gameDisplay.blit(design.cannibal_left, (530, 260))
        displayMessage("x" + str(nrMisRight), BUTTON_INACTIVE_COLOR, 640, 225, False, True)
        displayMessage("x" + str(nrCanRight), BUTTON_INACTIVE_COLOR, 640, 475, False, True)

        displayMessage("Finished!", BUTTON_INACTIVE_COLOR, WINDOW_WIDTH / 2 , WINDOW_HEIGHT - 100, False, True)
        gameDisplay.blit(boat, (boat_x, boat_y))

        clock.tick(15)
        pygame.display.update()

def selectBoat(nrMis, nrCan):

    global boat, difficulty

    if difficulty > 0:
        boat = design.boat_both
        return

    if nrMis == 2:
        boat = design.boat_two_missionaries
    elif nrMis == 1 & nrCan == 1:
        boat = design.boat_both
    elif nrCan == 2:
        boat = design.boat_two_cannibals
    elif nrCan == 1:
        boat = design.boat_one_cannibal
    elif nrMis == 1:
        boat = design.boat_one_missionary


def updateRight(misMoved, canMoved):
    global nrMisRight, nrCanRight

    nrMisRight += misMoved
    nrCanRight += canMoved


def updateLeft(misMoved, canMoved):
    global nrMisLeft, nrCanLeft

    nrMisLeft += misMoved
    nrCanLeft += canMoved

def boatMovement(misMoved, canMoved):
    global boat_x, boat_y, increaseBoatX, increaseBoatY, arrow, isAnimation
    if boat_x > 400:
        updateRight(misMoved, canMoved)
        arrow = design.arrow_left
        increaseBoatX = -10
        isAnimation = False
    elif boat_x < 100:
        updateLeft(misMoved, canMoved)
        arrow = design.arrow_right
        increaseBoatX = 10
        isAnimation = False

    if 100 <= boat_x < 200:
        increaseBoatY = 10
    elif 200 <= boat_x <= 300:
        increaseBoatY = 0
    elif 300 < boat_x <= 400:
        increaseBoatY = -10

    boat_x += increaseBoatX
    boat_y += increaseBoatY


if __name__ == '__main__':
    intro()
    # animation()
    pygame.quit()
    quit()
