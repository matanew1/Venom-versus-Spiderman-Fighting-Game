import random
import pygame
from venom_fight_game.settings import *


class Player:
    def __init__(self, app, hp, screen, name, pos):
        self.app = app
        self.pressed_key = None
        self.name = name
        self.pos = pos
        self.offset_x = 15
        self.offset_y = 15
        self.jump = False
        self.hp = hp
        self.alive = True
        self.animation_lst = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.screen = screen
        self.damage = 5
        self.animation_cool_down = 60
        self.image = None

    def setSpriteSheet(self, low, high, a, b):
        for i in range(low, high):
            player = pygame.image.load(f'images/{i}.png')
            player = pygame.transform.flip(player, a, b)
            self.animation_lst.append(player)

    def draw_player(self, pos=PLAYER_START_POS):
        if self.app.player.alive is False:
            self.animation_cool_down = 50
            self.setSpriteSheet(600, 608, True, True)  # venom dead
            if self.frame_index < len(self.animation_lst):
                self.image = self.animation_lst[self.frame_index]
            self.screen.blit(self.image, vec(pos.x, pos.y + 10))
        else:
            if self.app.enemy.alive is False:
                self.animation_cool_down = 120
                self.setSpriteSheet(300, 303, False, False)  # venom celebrate
                if self.frame_index < len(self.animation_lst):
                    self.image = self.animation_lst[self.frame_index]
                self.screen.blit(self.image, vec(pos.x - 150, pos.y - 60))
            else:
                if self.app.attack_p is False:
                    self.setSpriteSheet(30, 43, False, False)
                    if self.frame_index < len(self.animation_lst):
                        self.image = self.animation_lst[self.frame_index]
                    self.screen.blit(self.image, pos)
                else:
                    if self.pressed_key == 'v':
                        self.setSpriteSheet(2, 7, False, False)
                        if self.frame_index < len(self.animation_lst):
                            self.image = self.animation_lst[self.frame_index]
                        self.screen.blit(self.image, pos)

    def draw_enemy(self, pos=ENEMY_START_POS):
        if self.app.enemy.alive is False:
            self.animation_cool_down = 180
            self.setSpriteSheet(500, 506, True, False)  # spider man dead
            if self.frame_index < len(self.animation_lst):
                self.image = self.animation_lst[self.frame_index]
            self.screen.blit(self.image, pos)
        else:
            if self.app.player.alive is False:
                self.animation_cool_down = 110
                self.setSpriteSheet(400, 405, True, False)  # spider man celebrate
                if self.frame_index < len(self.animation_lst):
                    self.image = self.animation_lst[self.frame_index]
                self.screen.blit(self.image, ENEMY_STATIC_POS)
            else:
                if self.app.attack_e is False:
                    self.setSpriteSheet(50, 58, True, False)
                    if self.frame_index < len(self.animation_lst):
                        self.image = self.animation_lst[self.frame_index]
                    self.screen.blit(self.image, pos)
                else:
                    if self.pressed_key == 'k':
                        self.setSpriteSheet(60, 66, True, False)
                        if self.frame_index < len(self.animation_lst):
                            self.image = self.animation_lst[self.frame_index]
                        self.screen.blit(self.image, pos)

    def update(self, attack):
        if self.frame_index < len(self.animation_lst):
            self.image = self.animation_lst[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > self.animation_cool_down:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_lst):
            if attack == self.app.attack_e and self.app.attack_e is True:
                self.app.attack_e = self.idle(self.app.enemy)
            else:
                self.frame_index = 0
            if attack == self.app.attack_p and self.app.attack_p is True:
                self.app.attack_p = self.idle(self.app.player)
            else:
                self.frame_index = 0
        self.animation_lst.clear()

    def idle(self, player):
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        if player == self.app.player:
            enemy = self.app.enemy
            if player.pos.x in range(int(enemy.pos.x) - 220, int(enemy.pos.x) + 220) and enemy.alive:
                if enemy.hp > 0:
                    enemy.hp -= self.damage + random.randint(-5, 5)
                    if enemy.hp <= 0:
                        enemy.hp = 0
                        enemy.alive = False
                        self.app.winner = player.name
                        self.app.loser = enemy.name
            return False
        if player == self.app.enemy:
            enemy = self.app.player
            if player.pos.x in range(int(enemy.pos.x) - 140, int(enemy.pos.x) + 140) and enemy.alive:
                if enemy.hp > 0:
                    enemy.hp -= self.damage + random.randint(-5, 5)
                    if enemy.hp <= 0:
                        enemy.hp = 0
                        enemy.alive = False
                        self.app.winner = player.name
                        self.app.loser = enemy.name
            return False

    def move(self, user_input, type_key):
        if self.app.player.alive is True and self.app.enemy.alive is True:
            if type_key == 'e':
                if user_input[pygame.K_LEFT]:
                    if self.pos.x - self.offset_x > 0:
                        self.pos.x -= self.offset_x
                if user_input[pygame.K_RIGHT]:
                    if self.pos.x + self.offset_x < WIDTH - 150:
                        self.pos.x += self.offset_x
                if user_input[pygame.K_k] and self.app.enemy.alive is True:
                    self.pressed_key = 'k'
                    self.app.attack_e = True
                    self.draw_enemy()
                if user_input[pygame.K_UP]:
                    self.jump = True
                if self.jump is True:
                    self.pos.y -= self.offset_y
                    self.offset_y -= 1
                    if self.offset_y < -15:
                        self.jump = False
                        self.offset_y = 15
            else:
                if user_input[pygame.K_a]:
                    if self.pos.x - self.offset_x > 0:
                        self.pos.x -= self.offset_x
                if user_input[pygame.K_d]:
                    if self.pos.x + self.offset_x < WIDTH - 150:
                        self.pos.x += self.offset_x
                if user_input[pygame.K_v] and self.app.player.alive is True:
                    self.pressed_key = 'v'
                    self.app.attack_p = True
                    self.draw_player()
                if user_input[pygame.K_w]:
                    self.jump = True
                if self.jump is True:
                    self.pos.y -= self.offset_y
                    self.offset_y -= 1
                    if self.offset_y < -15:
                        self.jump = False
                        self.offset_y = 15
        else:
            if user_input[pygame.K_y]:
                self.app.end = True
                self.app.player.pos = vec(PLAYER_STATIC_POS)
                self.app.enemy.pos = vec(ENEMY_STATIC_POS)
            elif user_input[pygame.K_n]:
                self.app.running = False
