import random
import math,time
import pygame,sys,random
from pygame.locals import*


pygame.init()
width = 1280
height = 700
clock = pygame.time.Clock()
FPS = 60
column = 7
row = 4

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

ifrom,ito,jfrom,jto = 0,0,0,0
width_rec = 45
# Define the directions: Up, Down, Left, Right
directions = [(0,1),(0,-1),(1,0),(-1,0)]

tablelv3 = []
def initTableLv3():

    tablelv3.clear()
    for i in range(0,row):
        temp = []
        for j in range(0,column):
            temp.append(-1)
        tablelv3.append(temp)

def isMonsterLocation(pos):
    for mon in monster:
        if mon.posi == pos.posi and mon.posj == pos.posj:
            return True
    return False

def UpdateTableLv3():
    for i in range(ifrom,ito+1):
        for j in range(jfrom,jto+1):
            tablelv3[i][j] = Map.table[i][j]


def drawBlind():
    xpacman,ypacman = width_rec*pacman.posj  +x_root + pacman.posx,width_rec*pacman.posi+y_root+pacman.posy
    blind = pygame.transform.scale(pygame.image.load("./image/bg.png"),(width_rec*column,width_rec*row))

    if ypacman-3*width_rec >=y_root:
        screen.blit(blind,(x_root,ypacman - (3+row)*width_rec))
    pygame.draw.line(screen,(100,100,100),(xpacman -3*width_rec,ypacman - 3*width_rec),(xpacman +4*width_rec,ypacman - 3*width_rec),2)

    if ypacman+4*width_rec <= y_root + width_rec*row:
        screen.blit(blind,(x_root,ypacman + 4*width_rec))
    pygame.draw.line(screen,(100,100,100),(xpacman -3*width_rec,ypacman + 4*width_rec),(xpacman +4*width_rec,ypacman + 4*width_rec),2)

    if xpacman - 3*width_rec >=x_root:
        screen.blit(blind,(xpacman-(3+column)*width_rec,y_root))
    pygame.draw.line(screen,(100,100,100),(xpacman -3*width_rec,ypacman - 3*width_rec),(xpacman -3*width_rec,ypacman + 4*width_rec),2)

    if xpacman + 4*width_rec <=x_root + width_rec * column:
        screen.blit(blind,(xpacman+4*width_rec,y_root))
    pygame.draw.line(screen,(100,100,100),(xpacman +4*width_rec,ypacman - 3*width_rec),(xpacman +4*width_rec,ypacman + 4*width_rec),2)



def heuristic_for_foodlv3(food):
    if len(DirectionCanGoUp(food.posi,food.posj)) == 1:
        for mon in monster:
            if tablelv3[mon.posi][mon.posj] !=-1 and distance(Position(food.posi,food.posj),Position(mon.posi,mon.posj)) <3:
                return row*column*3
    return 1

def heuristic_for_lv3(node):
    for mon in monster:
        if mon.posi == node.posi and mon.posj == node.posj:
            return row*column*10
    for mon in monster:
        if distance(node,Position(mon.posi,mon.posj)) == 1:
            return row*column*5

    if len(DirectionCanGoUp(node.posi,node.posj)) == 1:
        return row*column*3

    return distance(Position(pacman.posi,pacman.posj),node)


def heuristic_for_lv4(node):
    for mon in monster:
        if mon.posi == node.posi and mon.posj == node.posj:
            return row*column*row*column*10

    if len(DirectionCanGoUp(node.posi,node.posj)) == 1:
        return row*column*row*column*9

    for mon in monster:
        if distance(node,Position(mon.posi,mon.posj)) == 1:
            return row*column*row*column*8



    return distance(Position(pacman.posi,pacman.posj),node)

def DirectionToPosition(pos,dire):
    if dire == LEFT:
        return Position(pos.posi,pos.posj-1)
    if dire == RIGHT:
        return Position(pos.posi,pos.posj+1)
    if dire == UP:
        return Position(pos.posi-1,pos.posj)
    if dire == DOWN:
        return Position(pos.posi+1,pos.posj)

