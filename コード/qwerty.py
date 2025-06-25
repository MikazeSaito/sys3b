import pygame
import random
import sys
def old_car(x_y_speed,cross,cars,circles):
    x=x_y_speed[0][0]
    y=x_y_speed[0][1]
    speed=x_y_speed[1]
    for hodo in cross:
        if speed>0:
            if hodo[0]-20<x and hodo[0]>x:
                return [[x,y],speed]
        else:
            if hodo[0]+250*60/340+20>x and hodo[0]+250*60/340<x:
                return [[x,y],speed]
    for car in cars:
        if speed>0:
            if car[0][0]-30<x and car[0][0]>x and car[1]>0:
                return [[x,y],speed]
        else:
            if car[0][0]+30>x and car[0][0]<x and car[1]<0:
                return [[x,y],speed]
    for human in circles:
        if speed>0:
            if human[2]==1 and human[0][0]-30<x and human[0][0]>x:
                return [[x,y],speed]
        else:
            if human [2]==1 and human[0][0]+30>x and human[0][0]<x:
                return [[x,y],speed]
    x+=speed*0.03
    return [[x,y],speed]


def new_system(circles,a,b):
    sum=0
    count=0
    for human in circles:
        if human[0][0]>a and human[0][0]<b:
            sum+=human[0][0]
            count+=1
    if count==0:
        return [0,0]
    else:
        return [sum/count,195]
    

def old_human(x_y_speed,cross):
    x=x_y_speed[0][0]
    y=x_y_speed[0][1]
    x_speed=x_y_speed[1][0]
    y_speed=x_y_speed[1][1]
    statas=x_y_speed[2]
    if statas==0:
        for hodo in cross:
            if hodo[0]<x and x<hodo[0]+250*60/340:
                statas=1
                if y==640:
                    y_speed=abs(x_speed)
                    x_speed=0
                else:
                    y_speed=-abs(x_speed)
                    x_speed=0
                break
    else:
        if y_speed>0 and y>710:
            statas=2
        elif y_speed<0 and y<640:
            statas=2
    x+=x_speed*0.03
    y+=y_speed*0.03
    return [[x,y],[x_speed,y_speed],statas]


def new_human(x_y_speed,cross):
    x=x_y_speed[0][0]
    y=x_y_speed[0][1]
    x_speed=x_y_speed[1][0]
    y_speed=x_y_speed[1][1]
    statas=x_y_speed[2]
    if statas==0:
        for hodo in cross:
            if hodo[0]<x and x<hodo[0]+250*60/340:
                statas=1
                if y==190:
                    y_speed=abs(x_speed)
                    x_speed=0
                else:
                    y_speed=-abs(x_speed)
                    x_speed=0
                break
    else:
        if y_speed>0 and y>260:
            statas=2
        elif y_speed<0 and y<190:
            statas=2
    x+=x_speed*0.03
    y+=y_speed*0.03
    return [[x,y],[x_speed,y_speed],statas]
    



# 初期化
pygame.init()
screen = pygame.display.set_mode((1400,900))
pygame.display.set_caption("クリックで円を描く")
image = pygame.image.load("road.png")
resized_image = pygame.transform.scale(image, (240, 60))
image2=pygame.image.load("cross.png")
resized_image2 = pygame.transform.scale(image2, (250*60/340, 60))
clock = pygame.time.Clock()
clock.tick(30)
count=0

# 色
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 円の情報を保持するリスト
circles1 = []
circles2=[]
cars1=[]
cars2=[]
cross1=[]
cross2=[]
""""i=0
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                i=1
                break
        elif event.type == pygame.MOUSEBUTTONDOWN:
                # クリックした座標を取得
            pos = list(pygame.mouse.get_pos())
            speed=int(input("speed="))
            circles.append([pos,speed])
            pos2=[pos[0]+700,pos[1]]
            circles.append([pos2,speed])
            print([pos2,speed])
    if i==1:
        break"""

running = True
while running:
    count+=1
    if random.random()<0.001:
        cars1.append([[0,210],20])
        cars2.append([[0,660],20])
    if random.random()<0.001:
        cars1.append([[1400,240],-20])
        cars2.append([[1400,690],-20])
    if random.random()<0.005:
        x=random.uniform(0,1400)
        y=random.choice([-35,35])
        speed=random.uniform(4,5)
        vec=random.choice([-1,1])
        circles1.append([[x,y+225],[speed*vec,0],0])
        circles2.append([[x,y+675],[speed*vec,0],0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 画面を白でクリア
    screen.fill(WHITE)
    pygame.draw.line(screen, (0, 0, 0), (0, 450), (1400, 450), 10)
    for i in range(0,1400,240):
        screen.blit(resized_image, (i, 195))
        screen.blit(resized_image, (i, 645))
    # クリックした場所に赤い円を描画
    if count==600:
        for i in range(0,1400,400):
            x=new_system(circles1,i,i+400)
            if x[1]!=0:
                cross1.append(x)
            cross2.append([i,645])
    if count==1200:
        for i in range(0,1400,400):
            cross2.remove([i,645])
        cross1.clear()
    for x in cross2:
        screen.blit(resized_image2, (x[0], x[1]))

    for x in cross1:
        screen.blit(resized_image2, (x[0], x[1]))
        
    for center in circles1:
        pygame.draw.circle(screen, RED, center[0], 10)
        center_new = new_human(center, cross1)
        center[0] = center_new[0]
        center[1] = center_new[1]
        center[2] = center_new[2]
        if center[0][0]<0 or center[0][0]>1400:
            circles1.remove(center)
        elif center[2]==2:
            circles1.remove(center)           
    for center in circles2:
        pygame.draw.circle(screen, RED, center[0], 10)
        center_new = old_human(center, cross2)
        center[0] = center_new[0]
        center[1] = center_new[1]
        center[2] = center_new[2]
        if center[0][0]<0 or center[0][0]>1400:
            circles2.remove(center)
        elif center[2]==2:
            circles2.remove(center)
    for car in cars1:
        pygame.draw.circle(screen, 'BLUE', car[0], 10)
        new_car=old_car(car,cross1,cars1,circles1)
        car[0]=new_car[0]
        car[1]=new_car[1]
        if car[0][0]<0 or car[0][0]>1400:
            cars1.remove(car)
    for car in cars2:
        pygame.draw.circle(screen, 'BLUE', car[0], 10)
        new_car=old_car(car,cross2,cars2,circles2)
        car[0]=new_car[0]
        car[1]=new_car[1]
        if car[0][0]<0 or car[0][0]>1400:
            cars2.remove(car)
    if count==1200:
        count=0
    pygame.display.flip()
    

pygame.quit()