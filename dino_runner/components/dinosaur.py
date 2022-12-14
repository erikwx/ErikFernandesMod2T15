import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING # 1 IMPORTEI DUCK


X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5
Y_POS_DUCK = 340 # 2 POSICAO DUCK GLOBAL

class Dinosaur (Sprite):
    def __init__(self):
        self.image = RUNNING[0] # imagem dele correndo
        self.dino_rect = self.image.get_rect() # pegar dimensao da imagem
        # POSICOES E PASSOS
        self.dino_rect.x = X_POS # posicao x do rect do dino
        self.dino_rect.y = Y_POS # posicao y do rect do dino
        self.step_index = 0 # contador de passos
        # MOVIMENTOS
        self.dino_run = True # bool dino correndo
        self.dino_jump = False # bool dino pulando
        self.dino_duck = False # bool dino abaixando # 3 CRIEI ATRIBUTO DUCK
        # VELOCIDADES
        self.jump_vel = JUMP_VEL # velocidade do pulo

    def update(self, user_input):
        if self.dino_run:
            self.run() # chama o metodo de correr

        if self.dino_jump:
            self.jump() # chama o metodo de pulo

        if self.dino_duck:
            self.duck() # 4 CHAMAR METODO DUCK
    
        if self.step_index >= 10: # se a qtd de passos >= a 10
            self.step_index = 0

        # JUMP CHECK # 5 MODIFIQUEI OS IF
        if user_input[pygame.K_UP] and not self.dino_jump: # se o input for UP, e ele nao tiver pulando
            self.dino_jump = True # pulo vira true, e ele sobe
            self.dino_run = False # correndo vira false, pra ele n mexer as pernas
            self.dino_duck = False # duck vira false pra ele n abaixar no ar
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True # duck vira true, e ele abaixa
            self.dino_run = False # run vira false pra ele n mexer as pernas (imagem do duck ja tem)
            self.dino_jump = False # jump vira false pra ele n poder pular ( era pra ser assim)
        elif not (self.dino_jump or user_input[pygame.K_DOWN]): # se nao tiver nem dando duck, nem pulando, so vai correr
            self.dino_run = True # volta a correr
            self.dino_duck = False # duck vira false
            self.dino_jump = False # pulo vira false

    # MOVEMENTS FUNCTIONS

    def jump(self): # método de pulo
        self.image = JUMPING # imagem de pulo
        if self.dino_jump: # se ele tiver pulando
            self.dino_rect.y -= self.jump_vel * 4 # atribui no dino rectY, - jump * 
            self.jump_vel -= 0.8 # velocidade do pulo
        
        if self.jump_vel < - JUMP_VEL: # se a velocidade do pulo for menor que - 8.5
            self.dino_rect.y = Y_POS # 310 = 310
            self.dino_jump = False # nao ta pulando
            self.jump_vel = JUMP_VEL # velocidade do pulo 0.8

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1] # a cada 5 passos, alterna a imagem
        self.dino_rect = self.image.get_rect() # atribui as coordenadas na variavel dino_rect
        self.dino_rect.x = X_POS # rect x = pos X
        self.dino_rect.y = Y_POS # rec y = pox y
        self.step_index += 1 # adiciona +1 a cada passo, para animacao

    def duck(self): # 6 METODO DUCK
        self.image = DUCKING[0] if self.step_index < 5 else DUCKING[1] # a cada 5 passos, alterna a imagem
        self.dino_rect = self.image.get_rect() # atribui as coordenadas na variavel dino_rect
        self.dino_rect.x = X_POS # rec X = pos x
        self.dino_rect.y = Y_POS_DUCK # rec y duck = pos duck y
        self.step_index += 1 # adiciona +1 a cada passo, ate totalizar 5 para animação

    def draw(self, screen: pygame.Surface): # desenha na tela, uma imagem
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y)) # desenha na tela, a imagem, através das coordenadas