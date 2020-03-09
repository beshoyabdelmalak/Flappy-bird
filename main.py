import pygame
import os
import time
from model import Bird, Base, Pipe

pygame.font.init()

WN_WIDTH = 500
WN_HIGHT = 800
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

STAT_FONT = pygame.font.SysFont('comicsans', 50)

def draw_window(window, bird, base, pipes, score):
	window.blit(BG_IMG, (0,0))

	for pipe in pipes:
		pipe.draw(window)
	
	score = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
	window.blit(score, (WN_WIDTH - 10  - score.get_width(), 10))

	base.draw(window)
	bird.draw(window)
	pygame.display.update()


def crash(window, score):
	window.blit(BG_IMG, (0,0))
	score = STAT_FONT.render("SCORE: " + str(score), 1, (255,255,255))
	replay = STAT_FONT.render("HIT SPACE TO PLAY AGAIN ", 1, (255,255,255))
	window.blit(score, (150, 200))
	window.blit(replay, (20, 200 + score.get_height()+ 10))
	pygame.display.update()


def game_loop():
	bird = Bird(200,200)
	base = Base(730)
	pipes = [Pipe(600)]
	window = pygame.display.set_mode((WN_WIDTH, WN_HIGHT))
	pygame.display.set_caption('Flappy Bird')
	clock = pygame.time.Clock()
	score = 0
	
	run = True
	start = True
	# e = True
	while run:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		
		keys_pressed = pygame.key.get_pressed()
		if start:
			draw_window(window, bird, base, pipes, score)
			if keys_pressed[pygame.K_SPACE]:
				bird.jump()
				start = False
		else:
			remove_pipes = []
			passed = False
			crashed = False
			for pipe in pipes:
				if pipe.collide(bird):
					crashed = True
					crash(window, score)
					break
				
				if pipe.x + pipe.PIPE_TOP.get_width() < 0:
					remove_pipes.append(pipe)

				if not pipe.passed and pipe.x < bird.x:
					pipe.passed = True
					passed = True

				pipe.move()
			
			# in case of collision check if player wants to replay
			if crashed:
				keys_pressed = pygame.key.get_pressed()
				if keys_pressed[pygame.K_SPACE]:
					main()

			else:
				# if the bird passed the pipe increment score and add new pipe
				if passed:
					score += 1
					pipes.append(Pipe(600))
				
				# delete pipes that are out of the screen
				for remove in remove_pipes:
					pipes.remove(remove)

				# check if the bird hit the ground
				if bird.x + bird.img.get_height() >= 730:
					pass

				keys_pressed = pygame.key.get_pressed()

				# jump while playing
				if keys_pressed[pygame.K_SPACE]:
					bird.jump()
				
				bird.move()
				base.move()
				draw_window(window, bird, base, pipes, score)


def main():
	game_loop()
	pygame.quit()
	quit()

if __name__ == '__main__':
	main()