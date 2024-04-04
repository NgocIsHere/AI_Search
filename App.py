import pygame
import random

pygame.init()
clock = pygame.time.Clock()
width = 1280
height = 700
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
              (1, 1), (-1, -1), (1, -1), (-1, 1)]


class LevelChooser:
    def __init__(self):
        self.isPlay: False
        self.lv = 0
        self.point = 0
        self.bg = pygame.image.load('./image/bg.jpg')
        self.maplv1 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv2 = pygame.transform.scale(
            pygame.image.load('./image/maplv2.png'), (200, 150))
        self.maplv3 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv4 = pygame.transform.scale(
            pygame.image.load('./image/maplv4.png'), (200, 150))
        self.robot = pygame.transform.scale(
            pygame.image.load('./image/robot.png'), (50, 60))
        self.robot_x = 0
        self.robot_y = 0
        self.robot_dir = (1, 0)

        self.choice = 0
        self.isChoosing = True

    def drawChoose(self):
        global width, height
        x, y = pygame.mouse.get_pos()
        width, height = screen.get_size()
        self.bg = pygame.transform.scale(self.bg, (width, height))
        screen.blit(self.bg, (0, 0))

        robot_rect = self.robot.get_rect()
        # generate a robot which run on screen
        if random.randint(1, 50) == 25:
            self.robot_dir = random.choice(directions)
        self.robot_x += self.robot_dir[0] * 4
        self.robot_y += self.robot_dir[1] * 4
        # limit the running of robot on the screen
        if self.robot_x < 0:
            self.robot_x = width
        elif self.robot_x > width:
            self.robot_x = 0
        if self.robot_y < 0:
            self.robot_y = height
        elif self.robot_y > height:
            self.robot_y = 0

        screen.blit(self.robot, (self.robot_x, self.robot_y))

        font = pygame.font.SysFont('DroidSans', 50)
        color = (int(0), int(0), int(0))
        screen.blit(font.render("Welcome to Find Road Game.",
                    True, (color)), (width/2 - 235, 50))
        screen.blit(font.render("Let choose your level!",
                    True, (color)), (width/2 - 235, 98))

        if x > width/2-220 and x < width/2-20 and y > height/2 - 170 and y < height/2 - 20:
            pygame.draw.rect(
                screen, color, (width/2-225, height/2-175, 210, 160))
            self.choice = 1
        elif x > width/2+20 and x < width/2+220 and y > height/2 - 170 and y < height/2 - 20:
            self.choice = 2
            pygame.draw.rect(
                screen, color, (width/2+15, height/2-175, 210, 160))
        elif x > width/2-220 and x < width/2-20 and y > height/2 + 20 and y < height/2 + 170:
            self.choice = 3
            pygame.draw.rect(
                screen, color, (width/2-225, height/2 + 15, 210, 160))
        elif x > width/2+20 and x < width/2+220 and y > height/2 + 20 and y < height/2 + 170:
            self.choice = 4
            pygame.draw.rect(
                screen, color, (width/2+15, height/2+15, 210, 160))
        else:
            self.choice = 0

        screen.blit(self.maplv1, (width/2-220, height/2-170))
        screen.blit(self.maplv2, (width/2+20, height/2-170))
        screen.blit(self.maplv3, (width/2-220, height/2+20))
        screen.blit(self.maplv4, (width/2+20, height/2+20))

        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Level 1", True, color), (width/2-160, height/2-15))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Level 2", True, color), (width/2 + 80, height/2-15))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Level 3", True, color), (width/2-160, height/2 + 175))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Level 4", True, color), (width/2 + 80, height/2 + 175))
        pygame.display.flip()

    def choose(self):
        while self.isChoosing:
            self.drawChoose()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if self.choice != 0:
                            self.isChoosing = False

                clock.tick(60)


