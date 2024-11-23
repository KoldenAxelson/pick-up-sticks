import pygame
import time
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, MOVEMENT_DELAY, GRID_SIZE
from entities.player import Player
from world.game_world import GameWorld
from renderer import Renderer
from stats import GameStats

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pick Up Sticks')
        self.clock = pygame.time.Clock()
        
        self.player = Player(GRID_SIZE // 2, GRID_SIZE // 2)
        self.stats = GameStats()
        self.world = GameWorld(self.stats)
        self.renderer = Renderer(self.screen)
        
        self.running = True
        self.last_movement_time = time.time()

    def handle_input(self):
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and not self.player.is_moving:
                check_pos = (self.player.x + self.player.direction[0],
                               self.player.y + self.player.direction[1])
                if event.key == pygame.K_SPACE:
                    self.world.check_collection(check_pos, self.stats)
                elif event.key == pygame.K_r:
                    self.world.try_remove_rock(check_pos, self.stats)
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
                moved = self.player.try_move([0, -1], self.world)
            elif keys[pygame.K_s]:
                moved = self.player.try_move([0, 1], self.world)
            elif keys[pygame.K_a]:
                moved = self.player.try_move([-1, 0], self.world)
            elif keys[pygame.K_d]:
                moved = self.player.try_move([1, 0], self.world)
            
            if moved:
                self.stats.move_made()
                self.last_movement_time = current_time

    def update(self):
        dt = self.clock.get_time() / 1000.0
        self.player.update(dt)
        self.world.update(dt)

    def render(self):
        self.renderer.render(self.world, self.player, self.stats)
        self.clock.tick(60)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
        
        pygame.quit()