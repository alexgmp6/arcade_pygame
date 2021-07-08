import pygame

class Letra(pygame.sprite.Sprite):
    distancia=100
    contador=0
    def __init__(self, imagen=None):      
        # Carga las imagenes
        if not imagen:
            imagen=pygame.image.load("data/fuente.png").convert_alpha()
            Letra.contador = 0
            Letra.a_f=[]
            Letra.g_l=[]
            Letra.m_r=[]
            Letra.s_x=[]
            Letra.y_punto=[]
            Letra.coma_bola=[]
            for c in range(6):
                Letra.a_f.append(imagen.subsurface((c*46,0),(46,54)))
                Letra.g_l.append(imagen.subsurface((c*46,54),(46,54)))
                Letra.m_r.append(imagen.subsurface((c*46,108),(46,54)))
                Letra.s_x.append(imagen.subsurface((c*46,162),(46,54)))
                Letra.y_punto.append(imagen.subsurface((c*46,216),(46,54)))
                Letra.coma_bola.append(imagen.subsurface((c*46,270),(46,54)))
            Letra.todas_las_letras = Letra.a_f + Letra.g_l + Letra.m_r + Letra.s_x + Letra.y_punto

        else:
            self.imagen = imagen
            self.rect = self.imagen.get_rect()
            self.rect.top = 200
            self.rect.left = 500+Letra.distancia*Letra.contador 
            Letra.contador+=1

    def text_banner(self, text):
        Letra.contador = 0
        mapping = {
            "a":Letra.todas_las_letras[0],
            "b":Letra.todas_las_letras[1],
            "c":Letra.todas_las_letras[2],
            "d":Letra.todas_las_letras[3],
            "e":Letra.todas_las_letras[4],
            "f":Letra.todas_las_letras[5],
            "g":Letra.todas_las_letras[6],
            "h":Letra.todas_las_letras[7],
            "i":Letra.todas_las_letras[8],
            "j":Letra.todas_las_letras[9],
            "k":Letra.todas_las_letras[10],
            "l":Letra.todas_las_letras[11],
            "m":Letra.todas_las_letras[12],
            "n":Letra.todas_las_letras[13],
            "o":Letra.todas_las_letras[14],
            "p":Letra.todas_las_letras[15],
            "q":Letra.todas_las_letras[16],
            "r":Letra.todas_las_letras[17],
            "s":Letra.todas_las_letras[18],
            "t":Letra.todas_las_letras[19],
            "u":Letra.todas_las_letras[20],
            "v":Letra.todas_las_letras[21],
            "w":Letra.todas_las_letras[22],
            "x":Letra.todas_las_letras[23],
            "y":Letra.todas_las_letras[24],
            "z":Letra.todas_las_letras[25],
            " ":Letra.coma_bola[5]
        }

        banner = []
        for char in text.lower():
            banner.append(Letra(mapping[char]))
        return banner

        
        
    
              
    def move(self, vx,vy):
        self.rect.move_ip(vx,vy)
    def update(self, superficie):
        superficie.blit(self.imagen,self.rect)     
   