import random
import pygame

pygame.init()


def get_content(): # for tile inside generation
    r = random.random()  # Generates a float between 0.0 and 1.0
    if r < 0.05:
        return "treasure"
    elif r < 0.08:  
        return "small_potion"
    elif r < 0.10:  
        return "potion"
    elif r < 0.12:
        return "toxic_potion"
    elif r < 0.20:  
        return "enemy"
    elif r < 0.24:  
        return "treasure"
    else:
        return "empty"
    
def interact():
    global images
    global running
    screen.blit(images["player"], (world.width / 5, world.height / 3))
    
    x, y = player.pos #check player pos and display item at that pos
    screen.blit(images[world.map[y][x][1]], (world.width / 5 * 4, world.height / 3))
    
    if world.map[y][x][1] == "treasure":
        player.fame += 10
        print("+10 Fame: Treasure Found.")
        
    elif world.map[y][x][1] == "small_potion":
        player.health += 10
        print("+10 Health: Potion Consumed.")
        
    elif world.map[y][x][1] == "potion":
        player.health += 20
        print("+20 Health: Potion Consumed.")
        
    elif world.map[y][x][1] == "toxic_potion":
        player.health -= 15
        print("-15 Health: Toxic Potion Consumed.")
        
    elif world.map[y][x][1] == "enemy":
        player.health -= 15
        player.fame += 10
        print("-15 Health: Combat Engaged.")
        print("+10 Fame: Killed Enemy.")
        
        if player.health <= 0:
            print("Game Over")
            running = False
            print(f"Your final fame {player.fame}")
        
        
    world.map[y][x][1] = "empty" #puts an old square to empty
    
def check_monsters(world): # verifie si il y a des monstres qui reste dans le monde
    for row in world.map:
        for tile in row:
            if tile[1] == "enemy":
                return True
    return False

def check_all_tiles(world): # verifie si toutes les cases on ete parcourue
    for row in world.map:
        for tile in row:
            if not tile[2]:  # Check if the tile is not visited 
                return False
    return True 

        
        
    
def showstats(screen, width, height, player): # show the stats via a press of s
    global images
    global fame_text
    global hp_text
    
    # Render the text for fame and gold
    fame_text = font.render(f"Fame: {player.fame}", True, (255, 255, 255))  # White color
    heart_text = font.render(f"HP: {player.health}", True, (255, 255, 255))  # White color
    
    pygame.draw.rect(screen, (0, 0, 0), (width/10, height/2, width/10*8, height/3))
    pygame.draw.rect(screen, (150, 75, 0), (width/10 + width/200, height/2 + height/200, width/10*8 - width/140, height/3 - height/140))
    screen.blit(images["fame"], (width/10 + width/30, height/2 + height/30))
    screen.blit(images["heart"], (width/10 + width/5, height/2 + height/30))
    
    # Position the text below the images
    screen.blit(fame_text, (width / 10 + width / 30, height / 3 * 2.1))  # Adjust the y-coordinate
    screen.blit(heart_text, (width / 10 + width / 5, height / 3 * 2.1))  # Adjust the y-coordinate





class Player:
    def __init__(self, name, pos, health, tile_size):
        self.images = (pygame.image.load("playerup.png"),
                       pygame.image.load("playerdown.png"),
                       pygame.image.load("playerleft.png"),
                       pygame.image.load("playerright.png"))
        self.image = self.images[0]
        self.name = name
        self.pos = pos
        self.health = health
        self.tile_size = tile_size
        self.fame = 0
    def move(self, direction):
        if direction == 'up' and self.pos[1] > 0:
            self.pos[1] -= 1
            self.image = self.images[0]
        elif direction == 'down' and self.pos[1] < world.height / world.tile_size - 1:
            self.pos[1] += 1
            self.image = self.images[1]
        elif direction == 'left' and self.pos[0] > 0:
            self.pos[0] -= 1
            self.image = self.images[2]
        elif direction == 'right' and self.pos[0] < world.width / world.tile_size - 1:
            self.pos[0] += 1
            self.image = self.images[3]
            
        if self.check_tile():
            self.interact()

            
    def check_tile(self): #check if tile player is on has something
                    
        # set a new tile to old
        x, y = self.pos
        world.map[y][x][2] = True
        if world.map[y][x][1] != "empty":
            return True
        return False
        
    def interact(self): #do something with it
        x, y = self.pos
        #print(f"Found object {world.map[y][x][1]}")
        global interacting
        interacting = True
            
    
    def draw(self, screen):
        self.image = pygame.transform.scale(self.image, (world.tile_size / 2, world.tile_size / 2))
        screen.blit(self.image, (self.pos[0] * self.tile_size + world.tile_size / 4, self.pos[1] * self.tile_size + world.tile_size / 4))


        