def heuristic_path(start,path):
    currentpos = start
    cost = 0
    for dire in path:
        nextpos = DirectionToPosition(currentpos,dire)
        count = DirectionCanGoUp(nextpos.posi,nextpos.posj)
        if count == 2:
            cost +=row*column
        else:
            cost+=1
        currentpos = nextpos
    return cost
    

def UpdateBlind():
    global ifrom,ito,jfrom,jto
    ifrom,ito,jfrom,jto = pacman.posi -3,pacman.posi+3,pacman.posj - 3,pacman.posj+3
    if ifrom <0 : ifrom =0
    if ito>row-1: ito = row - 1
    if jfrom <0: jfrom = 0
    if jto >column-1:jto = column - 1

def isNeighborUnknow(node):
    newnode = []
    if node.posi!=0: newnode.append([node.posi-1,node.posj])
    if node.posi!=row-1: newnode.append([node.posi+1,node.posj])
    if node.posj!=0: newnode.append([node.posi,node.posj-1])
    if node.posj!=column-1: newnode.append([node.posi,node.posj+1])
    for n in newnode:
        if tablelv3[n[0]][n[1]] !=-1:
            return True,Position(n[0],n[1])
    return False, Position(-1,-1)


def heuristic(node, goal):
    if Map.table[goal.posi][goal.posj] == 2:
        for mon in monster:
            # xet cac o monster dang dung
            if node.posi == mon.posi and node.posj == mon.posj:
                return row*column*10

    return distance(node,goal)

def distance(node,goal):
    return round(math.sqrt((node.posi - goal.posi)*(node.posi - goal.posi) + 
                            (node.posj - goal.posj)*(node.posj - goal.posj)) *100) /100

class Position:
    def __init__(self, i,j):
        self.posi = i
        self.posj = j
    
    def print(self):
        print(self.posi, ' - ', self.posj)


def getDistance(x1,y1,x2,y2):
    return round(math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)) *100) /100

