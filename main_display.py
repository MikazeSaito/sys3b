import pygame
import math
import random
import numpy as np
from functions2 import multipurpose,make_human_waiting_time2,to_be_able_to_cross,calculate4,group_numbers_by_threshold,group_numbers_greedy_min_groups,calculate3,old_human,old_human2,make_happy,make_wait,calculate,old_car,new_car,new_system,new_human,make_car_waiting_time,make_human_waiting_time,calculate2
import matplotlib.pyplot as plt
import seaborn as sns

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
car_speed = 1.2
human_radi = 6
car_radi = 6
human_low_speed = 0.1
human_high_speed = 0.12
human_wait1=0
have_to_walk1=0
car_wait1=0
human_wait2=0
have_to_walk2=0
car_wait2=0
a,b,c,d=0,0,0,0
right=1400
left=0
max_have_to_walk1=0
max_have_to_walk2=0

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
walk1=[]
walk2=[]
player_list=[]
playcar_list=[]
time = 0 #横断歩道の周期を管理
bad1 = 0 #横断歩道を渡れなかった人数
bad2 = 0
happy1 = 0 #横断歩道を渡れた人数
happy2 = 0
virtual_time=1000
player_speed = random.uniform( human_low_speed , human_high_speed )
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
clock=pygame.time.Clock()
running = True
while running:
    
    time += 1
    # 車と人をランダム生成
    if random.random()<0.005:
        cars1.append( [ [ 0 , car1_1_y ] , car_speed] )
        cars2.append( [ [ 0 , car2_1_y ] , car_speed] )

    if random.random()<0.005:
        cars1.append( [ [ 1400 , car1_2_y ] , -car_speed ] )
        cars2.append( [ [ 1400 , car2_2_y ] , -car_speed ] )

    if random.random()<0.01:
        x = random.uniform( 0 , 1400 )
        y = random.choice( [ -road_width / 2 - delta , road_width / 2 + delta ] )
        speed = random.uniform( human_low_speed , human_high_speed )
        vec = random.choice( [ -1 , 1 ] )
        want = x + speed * vec * random.uniform(200,5000)
        want=max(want,0)
        want=-max(-want,-1400)
        _min=100000
        want_cross=0
        for i in range( 0 , 1400 , 420 ):
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





    # 画面を白でクリア
    screen.fill( WHITE )
    pygame.draw.line( screen , ( 0 , 0 , 0 ) , ( 0 , 450 ) , ( 1400 , 450 ) , 10)

    # 道路を表示
    for i in range( 0 , 1400 , road_width * 4 ):
        screen.blit( resized_image , ( i , cross1_y ) )
        screen.blit( resized_image , ( i , cross2_y ) )

    if time == 1500: #横断歩道の表示場所や時間を決定
        player_below=[]
        player_above=[]
        if player_list:
            for player in player_list:
                if player[1][0]<0:
                    player_below.append(player)
                if player[1][0]>0:
                    player_above.append(player)
        ranges=calculate4(humans1below+player_below,humans1above+player_above,virtual_time)
        sum=0
        for R in ranges:
            locate , start_time , end_time=multipurpose(humans1below+player_below,humans1above+player_above , cars1+playcar_list , int(R[0])-20 , int(R[1])+20 ,cross_width , road_width,virtual_time)
            crosses1.append([ [ locate , cross1_y ] , start_time , end_time+cross_width/0.2 ])
            sum+=5*start_time+7*end_time
            if locate<left:
                left=locate
            elif locate>right:
                right=locate
        virtual_time=sum/(12*len(ranges))

        for i in range ( 0 , 1400 , 420 ):
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
                walk1.append(math.floor(2*abs(human[3]-human[0][0])*6/4)/10)
                have_to_walk1+=2*abs(human[3]-human[0][0])
                if 2*abs(human[3]-human[0][0])>max_have_to_walk1:
                    max_have_to_walk1=2*abs(human[3]-human[0][0])
            else:
                walk1.append(0)
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
                walk1.append(math.floor(2*abs(human[3]-human[0][0])*6/4)/10)
                if 2*abs(human[3]-human[0][0])>max_have_to_walk1:
                    max_have_to_walk1=2*abs(human[3]-human[0][0])
                have_to_walk1+=2*abs(human[3]-human[0][0])
            else:
                walk1.append(0)
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
                walk2.append(math.floor(2*abs(human[3]-human[0][0])*6/4)/10)
                have_to_walk2+=2*abs(human[3]-human[0][0])
                if 2*abs(human[3]-human[0][0])>max_have_to_walk2:
                    max_have_to_walk2=2*abs(human[3]-human[0][0])
            else:
                walk2.append(0)
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
        player_danger=[]
        if player_list:
            for player in player_list:
                if human1_1_y+2<player[0][1]<human1_2_y-2:
                    player_danger.append(player)
                
        n_car = new_car( car , crosses1 , cars1+playcar_list , humans1below+player_danger, humans1above ,cross_width ,road1_y)
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
    text1 = font.render( f"Human out of the screen: {bad1}" , True , ( 0 , 0 , 0 ) )
    text2 = font.render( f"Human out of the screen: {bad2}" , True , ( 0 , 0 , 0 ) )
    text3 = font.render( f"Human who had crossed: {happy1}" , True , ( 0 , 0 , 0 ) )
    text4 = font.render( f"Human who had crossed: {happy2}" , True , ( 0, 0 , 0 ) )
    text5 = font.render( f"Average of humans' waiting time: {math.floor(a/6)/10}s" , True , ( 0 , 0 , 0 ) )
    text6 = font.render( f"Average of humans' waiting time: {math.floor(b/6)/10}s" , True , ( 0 , 0 , 0 ) )
    text7 = font.render( f"Sum of cars' waiting time: {math.floor(car_wait1/6)/10}s" , True , ( 0 , 0 , 0 ) )
    text8 = font.render( f"Sum of cars' waiting time: {math.floor(car_wait2/6)/10}s" , True , ( 0 , 0 , 0 ) )
    text9 = font.render( f"Average wasted walking distance: {math.floor(c*6/4)/10}m" , True , ( 0 , 0 , 0 ) )
    text10 = font.render( f"Average wasted walking distance: {math.floor(d*6/4)/10}m" , True , ( 0 , 0 , 0 ) )
    text11 = font.render( f"Max wasted walking distance: {math.floor(max_have_to_walk1*6/4)/10}m" , True , ( 0 , 0 , 0 ) )
    text12 = font.render( f"Max wasted walking distance: {math.floor(max_have_to_walk2*6/4)/10}m" , True , ( 0 , 0 , 0 ) )
    screen.blit( text1 , ( 20 , 20 ) )
    screen.blit( text2 , ( 20 , 470 ) )
    screen.blit( text3 , ( 500 , 20 ) )
    screen.blit( text4 , ( 500 , 470 ) )
    screen.blit( text5 , ( 900 , 20 ) )
    screen.blit( text6 , ( 900 , 470 ) )
    screen.blit( text7 , ( 20 , 60 ) )
    screen.blit( text8 , ( 20 , 510 ) )
    screen.blit( text9 , ( 600 , 60 ) )
    screen.blit( text10 , ( 600 , 510 ) )
    screen.blit( text11 , ( 20 , 100 ) )
    screen.blit( text12 , ( 20 , 550 ) )
    for cross in crosses1:
        if cross[1]>0:
            text = font.render( f" {math.floor(cross[1]/60)}" , True , 'red' )
            screen.blit( text , ( cross[0][0] , cross[0][1] ) )
        elif cross[2]>0:
            text = font.render( f" {math.floor(cross[2]/60)}" , True , 'red' )
            screen.blit( text , ( cross[0][0] , cross[0][1] ) )
    if time == 3000:
        time = 0
        right=1400
        left=0


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(player_list)==0:
                # スペースキーが押されたら新しいプレイヤーをランダムな位置に作成
                player_x = random.uniform( 200 , 1200 )
                player_y = human1_2_y
                
                player_vec = random.choice( [ -1 , 1 ] )
                player_want = player_x + player_speed * player_vec * random.uniform(200,5000)
                player_want=max(player_want,0)
                player_want=-max(-player_want,-1400)
                player_list.append([[player_x,player_y],[player_speed*player_vec,player_speed*player_vec],0,player_want,0,'black'])
            if event.key==pygame.K_RETURN and len(playcar_list)==0:
                playcar_list.append([[0,car1_1_y],car_speed])


    # キーが押され続けているかの判定（長押し対応）
    keys = pygame.key.get_pressed()
    if player_list: # 操作中のプレイヤーが存在する場合のみ
        for human in player_list:
            if keys[pygame.K_LEFT]:
                human[0][0] -= abs(human[1][0])
                human[1][0]=-player_speed
                human[1][1]=0
                human[2]=0
            elif keys[pygame.K_RIGHT]:
                human[0][0] += abs(human[1][0])
                human[1][0]=player_speed
                human[1][1]=0
                
            elif keys[pygame.K_UP]:
                human[0][1] -= abs(human[1][1])
                human[1][1]=-player_speed
                human[1][0]=0
                
            elif keys[pygame.K_DOWN]:
                human[0][1] += abs(human[1][1])
                human[1][1]=player_speed
                human[1][0]=0
                
            else:
                human[1][1]=0
                human[1][0]=0
            if human1_1_y+2<human[0][1]<human1_2_y-2:
                human[2]=1
            else:
                human[2]=0
            if human[0][1]<human1_1_y:
                player_list.clear() 
            pygame.draw.circle( screen , human[5] , human[ 0 ] , human_radi*1.2 ) 
            text = font.render( f"G" , True , 'red' )
            screen.blit( text , ( human[3]-5 , human1_1_y-10 ) )


    if playcar_list:
        for playcar in playcar_list:
            if keys[pygame.K_LEFT]:
                playcar[1]-=0.006
                playcar[1]=max(playcar[1],0)
            elif keys[pygame.K_RIGHT]:
                playcar[1]+=0.008
                playcar[1]=min(playcar[1],1.2)
            playcar[0][0]+=playcar[1]
            
            pygame.draw.circle( screen , 'black' ,playcar[0] , car_radi*1.2 )
            if playcar[0][0]>1400:
                playcar_list.clear()
    pygame.draw.circle( screen , 'gray' , [530,human1_1_y] , human_radi ) 
    pygame.draw.circle( screen , 'gray' , [560,human1_1_y] , human_radi ) 
    pygame.draw.circle( screen , 'gray' , [590,human1_1_y] , human_radi )
    pygame.draw.circle( screen , 'gray' , [620,human1_1_y] , human_radi )
    pygame.draw.circle( screen , 'gray' , [650,human1_1_y] , human_radi )  
    pygame.draw.circle( screen , 'gray' , [680,human1_1_y] , human_radi )  
    pygame.draw.circle( screen , 'gray' , [530,human1_2_y] , human_radi ) 
    pygame.draw.circle( screen , 'gray' , [560,human1_2_y] , human_radi ) 
    pygame.draw.circle( screen , 'gray' , [590,human1_2_y] , human_radi )
    pygame.draw.circle( screen , 'gray' , [620,human1_2_y] , human_radi )
    pygame.draw.circle( screen , 'gray' , [650,human1_2_y] , human_radi )  
    pygame.draw.circle( screen , 'gray' , [680,human1_2_y] , human_radi ) 
    real_cross_list=[]
    for cross in crosses1:
        if 530<cross[0][0]<680:
            if cross[1]>0:
                real_cross_list.append([(cross[0][0]-530+cross_width/2)/30, 'blue'])
            elif cross[2]>0:
                real_cross_list.append([(cross[0][0]-530+cross_width/2)/30, 'white'])
    
    pygame.display.flip()
    

