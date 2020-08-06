# SEAN TOBE
# 11/5/2017

import pygame
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (65, 105, 225)
ORED = (230, 0, 0)
OBLUE = (65, 105, 255)
LIGHTBLUE = (135, 206, 250)
DARKGREEN = (0, 69, 0)
LIGHTGREEN = (0, 130, 35)
WILDGREEN = (50, 255, 50)
BROWN = (225, 132, 69)
ORANGE = (160, 82, 45)
ORANGEY = (165, 42, 42)
PINK = (199, 21, 133)
LIGHTPINK = (255, 192, 203)
YELLOW = (255, 255, 0)


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 300
LVL_LIMIT_TOP = -30
LVL_LIMIT_BTM = 300
SPRITE_WH = 30
WIDESCREEN = (0, 0, 480, 300)


class Player(pygame.sprite.Sprite):
    global progress
    
    def __init__(self):
        
        super().__init__()

        self.image = pygame.Surface([SPRITE_WH, SPRITE_WH])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0
 
        # List of sprites for collions
        self.level = None

        # (0 = Start, 1 = 2D)
        self.progress = 0
 
    def update(self):

        # Keep track of player game progress
        # in order to set level/world rules
        if self.progress == 0:
            collisions = self.level.wall_list
        else:
            collisions = self.level.enemy_list  

        # Move left/right
        self.rect.x += self.change_x
            
        # Check for X collisions
        block_hit_list = pygame.sprite.spritecollide(self, collisions, False)
        for block in block_hit_list:
            # If moving right,
            # set right side to the left side of the objecthit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # If moving left, do the opposite
                self.rect.left = block.rect.right
            self.change_x = 0
            
        # Move up/down
        self.rect.y += self.change_y
 
        # Check for Y collisions
        block_hit_list = pygame.sprite.spritecollide(self, collisions, False)
        for block in block_hit_list:
 
            # Reset position based on the top/bottom of the object hit
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def setProgress(self, num):
        self.progress = num

    # Player-controlled movement:
    def go_left(self):
        self.change_x = -4
 
    def go_right(self):
        self.change_x = 4

    def go_up(self):
        self.change_y = -4
        
    def go_down(self):
        self.change_y = 4
 
    def stop_x(self):
        self.change_x = 0

    def stop_y(self):
        self.change_y = 0

class Block(pygame.sprite.Sprite):

    def __init__(self, Level, c, width, height):

        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.color = None

        # Trees
        if c == 'T':
            self.image.fill(DARKGREEN)
            self.color = DARKGREEN
            Level.wall_list.add(self)
            Level.enemy_list.add(self)
            Level.object_list.add(self)
        # Dirt Trail
        if c == 'D':
            self.image.fill(BROWN)
            self.color = BROWN
            Level.object_list.add(self)
        # Light Grass
        if c == 'O':
            self.image.fill(LIGHTGREEN)
            self.color = LIGHTGREEN
            Level.object_list.add(self)
        # Water
        if c == 'B':
            self.image.fill(LIGHTBLUE)
            self.color = LIGHTBLUE
            Level.wall_list.add(self)
            Level.enemy_list.add(self)
            Level.object_list.add(self)
        # House
        if c == 'H':
            self.image.fill(ORANGE)
            self.color = ORANGE
            Level.enemy_list.add(self)
            Level.object_list.add(self)
        # House2
        if c == 'G':
            self.image.fill(ORANGEY)
            self.color = ORANGEY
            Level.enemy_list.add(self)
            Level.object_list.add(self)
        # Building
        if c == 'L':
            self.image.fill(GRAY)
            self.color = GRAY
            Level.wall_list.add(self)
            Level.enemy_list.add(self)
            Level.object_list.add(self)
        # Building RED
        if c == 'R':
            self.image.fill(ORED)
            self.color = ORED
            Level.wall_list.add(self)
            Level.enemy_list.add(self)
            Level.object_list.add(self)
        # Building BLUE
        if c == 'E':
            self.image.fill(OBLUE)
            self.color = OBLUE
            Level.wall_list.add(self)
            Level.enemy_list.add(self)
            Level.object_list.add(self)
        # Wild Grass
        if c == 'V':
            self.image.fill(WILDGREEN)
            self.color = WILDGREEN
            Level.object_list.add(self)
        # Mother
        if c == 'M':
            self.image.fill(PINK)
            self.color = PINK
            Level.wall_list.add(self)
            Level.enemy_list.add(self)
            Level.object_list.add(self)
        # Neighbor
        if c == 'N':
            self.image.fill(BLUE)
            self.color = BLUE
            Level.wall_list.add(self)
            Level.enemy_list.add(self)
            Level.object_list.add(self)
        # Professor
        if c == 'P':
            self.image.fill(YELLOW)
            self.color = YELLOW
            Level.wall_list.add(self)
            Level.enemy_list.add(self)
            Level.object_list.add(self)

        self.rect = self.image.get_rect()

    def setColor(color):
        self.color = color