class TableGame:
    def __init__(self):
        self.table = []
        self.path = []
    def initTable(self):
        for i in range(0,row):
            temp = []
            for j in range(0,column):
                temp.append(0)
            self.table.append(temp)

    def UpdateTable(self,posi,posj):
        if(self.table[posi][posj] == 2):
            self.table[posi][posj] = 0
            playgame.point+=20

    def checkWin(self):
        for i in range(0,row):
            for j in range(0,column):
                if (self.table[i][j] == 2):
                    return False
        return True

    def findFoodNearest(self,posi,posj):
        nearestFood = row * column
        ifood = 0
        jfood = 0
        for i in range(0,row):
            for j in range (0,column):
                distance = getDistance(posi,posj,i,j)
                if self.table[i][j] == 2 and nearestFood  > distance:
                    ifood = i
                    jfood = j
                    nearestFood = distance

        return Position(ifood,jfood)
    
    def findFoodNearestLv3(self, posi, posj):
        nearestfood = row * column
        ifood = -1
        jfood = -1
        for i in range(-3, 4):  # Iterate over the range -3 to 3 (inclusive)
            for j in range(-3, 4):  # Iterate over the range -3 to 3 (inclusive)
                x = posi + i
                y = posj + j
                if x >= 0 and x < len(self.table) and y >= 0 and y < len(self.table[x]) and self.monstertable[x][y] == 2:
                    distance = getDistance(posi, posj, x, y)
                    if distance < nearestfood:
                        ifood = x
                        jfood = y
                        nearestfood = distance

        return Position(ifood, jfood)

    def A_star_Lv1(self):
        goal = self.findFoodNearest(pacman.posi,pacman.posj)
        start = Position(pacman.posi,pacman.posj)
        path = self.A_star_algorithm(start,goal)
        if len(path) !=0:
            return [path[0]]
        if len(path) == 0:
            for p in PositionCanGoUp(start.posi,start.posj):
                pygame.draw.rect(screen, (255, 0, 0), (p.posj * width_rec + x_root, p.posi * width_rec + y_root, width_rec, width_rec))
        return []
    
    def A_star_Lv2(self):
        goal = self.findFoodNearest(pacman.posi,pacman.posj)
        start = Position(pacman.posi,pacman.posj)
        path = self.A_star_algorithm(start, goal)
        if len(self.path) != 0 and len(self.path) <= len(path):
            time.sleep(1)
            return []
        if len(path) != 0:
            self.path = path
            return [self.path[0]]
        if len(self.path) == 0:
            for p in PositionCanGoUp(start.posi,start.posj):
                pygame.draw.rect(screen, (255, 0, 0), (p.posj * width_rec + x_root, p.posi * width_rec + y_root, width_rec, width_rec))
        return []
    
    def A_star_lv3(self):
        dire =[]
        start = Position(pacman.posi,pacman.posj)

        count = 0
        for pos in PositionCanGoUp(pacman.posi,pacman.posj):
            if heuristic_for_lv3(pos) <row*column*5:
                count+=1
                dire.append(DirectionFromTo(start,pos))
        if count==0:
            return []
        if count ==1:
            return [dire[0]]

        minf = row*column*100
        result= -1
        for i in range(0,row):
            for j in range(0,column):
                if tablelv3[i][j]==2:
                    goal =Position(i,j)
                    path = self.A_star_algorithm(start,goal)
                    if len(path) !=0 and path[0] in dire and minf > len(path) + heuristic_for_foodlv3(goal):
                        result = path[0]
                        #print(path)
                        minf = len(path) + heuristic_for_foodlv3(goal)
        if result!=-1:
            #print("result ",[result])
            return [result]

        #hoc map
        #print(1)
        minf = row*column*100
        check,goal = False,Position(-1,-1)
        for i in range(0,row):
            for j in range(0,column):
                if tablelv3[i][j] == -1:
                    check,goal = isNeighborUnknow(Position(i,j))
                    if check:
                        path = self.A_star_algorithm(start,goal)
                        if len(path) !=0 and path[0] in dire and minf > len(path) + heuristic_for_lv3(goal):
                            result = path[0]
                            #print(path)
                            minf = len(path) + heuristic_for_lv3(goal)
        if result!=-1:
            return [result]

        return [dire[0]]
        

    def A_star_lv4(self):
        dire =[]
        start = Position(pacman.posi,pacman.posj)
        result =[]

        count = 0
        for pos in PositionCanGoUp(pacman.posi,pacman.posj):
            if heuristic_for_lv4(pos) <row*column*row*column*9:
                count+=1
            elif heuristic_for_lv4(pos) == row*column*row*column*9 and Map.table[pos.posi][pos.posj] == 2:
                result = [DirectionFromTo(start,pos)]
            dire.append([DirectionFromTo(start,pos),heuristic_for_lv4(pos)])
        dire = sorted(dire, key = lambda item: item[1], reverse = False)
        #print(pacman.posi,pacman.posj,dire)

        if count==0 :
            return result
        if dire[0][1] == row*column*row*column*8 and dire[len(dire)-1][1] <row*column*row*column*9:
            
            return []
        if dire[0][1] == row*column*row*column*8 and dire[len(dire)-1][1] >=row*column*row*column*9:
            return [dire[0][0]]
        if count ==1 :
            return [dire[0][0]] 

        temp =[]
        for i in range(0,len(dire)):
            if dire[i][1] <row*column*row*column*8:
                temp.append(dire[i][0])

        dire = temp
        
        minf = row*column*row*column*100
        result= -1
        for i in range(0,row):
            for j in range(0,column):
                if Map.table[i][j]==2:
                    goal =Position(i,j)
                    path = self.A_star_algorithm(start,goal)
                    if len(path) !=0 and path[0] in dire and minf > len(path) + heuristic_for_lv4(goal):
                        result = path[0]
                        #print(path)
                        minf = len(path) + heuristic_for_lv4(goal)
        if result!=-1:
            #print("result ",[result])
            return [result]

        return [dire[0]]
        

    def A_star_algorithm(self, start, goal):
        result = []
        isVisited = []
        for i in range(0, row):
            temp =[]
            for j in range(0, column):
                temp.append(0)
            isVisited.append(temp)
        queue = []
        isVisited[start.posi][start.posj] = 1

        queue.append([start.posi, start.posj, heuristic(start, goal)])

        while queue:
            newpos = queue[0]
            newpos.pop(2)  #delete weight from newpos
            start = Position(newpos[0], newpos[1])
            result.append(start)
            queue.pop(0)
            if start.posi == goal.posi and start.posj == goal.posj:
                break
            connectPos = PositionCanGoUp(start.posi, start.posj)

            for pos in connectPos:
                if isVisited[pos.posi][pos.posj] == 0:
                    weight = heuristic(pos, goal)   #get weight in heuristic table
                    queue.append([pos.posi, pos.posj, weight])
                    isVisited[pos.posi][pos.posj] = 1
                    #print(connectPos[i].posi,connectPos[i].posj)
            queue = sorted(queue, key = lambda item: item[2], reverse = False)
        temp = result[len(result) - 1]
        if temp.posi != goal.posi or temp.posj != goal.posj:
            return []
        
        return ConvertToDirection(result)
    