class World:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.map = [[[tile, get_content(), False] for tile in range(int(width / tile_size))] for row in range(int(height / tile_size))]
        self.tile_image = pygame.image.load("tile.png")
        self.old_tile_image = pygame.image.load("old_tile.png") #we need old tiles so people know where they have already walked
        # by default image is 8x8 we need to scale it properly
        self.tile_image = pygame.transform.scale(self.tile_image, (tile_size, tile_size))
        self.old_tile_image = pygame.transform.scale(self.old_tile_image, (tile_size, tile_size))
        
    def draw(self, screen):
        for row in range(len(self.map)):
            for el in range(len(self.map[row])):
                if not self.map[row][el][2]:
                    screen.blit(self.tile_image, (el * self.tile_size, row * self.tile_size))
                else:
                    screen.blit(self.old_tile_image, (el * self.tile_size, row * self.tile_size))

        
        
        


screen_width = 800
screen_height = 600
tile_size = 75

# To ensure the width and height is divisibile by the tile size

screen_width -= screen_width % tile_size
screen_height -= screen_height % tile_size

pygame.font.init()
font = pygame.font.Font(None, round(screen_width / 22))

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Yogis Adventure")

# Create world object
world = World(width=screen_width, height=screen_height, tile_size=tile_size)
player = Player("Aragorn", [0, 0], 100, tile_size)

# Image Files

# Render the text for fame and gold
fame_text = font.render(f"Fame: {player.fame}", True, (255, 255, 255))  # White color
heart_text = font.render(f"HP: {player.health}", True, (255, 255, 255))  # White color
    

# Define the image files and their corresponding keys
image_files = {
    "player": "playerdown.png",
    "enemy": "monster.png",
    "small_potion": "smallpotion.png",
    "potion": "potion.png",
    "toxic_potion": "toxicpotion.png",
    "treasure": "treasure.png",
    "fame": "fame.png",
    "heart": "heart.png",
}

# dictionnary
images = {}

# Load and scale images
for key, file in image_files.items():
    img = pygame.image.load(file)
    img = pygame.transform.scale(img, (world.width // 10, world.width // 10))
    images[key] = img

# access images["player"], images["enemy"], etc.
        
        
running = True
clock = pygame.time.Clock()
pressed_keys = {}

interacting = False #When you land on square with item
color = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.KEYDOWN:
            pressed_keys[event.key] = True
        elif event.type == pygame.KEYUP:
            pressed_keys[event.key] = False
        
        if not interacting:
            if pressed_keys.get(pygame.K_UP, False):
                player.move('up')
            elif pressed_keys.get(pygame.K_DOWN, False):
                player.move('down')
            elif pressed_keys.get(pygame.K_LEFT, False):
                player.move('left')
            elif pressed_keys.get(pygame.K_RIGHT, False):
                player.move('right')
                
            if check_all_tiles(world):
                running = False
    

            
    
    if interacting:
        if color <= 250:
            color += 5
            screen.fill((color, color, color))
            if color > 250:
                interact()
        
        else:
            if pressed_keys.get(pygame.K_q, False):
                interacting = False
                color = 0
                
            showstats(screen, screen_width, screen_height, player)
        
    else:
        # Draw the world
        world.draw(screen)
        player.draw(screen)

        
    if pressed_keys.get(pygame.K_s, False):
        showstats(screen, screen_width, screen_height, player)
        
    
        
    # Update the display
    pygame.display.flip()
    clock.tick(30)  # 30 frames per second
    
    


# le jeu a termine,
clock.tick(500)  # atteinte
screen.fill((0, 0, 0)) # black screen
if not check_monsters(world) and player.health > 0:
    game_over_text = font.render('VICTORY', True, (0, 255, 0))  # Green color
else:
    game_over_text = font.render('GAME OVER', True, (255, 0, 0))  # Red color
    
text_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 3))

screen.blit(game_over_text, text_rect)
showstats(screen, screen_width, screen_height, player)
pygame.display.flip() # display the text

pygame.time.wait(5000)  # wait a moment

# Quit pygame
pygame.quit()

# Missing feature: game doesnt end when all the squares have been cleared


    
    