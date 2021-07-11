#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import pygame
from pygame import *

def load_image(name, colorkey=False):
    #crea una ruta a la carpeta de datos
    #al escribirlo de esa forma, nos aseguramos
    #de que pueda abrir en todos los S.O.
    #donde este instalado python
    fullname = os.path.join(name)
    #comprobamos si existe la imagen
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('No se puede cargar la imagen: '), fullname
        raise SystemExit
    #combierte la imagen para que pygame la pueda usar
    image = image.convert()
    #En este punto asignamos el colorkey
    #es decir, un color de base al que se
    #borrara dejando solo el canal alfa (transparencia)
    if colorkey:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    #devuelve la imagen y la recta de la imagen
    return (image, image.get_rect())

"""Mira, el objeto con el que se remplaza el "ratón"..."""
class Mira(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        (self.image, self.rect) = load_image('mira.png', True)
    def update(self):
        posicion = pygame.mouse.get_pos()
        self.rect.center = posicion
        # Evita que la mira salga del rango permitido.
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 450:
            self.rect.right = 450
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 450:
            self.rect.bottom = 450
           
""" Creamos una clase para el botton"""
class OKButton(pygame.sprite.Sprite):
    def __init__(self, initialpos):
        (self.initialx, self.initialy)=initialpos
        pygame.sprite.Sprite.__init__(self)
        (self.image, self.rect) = load_image('Ok.png', True)
    def update(self):
        posicion= self.initialx, self.initialy
        self.rect.center = posicion

"""Clase para guardar"""
class SaveGame():
    def __init__(self):
        pass
    """ Esta seción es una reutilización de código
    def Abrir(self, nombre):
        self.nombre = nombre
        self.archivo = open((self.nombre), "r")
        self.lectura = (self.archivo).readline()
        self.diccionario = ast.literal_eval((self.lectura))
        (self.archivo).close()
        return self.diccionario
    """
    def Guardar(self, nombre, diccionario):
        self.nombre = nombre
        self.diccionario = diccionario
        self.texto =  str(self.diccionario)
        self.archivo = open((self.nombre), "w")
        self.escribir = (self.archivo).write((self.texto))
        (self.archivo).close()
        print ("Puntaje salvado")
    def Info(self):
        print ("""
Este es el modulo encargado de leer y guardar los archivos durante el juego,
"Abrir" se defie como nombre_clase.Abrir("nombredel.archivo")
"Guardar" se define como nombre_clase.Guardar("Nombre del archivo", diccionario_de_datos)
supongo que no tengo que decir que si se guardara otro tipo de dato seria...desastroso"""
        )
class Escritura():
    def __init__(self):
        self.line = 0
        self.strings = ['',]
        #self.font = pygame.font.Font('dejavu.ttf', 12) #(*1)
        self.font = pygame.font.Font(None, 28)
        self.dist = 20
        self.ipos_x = 50
        self.ipos_y = 50
       
    def update(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.strings.append('')
                    self.line += 1
                    print (self.line)
                elif event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_BACKSPACE:
                    if self.strings[self.line] == '' and self.line > 0:
                        self.strings = self.strings[0:-1]
                        self.line -= 1
                    else:
                        self.strings[self.line] = self.strings[self.line][0:-1]
                else:
                    self.strings[self.line] = str(self.strings[self.line] + event.unicode)
                   
    def draw(self, screen):
        #print self.strings, self.line
        screen.fill((0, 0, 0))
        for line in range(len(self.strings)):
            img_line = self.font.render(self.strings[line], 1, (255, 255, 255))
            screen.blit(img_line, (self.ipos_x, self.ipos_y + self.dist * line))
    def que_escribio(self):
        return self.strings[0]#Esto es para salvar solo la primera linea del nombre
           
def main():
    pygame.init()
    screen = pygame.display.set_mode((450, 450))
    pygame.display.set_caption("Guardar Puntos; Escribe tu nombre")
    #pygame.mouse.set_visible(False)
    sprites = pygame.sprite.RenderClear()
    boton = OKButton((400,400))
    pygame.init()
    mira=Mira()
    sprites.add(mira)
    sprites.add(boton)
    salvar = SaveGame()
    escritura = Escritura()
    salir = False
    while salir == False:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                salir = True
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.sprite.collide_rect(mira, boton):
                                #Aqui es donde guardamos y salimos
                                salvar.Guardar("Arch.txt",{"Nombre":escritura.que_escribio(),"Puntaje" :1000})
                                salir = True
        escritura.draw(screen)
        sprites.draw(screen)
        escritura.update(events)
        display.update()
        sprites.update()
        pygame.display.flip()

if __name__ == '__main__':
    main()