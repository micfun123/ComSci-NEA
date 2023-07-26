import pygame
# initialize pygame
pygame.init()

# define width of screen
width = 1000
# define height of screen
height = 600
screen_res = (width, height)

pygame.display.set_caption("GFG Bouncing game")
screen = pygame.display.set_mode(screen_res)

# define colors
red = (255, 0, 0)
black = (0, 0, 0)

# define ball
ball_obj = pygame.draw.circle(
	surface=screen, color=red, center=[100, 100], radius=5)
# define speed of ball
# speed = [X direction speed, Y direction speed]
speed = [1, 1]

# game loop
while True:
	# event loop
	for event in pygame.event.get():
		# check if a user wants to exit the game or not
		if event.type == pygame.QUIT:
			exit()

	# fill black color on screen
	screen.fill(black)

	# move the ball
	# Let center of the ball is (100,100) and the speed is (1,1)
	ball_obj = ball_obj.move(speed)
	# Now center of the ball is (101,101)
	# In this way our wall will move

	# if ball goes out of screen then change direction of movement
	if ball_obj.left <= 0 or ball_obj.right >= width:
		speed[0] = -speed[0]
	if ball_obj.top <= 0 or ball_obj.bottom >= height:
		speed[1] = -speed[1]

	# draw ball at new centers that are obtained after moving ball_obj
	pygame.draw.circle(surface=screen, color=red,
					center=ball_obj.center, radius=40)

	# update screen
	pygame.display.flip()
