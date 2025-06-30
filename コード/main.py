import pygame
import random
import numpy as np
from functions import old_human,make_happy,make_wait,calculate,old_car,new_car,new_system,new_human,make_car_waiting_time,make_human_waiting_time,calculate2


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


# 色
WHITE = ( 255 , 255 , 255 )
RED = ( 255 , 0 , 0 )


# 人、車、横断歩道の情報を管理するリスト(1は最適化、2は従来)
humans1 = []
humans2 = []
cars1 = []
cars2 = []
crosses1 = []
crosses2 = []


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
        want = x + speed * vec * 50
        humans1.append( [ [ x , y + road1_y ] , [ speed * vec , 0 ] , 0 , want ] )
        humans2.append( [ [ x , y + road2_y ] , [ speed * vec , 0 ] , 0 , want ] )

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
        for i in range ( 0 , 1400 , 280 ):
            x , start_time , end_time = calculate2( humans1 , cars1 , i , i + 280 ,cross_width)
            if start_time != 0:
                crosses1.append( [ [ x , cross1_y ] , start_time , end_time ] )
            crosses2.append( [ i , cross2_y ] )

    if time == 3000: #横断歩道を消去
        crosses2.clear()
        crosses1.clear()

    for x in crosses2:
        screen.blit( resized_image2 , ( x[ 0 ], x[ 1 ] ) )

    for x in crosses1:
        x[ 1 ] -= 1
        x[ 2 ] -= 1
        if x[ 1 ] < 1 and x[ 2 ] > 0:
            screen.blit( resized_image2 , ( x[ 0 ][ 0 ], x[ 0 ][ 1 ] ) )
        elif x[ 1 ] > 0:
            screen.blit( resized_image3 , ( x[ 0 ][ 0 ], x[ 0 ][ 1 ] ) )

    # 人の動きを決定 
    for human in humans1:
        pygame.draw.circle( screen , RED , human[ 0 ] , human_radi ) 
        human_new = new_human( human , crosses1 , cross_width , human1_1_y , human1_2_y )
        human[ 0 ] = human_new[ 0 ]
        human[ 1 ] = human_new[ 1 ]
        human[ 2 ] = human_new[ 2 ]
        if human[ 0 ][ 0 ] < 0 or human[ 0 ][ 0 ] > 1400:
            humans1.remove( human )
            bad1 += 1
        elif human[ 2 ] == 2:
            humans1.remove( human )
            happy1 += 1   

    for human in humans2:
        pygame.draw.circle( screen , RED , human[ 0 ] , human_radi )
        human_new = old_human( human , crosses2 ,cross_width , human2_1_y , human2_2_y )
        human[ 0 ] = human_new[ 0 ]
        human[ 1 ] = human_new[ 1 ]
        human[ 2 ] = human_new[ 2 ]
        if human[ 0 ][ 0 ] < 0 or human[ 0 ][ 0 ] > 1400:
            humans2.remove( human )
            bad2+=1
        elif human[ 2 ] == 2:
            humans2.remove( human )
            happy2 += 1

    #車の動きを決定
    for car in cars1:
        pygame.draw.circle( screen , 'BLUE' , car[ 0 ] , car_radi ) 
        n_car = new_car( car , crosses1 , cars1 , humans1 ,cross_width )
        car[ 0 ] = n_car[ 0 ]
        car[ 1 ] = n_car[ 1 ]
        if car[ 0 ][ 0 ] < 0 or car[ 0][ 0 ] > 1400:
            cars1.remove( car )

    for car in cars2:
        pygame.draw.circle( screen , 'BLUE' , car[ 0 ] , car_radi )
        n_car = old_car( car , crosses2 , cars2 , humans2 , cross_width )
        car[ 0 ] = n_car[ 0 ]
        car[ 1 ] = n_car[ 1 ]
        if car[ 0 ][ 0 ] < 0 or car[ 0 ][ 0 ] > 1400:
            cars2.remove( car )

    #得点を表示
    text1 = font.render( f"BAD: {bad1}" , True , ( 0 , 0 , 0 ) )
    text2 = font.render( f"BAD: {bad2}" , True , ( 0 , 0 , 0 ) )
    text3 = font.render( f"GOOD: {happy1}" , True , ( 0 , 0 , 0 ) )
    text4 = font.render( f"GOOD: {happy2}" , True , ( 0, 0 , 0 ) )
    screen.blit( text1 , ( 20 , 20 ) )
    screen.blit( text2 , ( 20 , 470 ) )
    screen.blit( text3 , ( 170 , 20 ) )
    screen.blit( text4 , ( 170 , 470 ) )

    if time == 3000:
        time = 0
    pygame.display.flip()
    

pygame.quit()