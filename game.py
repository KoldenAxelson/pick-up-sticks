import pygame
import time
from constants import WINDOW_SIZE, MOVEMENT_DELAY
from entities.player import Player
from world.game_world import GameWorld
from renderer import Renderer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Pick Up Sticks')
        self.clock = pygame.time.Clock()
        
        self.player = Player()
        self.world = GameWorld()
        self.renderer = Renderer(self.screen)
        
        self.running = True
        self.last_movement_time = time.time()

    def handle_input(self):
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and not self.player.is_moving:
                if event.key == pygame.K_SPACE:
                    check_pos = (self.player.grid_pos[0] + self.player.direction[0],
                               self.player.grid_pos[1] + self.player.direction[1])
                    self.world.collect_stick(check_pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    self.player.is_running = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.player.is_running = False
        
        # Handle continuous movement
        if not self.player.is_moving and current_time - self.last_movement_time >= MOVEMENT_DELAY:
            keys = pygame.key.get_pressed()
            moved = False
            if keys[pygame.K_w]:
                moved = self.player.try_move([0, -1], self.world.rocks, self.world.current_stick)
            elif keys[pygame.K_s]:
                moved = self.player.try_move([0, 1], self.world.rocks, self.world.current_stick)
            elif keys[pygame.K_a]:
                moved = self.player.try_move([-1, 0], self.world.rocks, self.world.current_stick)
            elif keys[pygame.K_d]:
                moved = self.player.try_move([1, 0], self.world.rocks, self.world.current_stick)
            
            if moved:
                self.last_movement_time = current_time

    def update(self):
        dt = self.clock.get_time() / 1000.0
        self.player.update(dt)

    def render(self):
        self.renderer.render(self.world, self.player)
        self.clock.tick(60)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
        
        pygame.quit()