def ConvertToDirection(pos):
    direction =[]
    i = len(pos) - 1
    while(i!=0):
        j = 1
        t = -1
        while(t == -1):
            t= DirectionFromTo(pos[i-j],pos[i])
            if (t!=-1 and t in DirectionCanGoUp(pos[i-j].posi,pos[i-j].posj)):
                i = i-j
                direction.insert(0,t)
            else: t=-1
            j+=1

    
    
    return direction

class PacMan:
    def __init__(self):
        self.posi = 1
        self.posj = 0
        self.posx = 0
        self.posy = 0
        self.v = 3
        self.step = 0
        self.pacman_image = pygame.transform.scale(pygame.image.load("./image/pacman.png"),(width_rec/2,width_rec/2))
        self.direction_queue = []

    def drawPacMan(self):
        screen.blit(self.pacman_image,(width_rec*self.posj + width_rec/4 +x_root + self.posx,width_rec*self.posi + width_rec/4+y_root+self.posy))
        if playgame.isplay:
            self.move()

    def move(self):
        #init direction queue 
        if(len(self.direction_queue) == 0):
            if(Map.table[self.posi][self.posj] == 2):
                Map.table[self.posi][self.posj] =0
                playgame.point+=20
            UpdateBlind()
            n = len(self.direction_queue)
            
            self.UpdateDirectionQueue()
            
            if len(self.direction_queue) == 0:
                self.v = 0
                playgame.isplay = False
                return
            else:self.v = 3

        if len(self.direction_queue) != 0:
            if self.direction_queue[0] == LEFT:
                self.posx -= self.v
            elif self.direction_queue[0] == RIGHT:
                self.posx +=self.v
            elif self.direction_queue[0] == UP:
                self.posy -=self.v
            else:
                self.posy+=self.v

            self.step+=self.v

        if self.step == width_rec:
            if(len(self.direction_queue) != 0):
                if self.direction_queue[0] == LEFT: self.posj -= 1
                elif self.direction_queue[0] == RIGHT: self.posj += 1
                elif self.direction_queue[0] == UP: self.posi -= 1
                elif self.direction_queue[0] == DOWN: self.posi += 1
                self.direction_queue.pop(0)
                playgame.point -=1
                playgame.cost +=1
            self.posx = self.posy = 0
            self.step = 0

    def UpdateDirectionQueue(self):
        #A* here. the path is insert to the direction_queue
        if playgame.select == 1:
            self.direction_queue = Map.A_star_Lv1()
        elif playgame.select == 2:
            self.direction_queue = Map.A_star_Lv2()


            
        elif playgame.select == 3:
            UpdateTableLv3()
            self.direction_queue = Map.A_star_lv3()
        elif playgame.select == 4:
            self.direction_queue = Map.A_star_lv4()

