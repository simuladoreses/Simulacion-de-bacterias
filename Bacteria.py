import pygame, sys
from pygame.locals import *
import random

class Bacteria(pygame.sprite.Sprite):
	def __init__(self, sprite, tamano, position_x, position_y, gram, metabolismo, porcentage_de_adaptacion, adaptacion):
		""" posicion de la bacteria en la simulacion
			gram: definir si la bacteria es gram positiva:True o negativa:False"""
		pygame.sprite.Sprite.__init__(self)

		#sprite de la bacteria
		self.sprite = pygame.image.load(sprite) if sprite else pygame.image.load("sprites/bacteria.png")
		self.tamano = tamano if tamano else random.randint(10,30) #checar el tama;o
		self.sprite = pygame.transform.scale(self.sprite, (self.tamano, self.tamano))
		self.sprite_de_bacteria = self.sprite.get_rect()

		#variables de la bacteria
		self.sprite_de_bacteria.centerx = position_x
		self.sprite_de_bacteria.centery = position_y
		self.gram = gram if gram else True
		self.salud = 100
		self.energia = random.randint(0, 100)
		self.reproduccion = False
		self.pared_celular = 100 if self.gram else 8
		self.metabolismo = random.randint(1, 9) / 10 
		self.porcentage_de_adaptacion = porcentage_de_adaptacion if porcentage_de_adaptacion else random.randint(1, 5) / 10
		self.adaptacion = adaptacion if adaptacion else 0.0
		self.tiempo = 0
		self.consumo_de_energia = consumo_de_energia if consumo_de_energia else (random.randint(3, 6) / 10) * -1

	def termorecepcion(self, temperatura):
		if temperatura < 5:
			self.salud -= 10
		elif temperatura > 5 and temperatura < 15:
			self.salud -= 0.5
		elif temperatura > 15 and temperatura < 30:
			self.salud -= 0.1
		elif temperatura > 30 and temperatura < 40:
			self.salud = self.salud
		elif temperatura > 40 and temperatura < 50:
			self.salud -= 0.1
		elif temperatura > 50 and temperatura < 60:
			self.salud -= 0.5
		elif temperatura > 60: 
			self.salud -= 10

	def sensacion_de_humedad(self, porcentage):
		if porcentage >= 0 and porcentage <= 20:
			self.salud -= 2
		elif porcentage > 20 and porcentage <= 40: 
			self.salud -= 1
		elif porcentage > 40 and porcentage <= 60 and self.salud <= 100: 
			self.salud += 0.01
		elif porcentage > 60 and porcentage <= 80 and self.salud <= 100: 
			self.salud += 0.1
		elif porcentage > 80 and porcentage <= 100 and self.salud <= 100: 
			self.salud += 0.2

	def sensacion_de_acidez(self, pH):
		#pH 7 es neutro, < es acido, > 7 es base
		if pH > 7.0 and pH < 8.0:
			self.salud = self.salud
		elif pH > 4.0 and pH < 7.0:
			self.salud -= 0.3 
		elif pH > 1.0 and pH < 4.0:
			self.salud -= 0.5
		elif pH > 8.0 and pH < 11.0:
			self.salud -= 0.3
		elif pH > 11.0 and pH < 14.0:
			self.salud -= 0.5

	def ingerir_nutrientes(self, nutrinte):
		if self.energia < 100:
			self.energia += nutrinte * self.metabolismo
		elif self.energia > 100: 
			self.energia = 90

	def receptor_de_antibiotico(self, daño):
		pass

	def verificar_reproduccion(self):
		if self.energia > 95 and self.energia < 100 and self.adaptacion > 90:
			self.energia -= 50
			return True
		else: return False

	def verificar_energia(self):
		self.energia += self.consumo_de_energia - 0.1
		return self.energia
	
	def verificar_salud(self):
		return self.salud

	def establecer_adaptacion(self):
		self.adaptacion += self.porcentage_de_adaptacion 

	def colocar_bacteria(self, window):
		window.blit(self.sprite, self.sprite_de_bacteria)

	def cordenadas(self):
		return self.sprite_de_bacteria.centerx, self.sprite_de_bacteria.centery

	def movimiento(self):
		self.sprite_de_bacteria.centerx += random.randint(-1, 1) 
		self.sprite_de_bacteria.centery += random.randint(-1, 1)
