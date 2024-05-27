import pygame
from bird import Bird
from pipe import Pipe
from play import Button
from ground import Ground
from pygame import mixer

# set up pygame modules
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans', 20)
big_font = pygame.font.SysFont('Comic Sans', 40)
small_font = pygame.font.SysFont('Comic Sans', 13)
pygame.display.set_caption("Flappy Bird")


# set up variables for the display
size = (500, 600)
screen = pygame.display.set_mode(size)

#background images
background = pygame.image.load("background.png")
gray_background = pygame.image.load("back-gray.png")
leaderboard_background = pygame.image.load("leaderboard.png")
image_size_l = leaderboard_background.get_size()
scale_size = (image_size_l[0] * 0.37, image_size_l[1] * 0.37)
leaderboard_background = pygame.transform.scale(leaderboard_background, scale_size)

#background music
mixer.music.load('background_music.mp3')
mixer.music.play(-1)

#sprites variables
bird = Bird(10, 170)
pipe_bottom1 = Pipe(460, 407, "pipe_bottom1.png")
pipe_top3 = Pipe(460, 0, "pipe_top3.png")
pipe_bottom2 = Pipe(280, 300, "pipe_bottom2.png")
pipe_top2 = Pipe(280, -4, "pipe_top2.png")
pipe_bottom3 = Pipe(100, 237, "pipe_bottom3.png")
pipe_top1 = Pipe(100, -4, "pipe_top1.png")
ground = Ground(0, 560)
ground2 = Ground(330, 560)
button = Button(193, 230)

#Booleans for switching screens
run = True
start = True
game = False
end = False
high_score_display = False

#gravity for bird
up = False

