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
import config
import sprites

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")







def game(winstyle = 0):
    # init pygame
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    # configuramos el modo de pantalla
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #carga de imagenes, asignamos a las clases de sprites
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

    #decoramos la ventana
    icon = pygame.transform.scale(Alien.images[0], (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Arcade Game')
    pygame.mouse.set_visible(0)

    #creamos background
    bgdtile = load_image('background.png')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    #cargamos los efectos
    boom_sound = load_sound('boom.wav')
    shoot_sound = load_sound('car_door.wav')
    power_up_sound=load_sound('powerUP.wav')
    power_up_down=load_sound('smb_pipe.wav')
    game_over_sound=load_sound('smb_gameover.wav')
    if pygame.mixer:
        music = os.path.join(main_dir, 'data', 'music.wav')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    # inicializamos los grupos
    aliens = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    lastalien = pygame.sprite.GroupSingle()

    #asignamos los grupos por defecto
    Player.containers = all
    PowerUp.containers = power_ups, all
    Alien.containers = aliens, all, lastalien
    Shot.containers = shots, all
    Bomb.containers = bombs, all
    Explosion.containers = all
    Score.containers = all

    #creamos algunos valores de inicio
    alienreload = ALIEN_RELOAD
    kills = 0
    clock = pygame.time.Clock()

    #initialize our starting sprites
    player = Player()
    Alien() #nota, esto 'vive' porque entra en un grupo de sprites
    if pygame.font:
        all.add(Score())


    Score.LAST_Score = Score.SCORE
    while player.alive():

        if Score.LAST_Score > 0 and (Score.SCORE % 10) == 0:
            Alien.speed = Alien.speed + 2
            if Alien.life<3:
                Alien.life +=1
            Alien.increase_alien_frequency()
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

        #actualizamos sprites
        all.update()

        #handle player input
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        player.move(direction)
        firing = keystate[K_SPACE] 
        if not player.reloading and firing and len(shots) < config.max_shots:
            Shot(player.gunpos())
            shoot_sound.play()
        player.reloading = firing

        # creamos nuevo alien
        if alienreload:
            alienreload = alienreload - 1
        elif not int(random.random() * Alien.alien_frequency):
            Alien()
            alienreload = ALIEN_RELOAD
 
        # Drop bombs
        if lastalien and not int(random.random() * BOMB_ODDS):
            Bomb(lastalien.sprite)

        # deteccion de colisiones
        for alien in pygame.sprite.spritecollide(player, aliens, 1):
            boom_sound.play()
            Explosion(alien)
            Explosion(player)
            Score.SCORE = Score.SCORE + 1
            Score.LAST_Score = Score.SCORE
            player.kill()

        for alien in pygame.sprite.groupcollide(aliens, shots, 1, 1).keys():
            
            
            """ if alien.getLife()!=0:
                alien.one_life_less()

            else:  """   
            boom_sound.play()
            Explosion(alien)
            Score.SCORE = Score.SCORE + 1
            Score.LAST_Score = Score.SCORE
        
        for power_up in pygame.sprite.spritecollide(player, power_ups, 1):
            power_up.kill()
            power_up_sound.play()   
            config.max_shots =100  
            player.speed=20      
            Shot.images = [load_image('shot2.png')]
            def cargar_bala_original():
                config.max_shots=2
                player.speed=10
                power_up_down.play()
                Shot.images = [load_image('shot.gif')]
            t = Timer(5, cargar_bala_original)
            t.start()


        for bomb in pygame.sprite.spritecollide(player, bombs, 1):
            boom_sound.play()
            Explosion(player)
            Explosion(bomb)
            
            player.kill()

        #pintamos la escena
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        #cap the framerate
        clock.tick(40)
    
    game_over_sound.play()
    
    
    if pygame.mixer:
        pygame.mixer.music.stop()
    pygame.time.wait(4000)
    return game_over.main()