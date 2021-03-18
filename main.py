import pygame
import os
pygame.font.init()
pygame.mixer.init()
#SOUND EFFECTS
BULLET_HIT_SOUND = pygame.mixer.Sound("assets/Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("assets/Gun+Silencer.mp3")
#Config of window
WIDTH , HEIGHT = 900 , 480
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
#Color
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
#Border
BORDER = pygame.Rect(WIDTH/2 - 5,0,10,HEIGHT)
#Frame per second
FPS = 60
#Name of the window
pygame.display.set_caption("Tank game")
#Tank Characters
    #Image of Tanks
TANK_IMAGE = pygame.image.load(os.path.join("assets","tank.png"))
TANK_SECOND_IMAGE = pygame.image.load(os.path.join("assets","tank1.png"))
    #Properties of tanks
TANK_WIDTH = 160
TANK_HEIGHT = 80
TANK_1_WIDTH = TANK_WIDTH - 20
TANK_1_HEIGHT = TANK_HEIGHT
    #Tank Velocity
TANK_VELOCITY = 2
    #Resizing tank
TANK = pygame.transform.rotate(pygame.transform.scale(TANK_IMAGE,(TANK_WIDTH,TANK_HEIGHT)),180)
TANK_1 = pygame.transform.scale(TANK_SECOND_IMAGE,(TANK_1_WIDTH,TANK_1_HEIGHT))
#Bullet's velocity
BULLET_VELOCITY = 8
#Number of bullets
NUM_BULLETS = 1
#Health
TANK_HIT = pygame.USEREVENT + 1
TANK_1_HIT = pygame.USEREVENT + 2
#Background
BACK = pygame.transform.scale(pygame.image.load(os.path.join("assets","background.jpg")),(WIDTH,HEIGHT))
#FONTS
HEALTH_FONT = pygame.font.SysFont('comicsans', 40,False,False)
WINNER_FONT = pygame.font.SysFont('comicsans',100)
#Graphic function
#HP
TANK_HEALTH = 3
TANK_1_HEALTH = 3
def penetration(health):
    health -= 1
    return health 
def draw(tank,tank_1,first_bullets,second_bullets,health,health1):
    #Fills all the window background
    # WIN.fill(GREEN)
    #DRAW BORDER
    WIN.blit(BACK,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    #HP indicator
    health_text = HEALTH_FONT.render("Health:" + str(health),1,GREEN)
    health1_text = HEALTH_FONT.render("Health:" +str(health1),1,GREEN)
    WIN.blit(health_text,(WIDTH - health_text.get_width(),10))
    WIN.blit(health1_text,(10,10))
    #Shows our tank
    WIN.blit(TANK,(tank.x,tank.y))
    WIN.blit(TANK_1,(tank_1.x,tank_1.y))
    # Bullets
    for bullet in first_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in second_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    #Updates our graphical manipulations
    pygame.display.update()
def tank_movement(keys_pressed,tank):
    #Tank Controlling
        if keys_pressed[pygame.K_a] and tank.x - TANK_VELOCITY > 0: #LEFT
            tank.x -= TANK_VELOCITY
        if keys_pressed[pygame.K_d] and tank.x + TANK_VELOCITY + tank.width < BORDER.x: #RIGHT
            tank.x += TANK_VELOCITY
        if keys_pressed[pygame.K_w] and tank.y - TANK_VELOCITY > 0: #UP
            tank.y -= TANK_VELOCITY
        if keys_pressed[pygame.K_s] and tank.y + TANK_VELOCITY + tank.height < HEIGHT: #DOWN
            tank.y += TANK_VELOCITY
def tank_1_movement(keys_pressed,tank_1):
    #Second tank controlling
        if keys_pressed[pygame.K_LEFT] and  tank_1.x - TANK_VELOCITY - 25 > BORDER.x: #LEFT
            tank_1.x -= TANK_VELOCITY
        if keys_pressed[pygame.K_RIGHT] and tank_1.x + TANK_VELOCITY + TANK_1_WIDTH < WIDTH: #RIGHT
            tank_1.x += TANK_VELOCITY
        if keys_pressed[pygame.K_UP] and tank_1.y - TANK_VELOCITY > 0: #UP
            tank_1.y -= TANK_VELOCITY
        if keys_pressed[pygame.K_DOWN] and tank_1.y + TANK_VELOCITY + tank_1.height < HEIGHT: #DOWN
            tank_1.y += TANK_VELOCITY
def handle_bullets(first_bullets,second_bullets,tank,tank_1):
    for bullet in first_bullets:
        bullet.x += BULLET_VELOCITY
        if tank_1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TANK_1_HIT))
            first_bullets.remove(bullet)
        if bullet.x > WIDTH:
            first_bullets.remove(bullet)

    for bullet in second_bullets:
        bullet.x -= BULLET_VELOCITY
        if tank.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TANK_HIT))
            second_bullets.remove(bullet)
        if bullet.x < 0:
            second_bullets.remove(bullet)
#Winner Function
def draw_winner(text:str):
    draw_text = WINNER_FONT.render(text,1,BLUE)
    WIN.blit(draw_text , (WIDTH/2 - draw_text.get_width()/2,HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
#Main Function
def main():
    #Rectangle player
    tank = pygame.Rect(100,200,TANK_WIDTH,TANK_HEIGHT)
    tank_1 = pygame.Rect(660,200,TANK_1_WIDTH,TANK_1_HEIGHT)
    #Buletts
    first_bullets = []
    second_bullets = []
    #Clock object
    clock = pygame.time.Clock()
    #Run of the game
    run = True
    while run:
        #Giving FPS limit
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(first_bullets) < NUM_BULLETS:
                    bullet = pygame.Rect(tank.x + tank.width, tank.y + tank.height//2 - 2, 10, 5)
                    first_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(second_bullets) < NUM_BULLETS:
                    bullet = pygame.Rect(tank_1.x, tank_1.y + tank_1.height//2 - 2, 10, 5)
                    second_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            global TANK_HEALTH
            global TANK_1_HEALTH
            if event.type == TANK_HIT:
                TANK_1_HEALTH -= 1
                BULLET_HIT_SOUND.play()
                #BULLET_HIT_SOUND.play()

            if event.type == TANK_1_HIT:
                TANK_HEALTH -= 1 
                BULLET_HIT_SOUND.play()
                #BULLET_HIT_SOUND.play()

        winner_text = ""
        if TANK_HEALTH <= 0:
            winner_text = "Left player Wins!"

        if TANK_1_HEALTH <= 0:
            winner_text = "Right player Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        # tank.x += 1
        #Tank Controlling
        keys_pressed = pygame.key.get_pressed()
        keys_1_pressed = pygame.key.get_pressed()
        #Movement function
        tank_movement(keys_pressed,tank)
        tank_1_movement(keys_1_pressed,tank_1)
        #Handling bullets
        handle_bullets(first_bullets,second_bullets,tank,tank_1)
        #Graphiacal update 
        draw(tank,tank_1,first_bullets,second_bullets,TANK_HEALTH,TANK_1_HEALTH)
    pygame.quit()

if __name__ == "__main__":
    main() 