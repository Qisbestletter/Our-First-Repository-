"""
Alex Valenzuela
Period 4
Final Project
MOTH GAME
Controls:
WASD to move
Click to identify
SPACE to end (once at goal and collected all good fires)
"""

#import the libraries
import pygame
import random

class Player:
    """
    This class represents the player character and their properties
    """
    def __init__(self, x, y, w, h, image):
        """
        :param x: the x coordinate
        :param y: the y coordinate
        :param w: the width
        :param h: the height
        :param image: the player's image
        :param rect: the player's rect: important for collisions
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    #Movement Code
    def move_up(self):
        """
        This function moves the player up
        :return: None
        """
        #move the y value of the player
        self.y -= 10
        #move the rect's value, so it follows the player
        self.rect.y = self.y

    def move_down(self):
        """
        This function moves the player down
        :return: None
        """
        #move the y value of the player
        self.y += 10
        #move the rect's value, so it follows the player
        self.rect.y = self.y

    def move_left(self):
        """
        This function moves the player left
        :return: None
        """
        #move the player's x value
        self.x -= 10
        #move the rect's value, so it follows the player
        self.rect.x = self.x

    def move_right(self):
        """
        This function moves the player right
        :return:
        """
        #move the player's x value
        self.x += 10
        #move the rect's value as well so it can follow the player
        self.rect.x = self.x



class Object:
    """
    This class represents the nonplayer objects and their properties
    """

    def __init__(self, x, y, w, h, image, id):
        """
        :param x: the x coordinate
        :param y: the y coordinate
        :param w: the width
        :param h: the height
        :param image: the object's image
        :param id: whether or not the object is harmful or not
        :param rect: the object's rect: important for collisions
        """

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load(image)
        self.id = id
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def indentify(self):
        return self.id

class Goal:
    """
    This class represents the goal and its properties
    """
    def __init__(self, x, y, w, h, image):
        """
        :param x: the x coordinate
        :param y: the y coordinate
        :param w: the width
        :param h: the height
        :param image: the goal's image
        :param rect: the goal's rect; important for collisions
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

def create_objects(num, list, image, w, h):
    """
    This function creates a set of objects
    :param num: the number of objects the user wants created
    :param list: The list the user wants the objects to be in
    :param image: The image of the objects that will be created
    :param w: The width of the objects
    :param h: The height of the objects
    :return: Nothing: the list itself changes
    """

    for i in range (num):
        list.append(Object(random.randint(0, w), random.randint(0, h), 60, 60, image, random.randint(1,2)))

def main():
    """
    This function is the main fucntion, and sets up the gameplay for the game
    :return:
    """

    #initialize pygame
    pygame.init()

    #CONSTANTS
    WIDTH = 800
    HEIGHT = 600
    PLAYER_IMAGE = "moth.png"
    OBJECT_IMAGE = "fire_no_pass.png"
    OBJECT_PASS_IMAGE = "fire_pass.png"
    GOAL_IMAGE = "orange_goal.png"

    #Create objects and player/ key variables relating to them
    count = 0
    num = int(input("How many objects would you like? "))
    game_objects = []
    create_objects(num, game_objects, OBJECT_IMAGE, WIDTH - 100, HEIGHT - 100)
    for object in game_objects:
        #if the object is to be collected, add to the count of collectable objects
        if object.id == 2:
            count += 1
    player = Player(50,50,50,50, PLAYER_IMAGE)
    goal = Goal(750, 550, 50, 50, GOAL_IMAGE)

    #General Setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    death_color = (0,0,0)

    #loop
    while running:
        screen.fill((0,0,0))
        resize_list = []
        #create objects and player: resize images then blit to screen
        for object in game_objects:
            object_resize = pygame.transform.scale(object.image, (50,50))
            screen.blit(object_resize, (object.x, object.y, object.w, object.h))
        goal_resize = pygame.transform.scale(goal.image, (50,50))
        player_resize = pygame.transform.scale(player.image, (50,50))
        screen.blit(player_resize, (player.x, player.y, player.w, player.h))
        screen.blit(goal_resize, (goal.x, goal.y, goal.w, goal.h))

        for event in pygame.event.get():
            #if the user quits, quit the game
            if event.type == pygame.QUIT:
                running = False
            #if the user clicks the mouse, get the mouse's position and compare to objects rect
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for object in game_objects:
                    #if the mouse and the object collide: reveal whether it's collectable
                    if object.rect.collidepoint(m_x, m_y):
                        #if the id is 2, its collectable: change its image
                        if object.id == 2:
                            object.image = pygame.image.load(OBJECT_PASS_IMAGE)
            #if the user pressed a key, check if it's space
            elif event.type == pygame.KEYDOWN:
                #if the keY was space, check if the player is colliding with anything
                if event.key == pygame.K_SPACE:
                    #if the player is colliding with the goal, check if they're done collecting
                    if player.rect.colliderect(goal.x, goal.y, goal.w, goal.h):
                        #if they're done collecting, end the game and make sure a green screen is displayed
                        if count == 0:
                            running = False
                            death_color = ((0,255,0))
                        #if they're not done, remind them they're not done
                        else:
                            print("You're not done collecting fires")
                    for object in game_objects:
                        #if the player pressed space, check if they're colliding with a fire object
                        if player.rect.colliderect(object.x, object.y, object.w, object.h):
                            #if they are, check if its a harmful one or not
                            if object.id == 1:
                                #if it is a harmful object, end the game and display a red screen
                                running = False
                                death_color = ((255,0,0))
                            #if it's a harmless one, reduce the count and remove the object
                            else:
                                game_objects.remove(object)
                                count -= 1
                #if the key pressed is w, move up
                elif event.key == pygame.K_w:
                    player.move_up()
                #if the key pressed is a, move left
                elif event.key == pygame.K_a:
                    player.move_left()
                #if the key pressed is s, move down
                elif event.key == pygame.K_s:
                    player.move_down()
                #if the key pressed is d, move right
                elif event.key == pygame.K_d:
                    player.move_right()


        pygame.display.flip()
    #when the game is over, display the appropriate color and message
    while not running:

        screen.fill(death_color)
        #if the death color tuple is green, they won: display a green screen and print the win msg
        if death_color == (0,255,0):
            print("YOU WIN!")
        #if the death color tuple is red, that means the user died: display a red screen and loss message
        elif death_color == (255,0,0):
            print("YOU LOST")
        #if the death color tuple is anything else, it means the user quit the game: display the quit message
        else:
            print("YOU GAVE UP :(")

        for event in pygame.event.get():
            #if the user quits, end the game
            if event.type == pygame.QUIT:
                running = True
        pygame.display.flip()

main()


