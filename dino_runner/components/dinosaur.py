import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD, HAMMER_TYPE, RUNNING_HAMMER, DUCKING_HAMMER, JUMPING_HAMMER

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUNNING_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}



pygame.mixer.init()
jump = pygame.mixer.Sound('dino_runner/assets/other/Jump.wav') # importei som de jump

X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5
Y_POS_DUCK = 340 # 2 POSICAO DUCK GLOBAL

class Dinosaur (Sprite):
    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUNNING_IMG[self.type][0] # imagem dele correndo
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
        self.setup_state()

    def setup_state(self):
        self.has_power_up = False
        self.shield = False # adicionar mais variavel se for outro item
        self.hammer = False # MEXI AQUI 39
        self.show_text = False
        self.shield_time_up = 0 

    def update(self, user_input):
        if self.dino_run:
            self.run() # chama o metodo de correr

        if self.dino_jump:
            self.jump() # chama o metodo de pulo

        if self.dino_duck:
            self.duck() # 4 CHAMAR METODO DUCK
    
        if self.step_index >= 9: # se a qtd de passos >= a 9
            self.step_index = 0

        # JUMP CHECK # 5 MODIFIQUEI OS IF
        if user_input[pygame.K_UP] and not self.dino_jump: # se o input for UP, e ele nao tiver pulando
            self.dino_jump = True # pulo vira true, e ele sobe
            self.dino_run = False # correndo vira false, pra ele n mexer as pernas
            self.dino_duck = False # duck vira false pra ele n abaixar no ar
            jump.play() # quando pular, toca o som
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True # duck vira true, e ele abaixa
            self.dino_run = False # run vira false pra ele n mexer as pernas (imagem do duck ja tem)
            self.dino_jump = False # jump vira false pra ele n poder pular ( era pra ser assim)
        elif not (self.dino_jump or user_input[pygame.K_DOWN]): # se nao tiver nem dando duck, nem pulando, so vai correr
            self.dino_run = True # volta a correr
            self.dino_duck = False # duck vira false
            self.dino_jump = False # pulo vira false

    # MOVEMENTS FUNCTIONS
    def run(self):
        self.image = RUNNING_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect() # atribui as coordenadas na variavel dino_rect
        self.dino_rect.x = X_POS # rect x = pos X
        self.dino_rect.y = Y_POS # rec y = pox y
        self.step_index += 1 # adiciona +1 a cada passo, para animacao

    def jump(self): # método de pulo
        self.image = JUMP_IMG[self.type] # imagem de pulo
        if self.dino_jump: # se ele tiver pulando
            self.dino_rect.y -= self.jump_vel * 4 # atribui no dino rectY, - jump * 
            self.jump_vel -= 0.8 # velocidade do pulo
        if self.jump_vel < - JUMP_VEL: # se a velocidade do pulo for menor que - 8.5
            self.dino_rect.y = Y_POS # 310 = 310
            self.dino_jump = False # nao ta pulando
            self.jump_vel = JUMP_VEL # velocidade do pulo 0.8

    def duck(self): # 6 METODO DUCK
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect() # atribui as coordenadas na variavel dino_rect
        self.dino_rect.x = X_POS # rec X = pos x
        self.dino_rect.y = Y_POS_DUCK # rec y duck = pos duck y
        self.step_index += 1 # adiciona +1 a cada passo, ate totalizar 5 para animação

    def draw(self, screen: pygame.Surface): # desenha na tela, uma imagem
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y)) # desenha na tela, a imagem, através das coordenadas