pygame.quit()
all_walk_data = []
if walk1:
    all_walk_data.extend(walk1)
if walk2:
    all_walk_data.extend(walk2)

if all_walk_data: # データが1つでも存在する場合にのみグラフを生成
    min_val = min(all_walk_data)
    max_val = max(all_walk_data)
    # np.linspaceを使って、データの最小値から最大値までの範囲で均等な間隔のビンを40個作成
    bins = np.linspace(min_val, max_val, 40)

    # System 1 (新しいシステム) のヒストグラムをプロット
    # bins: 上で定義した共通のビンを使用
    # kde=True: カーネル密度推定 (KDE) の曲線も表示
    # alpha=0.6: 棒グラフの透明度を設定し、重なった部分が見えるようにする
    # label: 凡例に表示する名前
    if walk1:
        sns.histplot(walk1, bins=bins, kde=True, color='skyblue', edgecolor='gray', alpha=0.6, label='System 1 (New)')
    
    # System 2 (従来のシステム) のヒストグラムを同じグラフにプロット
    if walk2:
        sns.histplot(walk2, bins=bins, kde=True, color='lightcoral', edgecolor='gray', alpha=0.6, label='System 2 (Old)')

    # グラフのタイトルと軸ラベルを設定
    plt.title('Distribution of Wasted Walking Distance (System 1 vs. System 2)')
    plt.xlabel('Distance (m)')
    plt.ylabel('Number of Humans')

    # 凡例を表示 (labelで指定した名前が表示される)
    plt.legend()

    # Y軸にグリッド線を表示 (透明度0.75)
    plt.grid(axis='y', alpha=0.75)
else: # データが存在しない場合のメッセージ
    plt.text(0.5, 0.5, "No data available for plotting.", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
    plt.title('Distribution of Wasted Walking Distance')
    plt.xlabel('Distance (m)')
    plt.ylabel('Number of Humans')

plt.savefig("histogram2.png")
# レイアウトを自動調整し、要素が重ならないようにする
plt.tight_layout()

# グラフを表示
plt.show()