#name text box for saving score
font = pygame.font.Font(None, 32)
input_box = pygame.Rect(175, 290, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False
typing = False

frame = 0
score = 0
score_list = []
score_name_list = []

# render the text for later
score_text = ("Score: " + str(score))
score_display = my_font.render(score_text , True, (0, 0, 0))
end_text = big_font.render('Game Over' , True, (0, 0, 0))
type_text = small_font.render('Type your name here' , True, (0, 0, 0))
enter_text = small_font.render("Press 'Enter' to save!", True, (0, 0, 0))

# -------- Main Program Loop -----------
clock = pygame.time.Clock()
while run:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False

        if start:
            pos = pygame.mouse.get_pos() #mouse position
            if event.type == pygame.MOUSEBUTTONDOWN and button.rect.collidepoint(pos):
                start = False
                game = True


        elif end:
            #textbox
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    #saving score
                    if event.key == pygame.K_RETURN:
                        #writes the score in file with comma
                        f = open("score.txt", "a")
                        f.write(str(score) + ',')
                        f = open('score.txt', 'r')
                        data = f.readline().strip()

                        num = []
                        e = 0
                        number = ''
                        comma = 0
                        #counts numbers of scores in file using commas
                        for c in data:
                            if c == ",":
                                comma = comma + 1
                        #makes a list of all scores
                        for i in range(comma):
                            while not (data[e] == ','):
                                num.insert(0, data[e])
                                e = e + 1
                            for o in num:
                                number = str(o) + str(number)
                            number = int(number)
                            score_list.append(number)
                            number = ''
                            e = e + 1
                            num = []

                        #writes the names in file with commas
                        f = open("scorename.txt", "a")
                        f.write(text + ',')
                        f = open('scorename.txt', 'r')
                        data = f.readline().strip()

                        word = []
                        e = 0
                        letter = ''
                        comma = 0
                        #counts numbers of names in file using commas
                        for c in data:
                            if c == ",":
                                comma = comma + 1
                        #makes a list of all scores
                        for i in range(comma):
                            while not (data[e] == ','):
                                word.insert(0, data[e])
                                e = e + 1
                            for o in word:
                                letter = str(o) + letter
                            score_name_list.append(letter)
                            letter = ''
                            e = e + 1
                            word = []

                        #clears the text box
                        text = ''

                        #length of lists
                        running = 0
                        if comma > 5:
                            running = 5
                        else:
                            running = comma

                        #makes lists of both top 5 scores and their names in order
                        high_score_list = []
                        high_name_list = []
                        if not (score_list == []):
                            for i in range(running):
                                max_score = max(score_list)
                                high_score_list.append(max_score)
                                max_index = score_list.index(max_score)
                                score_list.pop(max_index)
                                max_name = score_name_list[max_index]
                                high_name_list.append(max_name)
                                score_name_list.pop(max_index)

                        high_score_display = True
                        end = False

                    #deletes texts when backspace is pressed
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

    if game:
        clock.tick(60)
        #gravity for bird
        if up == False:
            bird.move_down()
        keys = pygame.key.get_pressed()
        #moves the bird up when user press SPACE
        if bird.y < 580:
            if keys[pygame.K_SPACE]:
                bird.move_up()
                up = True
                #flap animation with sound
                if frame % 5 == 0:
                    bird.switch_image()
                if frame % 9    == 0:
                    mixer.Sound('flap.mp3').play()
            else:
                up = False
        
        #background sprites like pipes and ground keeps moving left
        pipe_bottom1.move_left()
        pipe_bottom2.move_left()
        pipe_bottom3.move_left()
        pipe_top1.move_left()
        pipe_top2.move_left()
        pipe_top3.move_left()
        ground.move_left()
        ground2.move_left()

        #loops the bacground
        if ground.x < -330:
            ground = Ground(330, 560)
        elif ground2.x < -330:
            ground2 = Ground(330, 560)

        if pipe_bottom1.x == -63:
            pipe_bottom1 = Pipe(500, 407, "pipe_bottom1.png")
            pipe_top3 = Pipe(500, 0, "pipe_top3.png")
            
        elif pipe_bottom2.x == -63:
            pipe_bottom2 = Pipe(500, 300, "pipe_bottom2.png")
            pipe_top2 = Pipe(500, 0, "pipe_top2.png")
 
        elif pipe_bottom3.x == -63:
            pipe_bottom3 = Pipe(500, 237, "pipe_bottom3.png")
            pipe_top1 = Pipe(500, 0, "pipe_top1.png")
        
        #updates score as time passes
        if frame % 30 == 0:
            score = score + 1
        score_text = ("Score: " + str(score))
        score_display = my_font.render(score_text , True, (0, 0, 0))

        #detects collison of bird with pipes and ground
        if bird.rect.colliderect(pipe_bottom1.rect) or bird.rect.colliderect(pipe_bottom2.rect) \
        or bird.rect.colliderect(pipe_bottom3.rect) or bird.rect.colliderect(pipe_top1.rect) \
        or bird.rect.colliderect(pipe_top2.rect) or bird.rect.colliderect(pipe_top3.rect) \
        or bird.rect.colliderect(ground.rect) or bird.rect.colliderect(ground2.rect):
            mixer.Sound('Death.mp3').play()
            game = False
            end = True

    #blits all the sprites if everything besides leaderboard is true
    if start or game or end:
        screen.blit(background, (0, 0))
        screen.blit(bird.image, bird.rect)
        screen.blit(pipe_bottom1.image, pipe_bottom1.rect)
        screen.blit(pipe_top3.image, pipe_top3.rect)
        screen.blit(pipe_bottom2.image, pipe_bottom2.rect)
        screen.blit(pipe_top2.image, pipe_top2.rect)
        screen.blit(pipe_bottom3.image, pipe_bottom3.rect)
        screen.blit(pipe_top1.image, pipe_top1.rect)
        screen.blit(ground.image, ground.rect)
        screen.blit(ground2.image, ground2.rect)
        screen.blit(score_display, (0, 0))
        if start:
            #creates transparent gray background over the game
            screen.blit(gray_background, (0, 0))
            #blits button
            screen.blit(button.image, button.rect)
        if end:
            #blits things for saving score
            screen.blit(gray_background, (0, 0))
            end_block = pygame.draw.rect(screen, (255, 255, 255), [150, 110, 245, 270])
            screen.blit(end_text, (170, 150))
            screen.blit(score_display, (230, 210))
            screen.blit(type_text, (212, 265))
            screen.blit(enter_text, (212, 322))
            # Render the current text.
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()

    #leaderboard
    elif high_score_display:
        #blits background for leaderboard
        screen.fill((0, 0, 0))
        screen.blit(leaderboard_background, (35, 0))

        #blits the scores from highest to lowest
        if len(high_score_list) >= 1:
            score_1st = my_font.render(str(high_score_list[0]), True, (255, 255, 255))
            screen.blit(score_1st, (375, 202))
        if len(high_score_list) >= 2:
            score_2nd = my_font.render(str(high_score_list[1]), True, (255, 255, 255))
            screen.blit(score_2nd, (375, 300))
        if len(high_score_list) >= 3:
            score_3rd = my_font.render(str(high_score_list[2]), True, (255, 255, 255))
            screen.blit(score_3rd, (375, 388))
        if len(high_score_list) >= 4:
            score_4th = my_font.render(str(high_score_list[3]), True, (255, 255, 255))
            screen.blit(score_4th, (375, 473))
        if len(high_score_list) >= 5:
            score_5th = my_font.render(str(high_score_list[4]), True, (255, 255, 255))
            screen.blit(score_5th, (375, 551))

        #blits the names of their highscores
        if len(high_score_list) >= 1:
            name_1st = my_font.render(high_name_list[0], True, (255, 255, 255))
            screen.blit(name_1st, (200, 202))
        if len(high_score_list) >= 2:
            name_2nd = my_font.render(high_name_list[1], True, (255, 255, 255))
            screen.blit(name_2nd, (200, 300))
        if len(high_score_list) >= 3:
            name_3rd = my_font.render(high_name_list[2], True, (255, 255, 255))
            screen.blit(name_3rd, (200, 388))
        if len(high_score_list) >= 4:
            name_4th = my_font.render(high_name_list[3], True, (255, 255, 255))
            screen.blit(name_4th, (200, 473))
        if len(high_score_list) >= 5:
            name_5th = my_font.render(high_name_list[4], True, (255, 255, 255))
            screen.blit(name_5th, (200, 551))

    #updates the screen
    pygame.display.update()
    frame += 1

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()