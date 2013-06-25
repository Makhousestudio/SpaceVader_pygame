#T1 - Space Invader Alpha 2 6/25/2013
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
	def event_manager(self,event,Objects):
		keys = pg.key.get_pressed()
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				Objects.append(Bullet(self.rect.center))		
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
		self.rect = pg.Rect(location,(0,25))
	def make_image(self):
		self.image = pg.Surface((0,25)).convert()
		self.image.fill([255,255,255])
		self.image.blit(SHADER,(0,0))

class Bullet:
	def __init__(self, loc):
		self.image = LASER
		self.start_rect = self.image.get_rect(center=loc)
		self.rect = self.start_rect.copy()
		self.done = False
		self.move = [0,0]
		self.speed = 5
	def update(self,Surf):
		self.move[0] += 0
		self.move[1] -= self.speed
		self.rect.topleft = self.start_rect.move(self.move).topleft
		self.remove(Surf)
		Surf.blit(self.image,self.rect)
	def remove(self,Surf):
		if not self.rect.colliderect(Surf.get_rect()):
			self.done = True

class Control:
	def __init__(self):
		self.state = "GAME"
		self.screen = pg.display.get_surface()
		self.Player = Player((60,500),5)
		self.make_obstacles()
		self.Clock = pg.time.Clock()
		self.lti = 0
		self.Objects = []
	def main(self,Surf):
		while True:
			if self.state == "GAME":
				self.eventloop(self.Objects)
				self.update(Surf)
			elif self.state == "DONE":
				break
			pg.display.update()
			self.Player.x_vel = 0
			self.Clock.tick(65)
	def update(self,Surf):
		Surf.blit(bg,Surf.get_rect())
		Surf.blit(label, (0, 0))
		for Obj in self.Objects[:]:
			Obj.update(self.screen)
			if Obj.done:
				self.Objects.remove(Obj)
		self.Player.update(Surf,self.Obstacles)
	def eventloop(self,Objects):
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.Player.x_vel -= self.Player.speed
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.Player.x_vel += self.Player.speed
		for event in pg.event.get():
			if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
				self.state = "DONE"
			self.Player.event_manager(event,self.Objects)
	def make_obstacles(self):
		self.Obstacles = [Block((700,550)),Block((0,550))]
		self.Bull = [Bullet((10,10))]


#################################
if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    SCREENSIZE = (700,600)
    SCREEN = pg.display.set_mode(SCREENSIZE)
    pg.display.set_caption("SPACE VADER BY: EDWIN M. MAK")
    SPACE = pg.image.load('space.jpg').convert_alpha(SCREEN)
    SHIP = pg.image.load("Lun.gif").convert_alpha(SCREEN)
    SHADER = pg.image.load("shader.png").convert_alpha(SCREEN)
    LASER = pg.image.load("laser.gif").convert_alpha(SCREEN)
    myfont = pg.font.SysFont("Comic Sans MS", 20)
    label = myfont.render("Space Vader (WORK IN PROGRESS) | By: Edwin M. Mak", 1, (255,255,255))
    bg = pg.transform.scale(SPACE,SCREENSIZE)
    RunIt = Control()
    RunIt.main(SCREEN)
    pg.quit();sys.exit()