class Level():

    def __init__(self, player):
        self.object_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.player = player
 
    # Update everything in the level
    def update(self):
        self.object_list.update()
        self.enemy_list.update()
        self.wall_list.update()
 
    def draw(self, screen): 
        # Draw black background
        screen.fill(BLACK)
 
        # Draw all the sprite lists
        self.object_list.draw(screen)
        self.enemy_list.draw(screen)
        self.wall_list.draw(screen)

class Level_01(Level):
 
    def __init__(self, player):
 
        # Call parent constructor
        Level.__init__(self, player)

        # 16x10 array of levels
        # Characters for specific objects
        if player.progress == 0:
            array = [
                "TTTTTTTTDDTTTTTT",
                "TTOOOOOODDOOOOOT",
                "TTOOOOOODDOHHHOT",
                "TOOHHHHODNDHGHOT",
                "TOOHGGHODDOHGHOT",
                "TOOHHHHODDOHHHOT",
                "TOOODMOODDOOOOOT",
                "TOODDDDDDDOOOBBT",
                "TOODDDDDDDOOBBBT",
                "TTTTTTTTTTTTTTTT",]
        else:
            # Update map for game progress
            array = [
                "TTTTTTTTDDTTTTTT",
                "TTOOOOOODDOOOOOT",
                "TTOOOOOODDOHHHOT",
                "TOOHHHHODDDHGHOT",
                "TOOHGGHODDOHGHOT",
                "TOOHHHHODDOHHHOT",
                "TOOODMOODDOOOOOT",
                "TOODDDDDDDOOOBBT",
                "TOODDDDDDDOOBBBT",
                "TTTTTTTTTTTTTTTT",]
 
        convertLevel(self, array)
        
class Level_02(Level):
 
    def __init__(self, player):
 
        # Call parent constructor
        Level.__init__(self, player)

        # 16x10 array of levels
        # Characters for specific objects
        if player.progress == 0:
            array = [
                "TTTTTTTTTTTTTDDT",
                "TTTTOOOOOOOOODDT",
                "TOOOOOOODDDDDDDT",
                "TVPVVOOODDDDDDDT",
                "TVVVVOOODDOVVVVT",
                "TVVVVVOODDVVVVVT",
                "TVVVVVOODDVVVVVT",
                "TVVVVVOODDTTTVVT",
                "TTTTTTOODDTTTTTT",
                "TTTTTTTTDDTTTTTT",]
        else:
            # Update map for game progress
            array = [
                "TTTTTTTTTTTTTDDT",
                "TTTTOOOOOOOOODDT",
                "TOOOOOOODDDDDDDT",
                "TVVVVOOODDDDDDDT",
                "TVVVVOOODDNVVVVT",
                "TVVVVVOODDVVVVVT",
                "TVVVVVOODDVVVVVT",
                "TVVVVVOODDTTTVVT",
                "TTTTTTOODDTTTTTT",
                "TTTTTTTTDDTTTTTT",]

        convertLevel(self, array)

class Level_03(Level):
 
    def __init__(self, player):
 
        # Call parent constructor
        Level.__init__(self, player)

        # 16x10 array of levels
        # Characters for specific objects
        array = [
            "TTTTTTTTTTTTTTTT",
            "TBBBBBBBPOOVVVVT",
            "TBBBBDDDOOOVVVVT",
            "TBBDDDDDDDOOOOOT",
            "TODDDDDDDDRLLLLT",
            "TODDDOOODDLLLLLT",
            "TODDOOOODDDDDDDT",
            "TLLLEVVVDDDDDDDT",
            "TLLLLVVVVVOOODDT",
            "TTTTTTTTTTTTTDDT",]

        convertLevel(self, array)

def convertLevel(Level, array):
        # Iterate through 2D array and add objects/sprites to the level
        tmp_x = 0
        tmp_y = 0
        for col in array:
            for row in col:
                # Create Block object
                # row = specific character defining type of object/sprite
                obj = Block(Level, row, SPRITE_WH, SPRITE_WH)
                obj.rect.x = tmp_x
                obj.rect.y = tmp_y
                tmp_x += SPRITE_WH
            tmp_x = 0 
            tmp_y += SPRITE_WH

def text_object(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def message(text, delta):
    msgText = pygame.font.Font('PokemonGB.ttf',11)
    TextSurf, TextRect = text_object(text, msgText)
    TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT - delta))
    screen.blit(TextSurf, TextRect)