class MapChooser:
    def __init__(self):
        self.isPlay: False
        self.lv = 0
        self.point = 0
        self.bg = pygame.image.load('./image/bg.jpg')
        self.maplv1 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv2 = pygame.transform.scale(
            pygame.image.load('./image/maplv2.png'), (200, 150))
        self.maplv3 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.robot = pygame.transform.scale(
            pygame.image.load('./image/robot.png'), (50, 60))
        self.robot_x = 0
        self.robot_y = 0
        self.robot_dir = (1, 0)

        self.choice = 0
        self.isChoosing = True

    def drawChoose(self):
        global width, height
        x, y = pygame.mouse.get_pos()
        width, height = screen.get_size()
        self.bg = pygame.transform.scale(self.bg, (width, height))
        screen.blit(self.bg, (0, 0))

        robot_rect = self.robot.get_rect()
        # generate a robot which run on screen
        if random.randint(1, 50) == 25:
            self.robot_dir = random.choice(directions)
        self.robot_x += self.robot_dir[0] * 4
        self.robot_y += self.robot_dir[1] * 4
        # limit the running of robot on the screen
        if self.robot_x < 0:
            self.robot_x = width
        elif self.robot_x > width:
            self.robot_x = 0
        if self.robot_y < 0:
            self.robot_y = height
        elif self.robot_y > height:
            self.robot_y = 0

        screen.blit(self.robot, (self.robot_x, self.robot_y))

        font = pygame.font.SysFont('DroidSans', 50)
        color = (int(0), int(0), int(0))
        screen.blit(font.render("Next Step: Choose a map!",
                    True, (color)), (width/2 - 200, 46))

        if x > width/2-220 and x < width/2-20 and y > height/2 - 170 and y < height/2 - 20:
            pygame.draw.rect(
                screen, color, (width/2-225, height/2-175, 210, 160))
            self.select = 1
        elif x > width/2+20 and x < width/2+220 and y > height/2 - 170 and y < height/2 - 20:
            self.select = 2
            pygame.draw.rect(
                screen, color, (width/2+15, height/2-175, 210, 160))
        elif x > width/2-110 and x < width/2+100 and y > height/2 + 20 and y < height/2 + 170:
            self.select = 3
            pygame.draw.rect(
                screen, color, (width/2-115, height/2 + 15, 210, 160))
        else:
            self.select = 0

        screen.blit(self.maplv1, (width/2-220, height/2-170))
        screen.blit(self.maplv2, (width/2+20, height/2-170))
        screen.blit(self.maplv3, (width/2-110, height/2+20))

        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Map 1", True, color), (width/2-160, height/2-15))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Map 2", True, color), (width/2 + 80, height/2-15))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Map 3 (No path)", True, color), (width/2-80, height/2 + 175))
        pygame.display.flip()

    def choose(self):
        while self.isChoosing:
            self.drawChoose()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if self.select != 0:
                            self.isChoosing = False

                clock.tick(60)


class AlgorithmChooser:
    def __init__(self):
        self.isPlay: False
        self.lv = 0
        self.point = 0
        self.bg = pygame.image.load('./image/bg.jpg')
        self.maplv1 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv2 = pygame.transform.scale(
            pygame.image.load('./image/maplv2.png'), (200, 150))
        self.maplv3 = pygame.transform.scale(
            pygame.image.load('./image/maplv1.png'), (200, 150))
        self.maplv4 = pygame.transform.scale(
            pygame.image.load('./image/maplv4.png'), (200, 150))
        self.robot = pygame.transform.scale(
            pygame.image.load('./image/robot.png'), (50, 60))
        self.robot_x = 0
        self.robot_y = 0
        self.robot_dir = (1, 0)

        self.choice = 0
        self.isChoosing = True

    def drawChoose(self):
        global width, height
        x, y = pygame.mouse.get_pos()
        width, height = screen.get_size()
        self.bg = pygame.transform.scale(self.bg, (width, height))
        screen.blit(self.bg, (0, 0))

        robot_rect = self.robot.get_rect()
        # generate a robot which run on screen
        if random.randint(1, 50) == 25:
            self.robot_dir = random.choice(directions)
        self.robot_x += self.robot_dir[0] * 4
        self.robot_y += self.robot_dir[1] * 4
        # limit the running of robot on the screen
        if self.robot_x < 0:
            self.robot_x = width
        elif self.robot_x > width:
            self.robot_x = 0
        if self.robot_y < 0:
            self.robot_y = height
        elif self.robot_y > height:
            self.robot_y = 0

        screen.blit(self.robot, (self.robot_x, self.robot_y))

        font = pygame.font.SysFont('DroidSans', 50)
        color = (int(0), int(0), int(0))
        screen.blit(font.render("Final: Choose an algorithm!",
                    True, (color)), (width/2 - 235, 50))

        if x > width/2-220 and x < width/2-20 and y > height/2 - 170 and y < height/2 - 20:
            pygame.draw.rect(
                screen, color, (width/2-225, height/2-75, 200, 80), 8)
            self.select = 1
        elif x > width/2+20 and x < width/2+220 and y > height/2 - 170 and y < height/2 - 20:
            self.select = 2
            pygame.draw.rect(
                screen, color, (width/2+15, height/2-75, 200, 80), 8)
        elif x > width/2-220 and x < width/2-20 and y > height/2 + 20 and y < height/2 + 170:
            self.select = 3
            pygame.draw.rect(
                screen, color, (width/2-120, height/2 + 15, 200, 80), 8)
        else:
            self.select = 0

        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "A Star", True, color), (width/2-160, height/2 - 40))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "Blind Search", True, color), (width/2 + 48, height/2-40))
        screen.blit(pygame.font.SysFont("Consolas", 20).render(
            "BFS", True, color), (width/2-40, height/2 + 48))
        pygame.display.flip()

    def choose(self):
        while self.isChoosing:
            self.drawChoose()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if self.select != 0:
                            self.isChoosing = False

                clock.tick(60)


while True:
    levelChooser = LevelChooser()
    levelChooser.choose()
    mapChooser = MapChooser()
    mapChooser.choose()

    algorithmChooser = AlgorithmChooser()
    if levelChooser.choice != 1:
        algorithmChooser.choose()
    else:
        algorithmChooser.choice = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    clock.tick(60)
    pygame.display.update()
