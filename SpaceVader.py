#T1 - Space Invader Alpha 1 6/19/2013
#By: Edwin Mak

import os,sys
from random import randint
import pygame as pg

class Player:
	def __init__(self, location, speed):
		self.image = SHIP
		self.speed = speed
		self.rect = self.image.get_rect()
		self.rect.topleft = location
		self.x_vel = 0
		self.col = []
	def get_pos(self,Obstacles):
		self.collide_with(Obstacles,(0,0))
	def update(self,Surf,Obstacles):
		self.rect.x += self.x_vel
		self.get_pos(Obstacles)
		Surf.blit(self.image,self.rect)
	def collide_with(self,Obstacles,offset):
		test = ((self.rect.x+offset[0],self.rect.y+offset[1]),self.rect.size)
		self.collide_ls = []
		for Obs in Obstacles:
			if pg.Rect(test).colliderect(Obs.rect):
				self.col.append(Obs)
				self.rect.x -= self.x_vel
		return self.col

class Block:
	def __init__(self, location):
		self.make_image()
		self.rect = pg.Rect(location,(50,50))
	def make_image(self):
		self.image = pg.Surface((50,50)).convert()
		self.image.fill([255,255,255])
		self.image.blit(SHADER,(0,0))
	def update(self, Surf):
		Surf.blit(self.image,self.rect)

class Control:
	def __init__(self):
		self.state = "GAME"
		self.Player = Player((60,500),5)
		self.make_obstacles()
		self.Clock = pg.time.Clock()
	def main(self,Surf):
		Surf.fill((0,0,0))
		while True:
			if self.state == "GAME":
				self.eventloop()
				self.update(Surf)
			elif self.state == "DONE":
				break
			pg.display.update()
			self.Player.x_vel = 0
			self.Clock.tick(65)
	def update(self,Surf):
		Surf.fill((0,0,0))
		[obs.update(Surf) for obs in self.Obstacles]
		self.Player.update(Surf,self.Obstacles)
	def eventloop(self):
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT] and self.Player.x_vel >= 0:
			self.Player.x_vel -= self.Player.speed
		if keys[pg.K_RIGHT] and self.Player.x_vel <= 0:
			self.Player.x_vel += self.Player.speed
		for event in pg.event.get():
			if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
				self.state = "DONE"
	def make_obstacles(self):
		self.Obstacles = [Block((650,550)),Block((0,550))]


#################################
if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    SCREENSIZE = (700,600)
    SCREEN = pg.display.set_mode(SCREENSIZE)
    SHIP = pg.image.load("Spaceship.png").convert_alpha(SCREEN)
    SHADER = pg.image.load("shader.png").convert_alpha(SCREEN)
    RunIt = Control()
    RunIt.main(SCREEN)
    pg.quit();sys.exit()
