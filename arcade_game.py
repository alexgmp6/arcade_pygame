#!/usr/bin/env python

import random, os.path

#import basic pygame modules
import pygame
import game_over
from pygame.locals import *
from threading import Timer
from config import *
from load import *
from sprites import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")



# each type of game object gets an init and an
# update function. the update function is called
# once per frame, and it is when each object should
# change it's current position and state. the Player
# object actually gets a "move" function instead of
# update, since it is passed extra information about
# the keyboard



def game(winstyle = 0):
    # Initialize pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup)
    img = load_image('tanque.png')
    Player.images = [img, pygame.transform.flip(img, 1, 0)]
    img = load_image('explosion1.gif')
    Explosion.images = [img, pygame.transform.flip(img, 1, 1)]
    Alien.images = load_images('bicho1.png', 'bicho2.png', 'bicho3.png',
    'bicho4.png','bicho5.png','bicho6.png','bicho7.png','bicho8.png',
    'bicho9.png','bicho10.png','bicho11.png','bicho12.png','bicho13.png',
    'bicho14.png','bicho15.png','bicho16.png')
    PowerUp.images = [load_image('omega.png')]
    Bomb.images = [load_image('bomb.png')]
    Shot.images = [load_image('shot.gif')]

    #decorate the game window
    icon = pygame.transform.scale(Alien.images[0], (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Arcade Game')
    pygame.mouse.set_visible(0)

    #create the background, tile the bgd image
    bgdtile = load_image('background.png')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    #load the sound effects
    boom_sound = load_sound('boom.wav')
    shoot_sound = load_sound('car_door.wav')
    power_up_sound=load_sound('powerUP.wav')
    power_up_down=load_sound('smb_pipe.wav')
    game_over_sound=load_sound('smb_gameover.wav')
    if pygame.mixer:
        music = os.path.join(main_dir, 'data', 'music.wav')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    # Initialize Game Groups
    aliens = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    lastalien = pygame.sprite.GroupSingle()

    #assign default groups to each sprite class
    Player.containers = all
    PowerUp.containers = power_ups, all
    Alien.containers = aliens, all, lastalien
    Shot.containers = shots, all
    Bomb.containers = bombs, all
    Explosion.containers = all
    Score.containers = all

    #Create Some Starting Values
    alienreload = ALIEN_RELOAD
    kills = 0
    clock = pygame.time.Clock()

    #initialize our starting sprites
    player = Player()
    Alien() #note, this 'lives' because it goes into a sprite group
    if pygame.font:
        all.add(Score())


    Score.LAST_Score = Score.SCORE
    while player.alive():

        if Score.LAST_Score > 0 and (Score.SCORE % 10) == 0:
            Alien.speed = Alien.speed + 2
            Score.LAST_Score = 0
            PowerUp((random.randint(1, 600), 1))


        #get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return "QUIT"
        keystate = pygame.key.get_pressed()

        # clear/erase the last drawn sprites
        all.clear(screen, background)

        #update all the sprites
        all.update()

        #handle player input
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        player.move(direction)
        firing = keystate[K_SPACE] 
        if not player.reloading and firing and len(shots) < MAX_SHOTS:
            Shot(player.gunpos())
            shoot_sound.play()
        player.reloading = firing

        # Create new alien
        if alienreload:
            alienreload = alienreload - 1
        elif not int(random.random() * ALIEN_ODDS):
            Alien()
            alienreload = ALIEN_RELOAD
 
        # Drop bombs
        if lastalien and not int(random.random() * BOMB_ODDS):
            Bomb(lastalien.sprite)

        # Detect collisions
        for alien in pygame.sprite.spritecollide(player, aliens, 1):
            boom_sound.play()
            Explosion(alien)
            Explosion(player)
            Score.SCORE = Score.SCORE + 1
            Score.LAST_Score = Score.SCORE
            player.kill()

        for alien in pygame.sprite.groupcollide(shots, aliens, 1, 1).keys():
            boom_sound.play()
            Explosion(alien)
            Score.SCORE = Score.SCORE + 1
            Score.LAST_Score = Score.SCORE
        
        for power_up in pygame.sprite.spritecollide(player, power_ups, 1):
            power_up.kill()
            power_up_sound.play()            
            Shot.images = [load_image('shot2.png')]
            def cargar_bala_original():
                power_up_down.play()
                Shot.images = [load_image('shot.gif')]
            t = Timer(5, cargar_bala_original)
            t.start()


        for bomb in pygame.sprite.spritecollide(player, bombs, 1):
            boom_sound.play()
            Explosion(player)
            Explosion(bomb)
            
            player.kill()

        #draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        #cap the framerate
        clock.tick(40)
    
    game_over_sound.play()
    
    if pygame.mixer:
        pygame.mixer.music.stop()
    pygame.time.wait(3000)
    return game_over.main()