import pygame
import sys
from constants import *
from player import Player
from asteroidfield import *
from circleshape import CircleShape
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    AsteroidField()

    dt = 0
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    score = 0
    font = pygame.font.Font(None, 64)
    percent_20 = (ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS) * 0.2


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collision(player):
                sys.exit("Game over!")
        
            for shot in shots:
                if asteroid.collision(shot):
                    shot.kill()
                    asteroid.split()
                    
                    if asteroid.radius <= (ASTEROID_MIN_RADIUS + percent_20):
                        score += 100
                    elif asteroid.radius >= (ASTEROID_MAX_RADIUS - percent_20):
                        score += 10
                    else:
                        score += 50
        
        screen.fill("black")

        for i in drawable:
            i.draw(screen)
        
        text = font.render(f"Score: {score:,}", True, "white")
        screen.blit(text, (20, 20))

        pygame.display.flip()

        # Limits the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()