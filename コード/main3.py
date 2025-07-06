import pygame
import random
import numpy as np
from functions2 import to_be_able_to_cross,calculate4,group_numbers_by_threshold,group_numbers_greedy_min_groups,calculate3,old_human,old_human2,make_happy,make_wait,calculate,old_car,new_car,new_system,new_human,make_car_waiting_time,make_human_waiting_time,calculate2


# 横断歩道の幅と道路の幅,位置を設定　車の速さなども設定
road_width = 40
cross_width = 250 * road_width / 340
road1_y = 225
road2_y = 675
delta = 3
cross1_y = road1_y - road_width / 2
cross2_y = road2_y - road_width / 2
car1_1_y = road1_y - road_width / 4
car2_1_y = road2_y - road_width / 4
car1_2_y = road1_y + road_width / 4
car2_2_y = road2_y + road_width / 4
human1_1_y = road1_y - road_width / 2 - delta
human1_2_y = road1_y + road_width / 2 + delta
human2_1_y = road2_y - road_width / 2 - delta
human2_2_y = road2_y + road_width / 2 + delta
car_speed = 1
human_radi = 6
car_radi = 6
human_low_speed = 0.08
human_high_speed = 0.1
human_wait1=0
have_to_walk1=0
car_wait1=0
human_wait2=0
have_to_walk2=0
car_wait2=0
a,b,c,d=0,0,0,0
right=1400
left=0

# 初期化
pygame.init()
screen = pygame.display.set_mode(( 1400 , 900 ))
pygame.display.set_caption( "横断歩道シミュレーション" )
image = pygame.image.load( "road.png" )
resized_image = pygame.transform.scale( image , ( road_width * 4 , road_width ))
image2 = pygame.image.load( "cross.png" )
resized_image2 = pygame.transform.scale( image2 , ( cross_width , road_width ))
image3 = pygame.image.load( "virtual_crossing.png" )
resized_image3 = pygame.transform.scale( image3 , ( cross_width , road_width ))
font = pygame.font.Font( None , 36 )


time = 0 #横断歩道の周期を管理
bad1 = 0 #横断歩道を渡れなかった人数
bad2 = 0
happy1 = 0 #横断歩道を渡れた人数
happy2 = 0
virtual_time=1000

# 色
WHITE = ( 255 , 255 , 255 )
RED = ( 255 , 0 , 0 )


# 人、車、横断歩道の情報を管理するリスト(1は最適化、2は従来)
humans2 = []
cars1 = []
cars2 = []
crosses1 = []
crosses2 = []
humans1below = []
humans1above = []