class Monster:
    def __init__(self, image, i, j):
        self.monster_image = pygame.transform.scale(pygame.image.load("./image/" + image),(width_rec/2,width_rec/2))
        self.posi = i
        self.posj = j
        self.posx = 0
        self.posy = 0
        self.v = 3
        self.step = 0
        self.direction_queue =[]

    def drawMonster(self):
        screen.blit(self.monster_image,(width_rec*self.posj + width_rec/4 +x_root + self.posx,width_rec*self.posi + width_rec/4+y_root+self.posy))
        if playgame.isplay:
            self.move()

    def move(self):
        #lv2 ko di chuyen
        if(playgame.select == 2):
            return
        else:
            if len(self.direction_queue) == 0:
                if pacman.posi == self.posi and pacman.posj == self.posj:
                    playgame.isplay = False
                    return
                self.UpdateDirectionQueue()
         
            if self.direction_queue[0] == LEFT:
                self.posx -= self.v
            elif self.direction_queue[0] == RIGHT:
                self.posx +=self.v
            elif self.direction_queue[0] == UP:
                self.posy -=self.v
            else:
                self.posy+=self.v

            self.step+=self.v

            if self.step == width_rec:
                if(len(self.direction_queue) != 0):
                    
                    if self.direction_queue[0] == LEFT: self.posj -= 1
                    elif self.direction_queue[0] == RIGHT: self.posj += 1
                    elif self.direction_queue[0] == UP: self.posi -= 1
                    elif self.direction_queue[0] == DOWN: self.posi += 1
                    self.direction_queue.pop(0)
                self.posx = self.posy = 0
                self.step = 0

    def UpdateDirectionQueue(self):
        if playgame.select == 3:
            self.direction_queue.append(self.RandomDirection(self.posi,self.posj))
        if playgame.select == 4:
            start = Position(self.posi,self.posj)
            goal = Position(pacman.posi,pacman.posj)
            path = Map.A_star_algorithm(start,goal)
            self.direction_queue=[path[0]]

    def RandomDirection(self,i,j):
        direction = []
        if j != column -1 and Map.table[i][j + 1] != 1: 
            direction.append(RIGHT)
        if j != 0 and Map.table[i][j - 1] != 1: 
            direction.append(LEFT)
        if i != 0  and Map.table[i - 1][j] != 1: 
            direction.append(UP)
        if i != row -1 and Map.table[i + 1][j] != 1: 
            direction.append(DOWN)

        return direction[random.randint(0,len(direction)-1)]

    def IsGameLose(self):
        if self.posi == pacman.posi and self.posj == pacman.posj:
            return True
        return False

class PlayGame:
    def __init__(self):
        self.isplay = False
        self.lv = 0
        self.point = 0
        self.bg = pygame.image.load("./image/bg.png")
        self.maplv1 = pygame.transform.scale(pygame.image.load("./image/maplv1.png"),(200,150))
        self.maplv2 = pygame.transform.scale(pygame.image.load("./image/maplv2.png"),(200,150))
        self.maplv3 = pygame.transform.scale(pygame.image.load("./image/maplv1.png"),(200,150))
        self.maplv4 = pygame.transform.scale(pygame.image.load("./image/maplv4.png"),(200,150))
        self.select = 0;
        self.isChoose = True
        self.cost = 0
    def drawChoose(self):
        global width,height
        x,y = pygame.mouse.get_pos()
        width,height = screen.get_size()
        randomcolor  = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

        self.bg = pygame.transform.scale(self.bg,(width,height))
        screen.blit(self.bg,(0,0))

        pygame.draw.rect(screen,(255,255,255),(150,100,width-300,height-200),10)
        pygame.draw.rect(screen,(0,38,230),(width/2-100,50,200,100),0,5)

        font = pygame.font.SysFont("Consolas",50)
        screen.blit(font.render("CHOOSE",True,(randomcolor)),(width/2-80,75))

        if x>width/2-220 and x<width/2-20 and y>height/2 - 170 and y<height/2 - 20:
            pygame.draw.rect(screen,randomcolor,(width/2-225,height/2-175,210,160))
            self.select = 1
        elif x>width/2+20 and x<width/2+220 and y>height/2 - 170 and y<height/2 - 20:
            self.select = 2
            pygame.draw.rect(screen,randomcolor,(width/2+15,height/2-175,210,160))
        elif x>width/2-220 and x<width/2-20 and y>height/2 + 20 and y<height/2 + 170:
            self.select = 3
            pygame.draw.rect(screen,randomcolor,(width/2-225,height/2 + 15,210,160))
        elif x>width/2+20 and x<width/2+220 and y>height/2 + 20 and y<height/2 + 170:
            self.select = 4
            pygame.draw.rect(screen,randomcolor,(width/2+15,height/2+15,210,160))
        else:
            self.select = 0
            
        screen.blit(self.maplv1,(width/2-220,height/2-170))
        screen.blit(self.maplv2,(width/2+20,height/2-170))
        screen.blit(self.maplv3,(width/2-220,height/2+20))
        screen.blit(self.maplv4,(width/2+20,height/2+20))

        screen.blit(pygame.font.SysFont("Consolas",20).render("Level 1",True,randomcolor),(width/2-160,height/2-15))
        screen.blit(pygame.font.SysFont("Consolas",20).render("Level 2",True,randomcolor),(width/2 + 80,height/2-15))
        screen.blit(pygame.font.SysFont("Consolas",20).render("Level 3",True,randomcolor),(width/2-160,height/2 + 175))
        screen.blit(pygame.font.SysFont("Consolas",20).render("Level 4",True,randomcolor),(width/2 + 80,height/2 + 175))

    def Choose(self):
        while self.isChoose :
            self.drawChoose()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button ==1:
                        if self.select!=0:
                            self.isChoose = False
                            self.isplay = True

            clock.tick(FPS)
            pygame.display.update()


    #def start(self):



screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption("Pacman")

def drawFood():
    for i in range(0,row):
        for j in range(0,column):
            if(Map.table[i][j] == 2):
                pygame.draw.circle(screen,(0,38,230),(width_rec*j +width_rec/2 +x_root,width_rec*i+ width_rec/2 +y_root),5)

def drawWall():
    wall_color = (0, 38, 230)  # Color for the walls
    for i in range(row):
        for j in range(column):
            if Map.table[i][j] == 1:  # Check if the cell contains a wall
                # Draw a rectangle for the wall
                pygame.draw.rect(screen, wall_color, (j * width_rec + x_root, i * width_rec + y_root, width_rec, width_rec))

def drawTableBorder():
    border_color = (0, 38, 230)  # Color for the border

    # Draw a rectangle around the entire game area
    pygame.draw.rect(screen, border_color, (x_root, y_root, column * width_rec, row * width_rec), 5)

def getMonsters():
    monster = []
    monster_numbers = 0
    for i in range(row):
        for j in range(column):
            if Map.table[i][j] == 3:
                monster_numbers = monster_numbers + 1
                mon = Monster('monster' + str(monster_numbers) + '.png', i, j)
                monster.append(mon)
    
    return monster

def draw():
    randomcolor  = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    screen.blit(playgame.bg,(0,0))
    drawWall()
    drawFood()
    drawTableBorder()
    for mon in monster:
        mon.drawMonster()
    pacman.drawPacMan()
    for mon in monster:
        mon.drawMonster()
    if playgame.select == 3:
        drawBlind()
    
    pygame.draw.rect(screen, (0, 38, 230), (50,50,150,70), 5)
    screen.blit(pygame.font.SysFont("Consolas",20).render("Point: "+str(playgame.point),True,randomcolor ),(65,75))


def readFile(filename):
    global row,column
    f = open(filename,'r')
    data = f.read()
    data = data.split("\n\n")

    #reading information for table
    column = int(data[0][data[0].find(" ")+1:])
    row = int(data[0][0:data[0].find(" ")])

    t = data[1].split("\n")
    Map.initTable()
    for i in range(0,row):
        for j in range(0,column):
            Map.table[i][j] = int(t[i][j*2])
    
    #reading information for pacman
    pacman.posi = int(data[2][0])
    pacman.posj = int(data[2][2])

def DirectionFromTo(pos1,pos2):
    if(pos1.posi - pos2.posi) == 1 and pos1.posj == pos2.posj:
        return UP
    if(pos1.posi - pos2.posi) == -1 and pos1.posj == pos2.posj:
        return DOWN
    if(pos1.posj - pos2.posj) == 1 and pos1.posi == pos2.posi:
        return LEFT
    if(pos1.posj - pos2.posj) == -1 and pos1.posi == pos2.posi:
        return RIGHT
    else: 
        return -1

