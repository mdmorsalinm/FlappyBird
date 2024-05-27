import pygame


class Pipe:

    def __init__(self, x, y, pipe_image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(pipe_image)
        self.rescale_image(self.image)
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        self.delta = 1


    def rescale_image(self, image):
        self.image_size = self.image.get_size()
        scale_size = (self.image_size[0] * 3, self.image_size[1] * 4)
        self.image = pygame.transform.scale(self.image, scale_size)


    def move_left(self):
        self.x = self.x - self.delta
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])

        