running = True
while running:
    time += 1
    # 車と人をランダム生成
    if random.random()<0.0015:
        cars1.append( [ [ 0 , car1_1_y ] , car_speed] )
        cars2.append( [ [ 0 , car2_1_y ] , car_speed] )

    if random.random()<0.0015:
        cars1.append( [ [ 1400 , car1_2_y ] , -car_speed ] )
        cars2.append( [ [ 1400 , car2_2_y ] , -car_speed ] )

    if random.random()<0.01:
        x = random.uniform( 0 , 1400 )
        y = random.choice( [ -road_width / 2 - delta , road_width / 2 + delta ] )
        speed = random.uniform( human_low_speed , human_high_speed )
        vec = random.choice( [ -1 , 1 ] )
        want = x + speed * vec * random.uniform(200,2000)
        want=max(want,0)
        want=-max(-want,-1400)
        _min=100000
        want_cross=0
        for i in range( 0 , 1400 , 280 ):
            if abs(want - i) <_min:
                _min = abs( want - i )
                want_cross = i
        vec2 = (want_cross - x) / abs(want_cross - x)
        humans2.append( [ [ x , y + road2_y ] , [ speed * vec2 , 0 ] , 0 , want,want_cross ,0] )

        if time<=1500:
            color='RED'
            vec3=vec
        else:
            color='YELLOW'
            vec3=to_be_able_to_cross(x,speed,vec,crosses1,road_width)
            if vec!=vec3:
                color='GREEN'
       
        if vec < 0:
            humans1below.append([ [ x , y + road1_y ] , [ speed * vec3 , 0 ] , 0 , want ,0,color] )
            
        else:
            humans1above.append([ [ x , y + road1_y ] , [ speed * vec3 , 0 ] , 0 , want ,0,color] )  



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 画面を白でクリア
    screen.fill( WHITE )
    pygame.draw.line( screen , ( 0 , 0 , 0 ) , ( 0 , 450 ) , ( 1400 , 450 ) , 10)

    # 道路を表示
    for i in range( 0 , 1400 , road_width * 4 ):
        screen.blit( resized_image , ( i , cross1_y ) )
        screen.blit( resized_image , ( i , cross2_y ) )

    if time == 1500: #横断歩道の表示場所や時間を決定
        ranges=calculate4(humans1below,humans1above,virtual_time)
        sum=0
        for R in ranges:
            locate , start_time , end_time=calculate2(humans1above,humans1below , cars1 , int(R[0])-20 , int(R[1])+20 ,cross_width , road_width,virtual_time)
            crosses1.append([ [ locate , cross1_y ] , start_time , end_time ])
            sum+=start_time+end_time
            if locate<left:
                left=locate
            elif locate>right:
                right=locate
        virtual_time=sum/(2*len(ranges))
        for i in range ( 0 , 1400 , 280 ):
            crosses2.append([ [ i , cross2_y ] , 0 , 1500 ])

    if time == 3000: #横断歩道を消去
        crosses2.clear()
        crosses1.clear()

    for x in crosses2:
        x[ 1 ] -= 1
        x[ 2 ] -= 1
        screen.blit( resized_image2 , ( x[ 0 ][ 0 ], x[ 0 ][ 1 ] ) )

    for x in crosses1:
        x[ 1 ] -= 1
        x[ 2 ] -= 1
        if x[ 1 ] < 1 and x[ 2 ] > 0:
            screen.blit( resized_image2 , ( x[ 0 ][ 0 ], x[ 0 ][ 1 ] ) )
        elif x[ 1 ] > 0:
            screen.blit( resized_image3 , ( x[ 0 ][ 0 ], x[ 0 ][ 1 ] ) )

    # 人の動きを決定 
    for human in humans1above:
        pygame.draw.circle( screen , human[5] , human[ 0 ] , human_radi ) 
        human_new = new_human( human , crosses1 , cross_width , human1_1_y , human1_2_y )
        if human[0]==human_new[0]:
            human[4]+=1
        if human[2]==0 and human_new[2]==1:
            if (human[3]-human[0][0])/human[1][0]<0:
                have_to_walk1+=2*abs(human[3]-human[0][0])
        human[ 0 ] = human_new[ 0 ]
        human[ 1 ] = human_new[ 1 ]
        human[ 2 ] = human_new[ 2 ]

        if human[ 0 ][ 0 ] < min(left,0) or human[ 0 ][ 0 ] > max(1400,right):
            humans1above.remove( human )

            bad1 += 1
        elif human[ 2 ] == 2:
            human_wait1+=human[4]
            humans1above.remove( human )
            happy1 += 1   
    for human in humans1below:
        pygame.draw.circle( screen , human[5] , human[ 0 ] , human_radi ) 
        human_new = new_human( human , crosses1 , cross_width , human1_1_y , human1_2_y )
        if human[0]==human_new[0]:
            human[4]+=1
        if human[2]==0 and human_new[2]==1:
            if (human[3]-human[0][0])/human[1][0]<0:
                have_to_walk1+=2*abs(human[3]-human[0][0])
        human[ 0 ] = human_new[ 0 ]
        human[ 1 ] = human_new[ 1 ]
        human[ 2 ] = human_new[ 2 ]

        if human[ 0 ][ 0 ] < min(left,0) or human[ 0 ][ 0 ] > max(1400,right):
            humans1below.remove( human )

            bad1 += 1
        elif human[ 2 ] == 2:
            human_wait1+=human[4]
            humans1below.remove( human )
            happy1 += 1   

    for human in humans2:
        pygame.draw.circle( screen , RED , human[ 0 ] , human_radi )
        human_new = old_human2( human , crosses2 ,cross_width , human2_1_y , human2_2_y )
        if human[0]==human_new[0]:
            human[5]+=1
        if human[2]==0 and human_new[2]==1:
            if (human[3]-human[0][0])/human[1][0]<0:
                have_to_walk2+=2*abs(human[3]-human[0][0])
        human[ 0 ] = human_new[ 0 ]
        human[ 1 ] = human_new[ 1 ]
        human[ 2 ] = human_new[ 2 ]

        if human[ 0 ][ 0 ] < 0 or human[ 0 ][ 0 ] > 1400:
            humans2.remove( human )
            bad2+=1
        elif human[ 2 ] == 2:
            human_wait2+=human[5]
            humans2.remove( human )
            happy2 += 1
            

    #車の動きを決定
    for car in cars1:
        pygame.draw.circle( screen , 'BLUE' , car[ 0 ] , car_radi ) 
        n_car = new_car( car , crosses1 , cars1 , humans1below, humans1above ,cross_width ,road1_y)
        if car[0]==n_car[0]:
            car_wait1+=1
        car[ 0 ] = n_car[ 0 ]
        car[ 1 ] = n_car[ 1 ]
        if car[ 0 ][ 0 ] < 0 or car[ 0][ 0 ] > 1400:
            cars1.remove( car )

    for car in cars2:
        pygame.draw.circle( screen , 'BLUE' , car[ 0 ] , car_radi )
        n_car = old_car( car , crosses2 , cars2 , humans2 , cross_width ,road2_y)
        if car[0]==n_car[0]:
            car_wait2+=1
        car[ 0 ] = n_car[ 0 ]
        car[ 1 ] = n_car[ 1 ]
        if car[ 0 ][ 0 ] < 0 or car[ 0 ][ 0 ] > 1400:
            cars2.remove( car )
    
    if happy1!=0 and time==3000:
        crossing_human=0
        for human in humans1above:
            if human[2]==1:
                crossing_human+=1
        for human in humans1below:
            if human[2]==1:
                crossing_human+=1       
        a=human_wait1/(happy1+crossing_human)
        c=have_to_walk1/(happy1+crossing_human)
    if happy2!=0 and time==3000:
        crossing_human=0
        for human in humans1below:
            if human[2]==1:
                crossing_human+=1
        b=human_wait2/(happy2+crossing_human)
        d=have_to_walk2/(happy2+crossing_human)
    #得点を表示
    text1 = font.render( f"BAD: {bad1}" , True , ( 0 , 0 , 0 ) )
    text2 = font.render( f"BAD: {bad2}" , True , ( 0 , 0 , 0 ) )
    text3 = font.render( f"GOOD: {happy1}" , True , ( 0 , 0 , 0 ) )
    text4 = font.render( f"GOOD: {happy2}" , True , ( 0, 0 , 0 ) )
    text5 = font.render( f"human_wait: {round(a,3)}" , True , ( 0 , 0 , 0 ) )
    text6 = font.render( f"human_wait: {round(b,3)}" , True , ( 0 , 0 , 0 ) )
    text7 = font.render( f"car_wait: {round(car_wait1)}" , True , ( 0 , 0 , 0 ) )
    text8 = font.render( f"car_wait: {round(car_wait2)}" , True , ( 0 , 0 , 0 ) )
    text9 = font.render( f"have_to_walk: {round(c)}" , True , ( 0 , 0 , 0 ) )
    text10 = font.render( f"have_to_walk: {round(d)}" , True , ( 0 , 0 , 0 ) )
    screen.blit( text1 , ( 20 , 20 ) )
    screen.blit( text2 , ( 20 , 470 ) )
    screen.blit( text3 , ( 170 , 20 ) )
    screen.blit( text4 , ( 170 , 470 ) )
    screen.blit( text5 , ( 400 , 20 ) )
    screen.blit( text6 , ( 400 , 470 ) )
    screen.blit( text7 , ( 800 , 20 ) )
    screen.blit( text8 , ( 800 , 470 ) )
    screen.blit( text9 , ( 1100 , 20 ) )
    screen.blit( text10 , ( 1100 , 470 ) )
    if time == 3000:
        time = 0
        right=1400
        left=0
    pygame.display.flip()
    

pygame.quit()