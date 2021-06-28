import pygame
import sujetos
import os
import time
import aliens.py

# Constantes
__ANCHO = 640
__ALTO = 480
__VX=2

# Inicializaciones y variables globales
pygame.init()
screen = pygame.display.set_mode((__ANCHO,__ALTO))
pygame.display.set_caption("cartel")
reloj = pygame.time.Clock()

# Carga las imagenes
imagen=pygame.image.load("fuente.png").convert_alpha()  
#276ancho 46px anchocada simbolo  y 324px-54 cada bloque alto  
a_f=[]
g_l=[]
m_r=[]
s_x=[]
y_punto=[]
coma_bola=[]
for c in range(6):
    print("vuelta ",c)
    a_f.append(imagen.subsurface((c*46,0),(46,54)))
    g_l.append(imagen.subsurface((c*46,54),(46,54)))
    m_r.append(imagen.subsurface((c*46,108),(46,54)))
    s_x.append(imagen.subsurface((c*46,162),(46,54)))
    y_punto.append(imagen.subsurface((c*46,216),(46,54)))
    coma_bola.append(imagen.subsurface((c*46,270),(46,54)))

def create_players():
    sujetos.contador = 0
    playerG = sujetos.Player(g_l[0])
    playerA = sujetos.Player(a_f[0])
    playerM = sujetos.Player(m_r[0])
    playerE = sujetos.Player(a_f[4])
    player_space = sujetos.Player(coma_bola[5])  # hay que cambiarlo por su valor y en playerO y playerv
    playerO = sujetos.Player(m_r[2])
    playerV = sujetos.Player(s_x[3])
    playerE2 = sujetos.Player(a_f[4])
    playerR = sujetos.Player(m_r[5])
    sprites = [playerG, playerA, playerM, playerE, player_space, playerO, playerV, playerE2, playerR]
    return sprites


def main():
    imagenes=[a_f[0],a_f[1]]

    sprites = create_players()

    sprites_fuera_de_pantalla = []
    
    exit = False   
    vx = 2
    contador=0
    
    while exit != True:     # Bucle principal


        screen.fill((0, 0, 0))

        for sprite in sprites:
            sprite.move(-vx,0)
            sprite.update(screen)
            if sprites[-1].rect.left < -45:
                sprites_fuera_de_pantalla.append(sprites_fuera_de_pantalla)

            if len(sprites_fuera_de_pantalla) == len(sprites):
                sprites = create_players()
                sprites_fuera_de_pantalla = []


        pygame.display.update()


                
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                exit = True                
        
        



            
                
           
                  
        reloj.tick(144)
       
 

# INICIO
if __name__ == '__main__':
    main()