def messageB(text, delta):
    msgText = pygame.font.Font('PokemonGB.ttf',12)
    TextSurf, TextRect = text_object(text, msgText)
    TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT - delta))
    screen.blit(TextSurf, TextRect)

def messageT(text, delta):
    msgText = pygame.font.Font('PokemonGB.ttf',13)
    TextSurf, TextRect = text_object(text, msgText)
    TextRect.center = (115, delta)
    screen.blit(TextSurf, TextRect)
    
def main():
    global screen
    
    pygame.init()

    # Initialize screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("1-D-MON")

    player = Player()

    # Initialize level list for level switching
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()

    # Initialize player vars/spawn
    player.level = current_level
    player.rect.x = 150
    player.rect.y = 210
    
    active_sprite_list.add(player)

    start = False

    # Title Screen
    while not start:
        pygame.draw.rect(screen, GRAY, WIDESCREEN, 0)
        message("1-D-MON", 50)
        message("Press <Spacebar> to play.", 35)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
        pygame.display.flip()

    # Game vars
    done = False
    clock = pygame.time.Clock()

    # Main Game Loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.go_up()
                if event.key == pygame.K_DOWN:
                    player.go_down()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop_x()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop_x()
                if event.key == pygame.K_UP and player.change_y < 0:
                    player.stop_y()
                if event.key == pygame.K_DOWN and player.change_y > 0:
                    player.stop_y()
                
        active_sprite_list.update()
        current_level.update()

        # Check for next level
        if current_level_no == 0:
            if player.rect.y < LVL_LIMIT_TOP:
                current_level_no += 1
                # Flash screen to indiciate level change
                pygame.draw.rect(screen, WHITE, WIDESCREEN, 0)
                pygame.draw.rect(screen, BLACK, WIDESCREEN, 0)
                current_level = level_list[current_level_no]
                player.level = current_level
                player.rect.y = LVL_LIMIT_BTM - SPRITE_WH
        elif current_level_no == 1:
            if player.rect.y > LVL_LIMIT_BTM:
                current_level_no -= 1
                pygame.draw.rect(screen, WHITE, WIDESCREEN, 0)
                pygame.draw.rect(screen, BLACK, WIDESCREEN, 0)
                current_level = level_list[current_level_no]
                player.level = current_level
                player.rect.y = LVL_LIMIT_TOP + SPRITE_WH
            elif player.rect.y < LVL_LIMIT_TOP:
                current_level_no += 1
                pygame.draw.rect(screen, WHITE, WIDESCREEN, 0)
                pygame.draw.rect(screen, BLACK, WIDESCREEN, 0)
                current_level = level_list[current_level_no]
                player.level = current_level
                player.rect.y = LVL_LIMIT_BTM - SPRITE_WH
        elif current_level_no == 2:
            if player.rect.y > LVL_LIMIT_BTM:
                current_level_no -= 1
                pygame.draw.rect(screen, WHITE, WIDESCREEN, 0)
                pygame.draw.rect(screen, BLACK, WIDESCREEN, 0)
                current_level = level_list[current_level_no]
                player.level = current_level
                player.rect.y = LVL_LIMIT_TOP + SPRITE_WH
                
        # Check for player progress in game (1D/2D)
        if player.progress > 0:
            # Enable 2D Aerial POV
            current_level.draw(screen)
            active_sprite_list.draw(screen)

            # Display Level names
            block_hit_list = pygame.sprite.spritecollide(player, current_level.object_list, False, collided = pygame.sprite.collide_rect_ratio(1.1))
            for block in block_hit_list:
                if current_level_no == 0:
                    messageT("FLAT TOWN", 18)
                if current_level_no == 1:
                    messageT("WILD ROUTE", 18)
                if current_level_no == 2:
                    messageT("MIRAGE LAKESIDE", 18)

            # Enable larger hitboxes for dialogue with characters
            block_hit_list = pygame.sprite.spritecollide(player, current_level.wall_list, False, collided = pygame.sprite.collide_rect_ratio(1.2))
            for block in block_hit_list:
                if block.color == LIGHTBLUE:
                    message("The water is a light sky blue.", 33)
                if block.color == ORED:
                    message("Hello! Do you need healing?", 40)
                if block.color == OBLUE:
                    message("Hello! Do you want to buy anything?", 40)
                if block.color == PINK:
                    print("Mother says..")
                    message("MOTHER:  RED SQUARE, we're here honey!", 61)
                    message("This is Flat Town! I hope you enjoy your", 47)
                    message("time here and have a fun time exploring!!", 33)
                if block.color == BLUE:
                    print("Neighbor says..")
                    message("BLUE SQUARE:  Hey RED SQUARE! How have", 50)
                    message("you been? See anything cool yet?" , 38)
                if block.color == YELLOW:
                    if current_level_no == 1:
                        message("Thank you kind being! As you can tell,", 64)
                        message("you can see much more now.", 47)
                        message("Meet me in the next town to learn more..", 25)
                    elif current_level_no == 2:
                        player.stop_x()
                        player.stop_y()
                        if player.progress == 1:
                            message("My face is reflected in the water.", 75)
                            message("A grin full of hope, or silence and fear...", 61)
                            message("What do you see reflected in your face?", 47)
                            message(".......", 36)
                            message("Oh. You have come to learn more?", 20)
                            message("If so, press <Spacebar>.", 8)
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        # Flash Yellow/White screen
                                        go = False
                                        while not go:
                                            pygame.draw.rect(screen, WHITE, WIDESCREEN, 0)
                                            for event in pygame.event.get():
                                                if event.type == pygame.KEYDOWN:
                                                    go = True
                                            pygame.display.flip()
                                            pygame.draw.rect(screen, YELLOW, WIDESCREEN, 0)
                                            pygame.display.flip()
                                            pygame.draw.rect(screen, WHITE, WIDESCREEN, 0)
                                            pygame.display.flip()
                                            pygame.draw.rect(screen, LIGHTPINK, WIDESCREEN, 0)
                                            pygame.display.flip()
                                                
                                        tmp = Block(current_level, 'O', SPRITE_WH, SPRITE_WH)
                                        tmp.rect.x = 240
                                        tmp.rect.y = 30
                                        block.image = pygame.image.load("mew.gif")
                                        player.setProgress(2)
                                    elif event.key == pygame.K_DOWN:
                                        player.go_down()
                                        break
                                    elif event.key == pygame.K_RIGHT:
                                        player.go_right()
                                        break
                                    elif event.key == pygame.K_LEFT:
                                        player.go_left()
                                        break
                                break
                        elif player.progress == 2:
                            message("I am one of billions of higher beings", 61)
                            message("that dominate this land. We see and", 47)
                            message("perceive 2 whole dimensions above you.", 33)
                            message("You see a point, and we see a plane.", 19)
                            
        else:                
            # Enable 1D Flatlander POV
            block_hit_list = pygame.sprite.spritecollide(player, current_level.object_list, False)
            for block in block_hit_list:
                pygame.draw.rect(screen, block.color, WIDESCREEN, 0)
                # Display Level names
                if current_level_no == 0:
                    messageT("FLAT TOWN", 18)
                if current_level_no == 1:
                    messageT("WILD ROUTE", 18)
                    messageB("HEEELP! Somebody! Anybody!", 75)
                    message("Is there anyone who can hear me?", 61)
                    message("Help me please! I'm in the left-side", 47)
                    message("wild grass!! Aahhhh!", 33)
                if current_level_no == 2:
                    messageT("MIRAGE LAKESIDE", 18)                   

            # Enable larger collision hitbox for wall_list objects
            block_hit_list = pygame.sprite.spritecollide(player, current_level.wall_list, False, collided = pygame.sprite.collide_rect_ratio(1.1))
            for block in block_hit_list:
                pygame.draw.rect(screen, block.color, WIDESCREEN, 0)
                if block.color == DARKGREEN:
                    messageT("FOREST", 18)
                if block.color == LIGHTBLUE:
                    message("The water is a light sky blue.", 33)
                    messageT("FLAT TOWN", 18)
                if block.color == PINK:
                    print("Mother says..")
                    message("MOTHER:  RED SQUARE, we're here honey!", 61)
                    message("This is Flat Town! I hope you enjoy your", 47)
                    message("time here and have a fun time exploring!!", 33)
                    message("I heard a professor lives in town,", 19)
                    message("try following the light brown dirt path.", 5)
                if block.color == BLUE:
                    message("BLUE SQUARE:  Hey RED SQUARE! Welcome to", 61)
                    message("town! But watch out for the wild bright" , 47)
                    message("green grass. There has been word of" , 33)
                    message("unfathomable sights beyond our perception..", 19)
                if block.color == YELLOW:
                    print("Professor says..")
                    # Flash Yellow/White screen
                    go = False
                    while not go:
                        pygame.draw.rect(screen, WHITE, WIDESCREEN, 0)
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                go = True
                        pygame.display.flip()
                        pygame.draw.rect(screen, YELLOW, WIDESCREEN, 0)
                        pygame.display.flip()
                        
                    player.setProgress(1)
                    level_list[0] = Level_01(player)
                    level_list[1] = Level_02(player)

        clock.tick(30)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
