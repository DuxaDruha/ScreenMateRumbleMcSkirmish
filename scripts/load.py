import pygame


def appendAnimation(list, path, numberOfElements, fileExtension):
    for i in range(numberOfElements):
        list.append(pygame.image.load(str(path) + str(i) + fileExtension))