def DirectionCanGoUp(i,j):
    direction = []
    if j != column -1 and Map.table[i][j + 1] != 1: 
        if playgame.select == 3:
            if  tablelv3[i][j+1]!=-1:
                direction.append(RIGHT)
        else:
            direction.append(RIGHT)
    if j != 0 and Map.table[i][j - 1] != 1: 
        if playgame.select == 3:
            if  tablelv3[i][j-1]!=-1:
                direction.append(LEFT)
        else:
            direction.append(LEFT)
    if i != 0  and Map.table[i - 1][j] != 1: 
        if playgame.select == 3:
            if  tablelv3[i-1][j]!=-1:
                direction.append(UP)
        else:
            direction.append(UP)
    if i != row -1 and Map.table[i + 1][j] != 1: 
        if playgame.select == 3:
            if  tablelv3[i+1][j]!=-1:
                direction.append(DOWN)
        else:
            direction.append(DOWN)
    
    return direction

def PositionCanGoUp(i,j):
    result =[]
    direction = DirectionCanGoUp(i,j)
    for t in range(0,len(direction)):
        if direction[t] == LEFT:
            result.append(Position(i,j -1))
        elif direction[t] == RIGHT:
            result.append(Position(i,j +1))
        elif direction[t] == UP:
            result.append(Position(i -1,j))
        elif direction[t] == DOWN:
            result.append(Position(i + 1,j))

    return result

def drawResult(time):
    isresult = True
    while isresult:
        isselect = False
        x,y = pygame.mouse.get_pos()
        randomcolor  = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        screen.blit(playgame.bg,(0,0))
        pygame.draw.rect(screen, (0, 38, 230), (width/2-150,height/2-150,300,300), 5)
        screen.blit(pygame.font.SysFont("Consolas",40).render("Point: "+str(playgame.point),True,(255,51,153) ),(width/2-120,height/2-140))
        screen.blit(pygame.font.SysFont("Consolas",40).render("Cost: "+str(playgame.cost),True,(255,51,153) ),(width/2-120,height/2-90))
        screen.blit(pygame.font.SysFont("Consolas",40).render("Time: "+str(time) +"s",True,(255,51,153) ),(width/2-120,height/2-40))

        #pygame.draw.ellipse(screen,(0,38,253),(width/2-50,height/2 + 20,100,70))
        if x>width/2-20 and x<width/2+20 and y>height/2+45 and y<height/2+65:
            screen.blit(pygame.font.SysFont("Consolas",20).render("Back",True,(0,38,230) ),(width/2-20,height/2+45))
            isselect = True
        else:
            screen.blit(pygame.font.SysFont("Consolas",20).render("Back",True,randomcolor ),(width/2-20,height/2+45))
            isselect = False


        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button ==1:
                    if isselect:
                        isresult = False


        clock.tick(FPS)
        pygame.display.update()

while True:
    width_rec=45
    pacman = PacMan()
    Map = TableGame()
    playgame = PlayGame()
    playgame.Choose()
    if playgame.select == 1:
        readFile("./map/map1_n.txt")
    elif playgame.select == 2:
        readFile("./map/map2_1nopath.txt")
    elif playgame.select == 3:
        num = random.randint(1, 2)
        readFile("./map/map3_" + str(num) + ".txt")
        initTableLv3()
    elif playgame.select == 4:
        num = random.randint(1, 2)
        readFile("./map/map4_" + str(num) + ".txt")
        width_rec=30

    monster = getMonsters()
    timestart = time.time()
    while playgame.isplay:
        #Map.UpdateTable(pacman.posi,pacman.posj)
        if (Map.checkWin()):
            playgame.isplay =False
        width,height = screen.get_size()
        x_root =  width/2 - column* width_rec/2
        y_root = height/2 - row*width_rec/2
        draw()
        
        for mon in monster:
            if (mon.IsGameLose()):
                playgame.isplay = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(FPS)
        pygame.display.update()
    
    drawResult(round(time.time() - timestart))