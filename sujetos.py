import pygame

class sujeto(pygame.sprite.Sprite):
    distancia=100
    contador=0
    def __init__(self, imagen):        
        self.imagen = imagen        
        
        self.rect = self.imagen.get_rect()
        self.rect.top = 200
        self.rect.left = 500+sujeto.distancia*sujeto.contador 
        sujeto.contador+=1

    
              
    def move(self, vx,vy):
        self.rect.move_ip(vx,vy)
    def update(self, superficie):
        superficie.blit(self.imagen,self.rect)  
    
    
        
       
        
class Player(sujeto):
    """Clase del heroe"""
    def __init__(self, imagenes):        
        sujeto.__init__(self,imagenes)        
   