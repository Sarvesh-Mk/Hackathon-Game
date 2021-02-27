import pygame
import sys, random
from settings import *
from player import *
from mobs import *

class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.enemies = []
        self.bullets = []
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, "mapexample.txt"))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.Bullets = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.saveMenu = saveMenu(self)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    if self.saveMenu.loadSaveData == True:
                        self.player = Player(
                            self,
                            self.savex,
                            self.savey,
                            self.save_data[2],
                        )
                    else:
                        self.player = Player(self, col, row)
                if tile == 'E':
                   mob(self,col,row)
                   #self.enemies.append(mob)
                if tile == "C":
                    self.chest = Chest(self, col, row)
                if tile == "S":
                    self.door = door(self, col, row, 0, -2)
                if tile == "B":
                    self.door = door(self, col, row, 2, 0)
                if tile == ".":
                    pass
        self.camera = Camera(self.map.width, self.map.height)
        self.mouse = Mouse(pygame.mouse.get_pos(), self)
    
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.update()
            self.draw()
            self.events()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def quit(self):
        pygame.quit()
        sys.exit()


    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.saveMenu.show_save_screen()
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.saveMenu.show_save_screen()
                    self.quit()
            
                if event.key == pygame.K_SPACE and self.player.weapon != "none":
                    if self.player.weapon == "bullet":
                        if self.player.up is True:
                            Bullet(self,self.player.rect.centerx,self.player.rect.centery,0,-10,)

                        if self.player.down is True:
                            Bullet(self,self.player.rect.centerx,self.player.rect.centery,0,-10,)

                        if self.player.right is True:
                            Bullet(self,self.player.rect.centerx,self.player.rect.centery,0,-10,)

                        if self.player.left is True:
                            Bullet(self,self.player.rect.centerx,self.player.rect.centery,0,-10,)


g = Game()
while True:
    g.new()
    g.run()