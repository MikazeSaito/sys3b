import numpy as np


def make_happy( now_want_speed , i ) :# 使わない可能性あり
    now = now_want_speed[ 0 ][ 0 ] + i
    want = now_want_speed[ 2 ]
    speed = now_want_speed[ 1 ][ 0 ]
    if speed != 0 and ( want - now ) / speed >= 0:
        if speed < 0:
            def happy( x ):
                if x <= now:
                    return np.exp( -( x - now ) ** 2 / ( now - want ) ** 2 )
                else:
                    return max( 0.05 * ( x - now ) / speed + 1 , 0 )
            return happy
        else:
            def happy( x ):
                if x >= now:
                    return np.exp( -( x - now ) ** 2 / ( now - want ) ** 2 )
                else:
                    return max( 0.05 * ( x - now ) / speed+1 , 0 )
            return happy
    else:
        if speed < 0:
            def happy( x ):
                if x < want:
                    return 0
                else:
                    return max( 0.05 * ( x - now ) / speed + 0.05 * ( want - now ) / speed , 0 )
            return happy
        else:
            def happy( x ):
                if x > want:
                    return 0
                else:
                    return max( 0.05 * ( x - now ) / speed + 1 + 0.05 * ( want - now ) / speed ,0 )  
            return happy
        

def make_wait ( now_want_speed ):
    now = now_want_speed[ 0 ][ 0 ]
    speed = now_want_speed[ 1 ][ 0 ]
    def wait( j ):
        return max( ( j - now ) / speed , 0 )
    return wait


def calculate( humans , a , b ):#ここまでの関数はひとセット。使わないかも
    m = -10000000
    locate = 0
    time = -1
    for i in range( 100 , 600 , 5 ):
        func_list=[]
        
        for human in humans:
            if human[ 0 ][ 0 ] > a - 100 and human[ 0 ][ 0 ] < b + 100:
                func_list.append( make_happy( human , i ) )
        for j in range( a , b , 5 ):
            sum = 0
            for func in func_list:
                sum += func( j )
            if m < sum:
                m = sum
                locate = j
                time = i
    return locate , time


def old_car( car , crosses , cars , humans , cross_width , road_y ): #従来の車の動き
    x = car[ 0 ][ 0 ]
    y = car[ 0 ][ 1 ]
    speed = car[ 1 ]
    for cross in crosses:
        if speed > 0:
            if cross[ 0 ][ 0 ] - 20 < x and cross[ 0 ][ 0 ] > x:
                return [ [ x , y ] , speed ]
        else:
            if cross[ 0 ][ 0 ] + cross_width + 20 > x and cross[ 0 ][ 0 ] + cross_width < x:
                return [ [ x , y ] , speed ]
    for car_near in cars:
        if speed > 0:
            if car_near[ 0 ][ 0 ] - 30 < x and car_near[ 0 ][ 0 ]>x and car_near[ 1 ] > 0:
                return [ [ x , y ] , speed ]
        else:
            if car_near[ 0 ][ 0 ] + 30 > x and car_near[ 0 ][ 0 ] < x and car_near[ 1 ] < 0:
                return [ [ x , y ] , speed ]
    for human in humans:
        if speed > 0:
            if human[ 2 ] == 1 and human[ 0 ][ 0 ] - 30 < x and human[ 0 ][ 0 ] > x and ((human[ 1 ][ 1 ] > 0 and human[ 0 ][ 1 ] < road_y) or human[ 1 ][ 1 ] < 0):
                return [ [ x , y ] , speed ]
        else:
            if human[ 2 ] == 1 and human[ 0 ][ 0 ] + 30 > x and human[ 0 ][ 0 ] < x and ((human[ 1 ][ 1 ] < 0 and human[ 0 ][ 1 ] > road_y) or human[ 1 ][ 1 ] > 0):
                return [ [ x , y ] , speed ]
    x += speed
    return [ [ x , y ] , speed ]


def new_car( car , crosses , cars ,human1below ,human1above, cross_width , road_y): #未来の車の動き
    x = car[ 0 ][ 0 ]
    y = car[ 0 ][ 1 ]
    speed = car[ 1 ]
    humans=human1below +human1above
    for cross in crosses:
        if speed > 0:
            if cross[ 1 ] < 1 and cross[ 2 ] > 0 and cross[ 0 ][ 0 ] - 20 < x and cross[ 0 ][ 0 ] > x:
                return [ [ x , y ] , speed ] 
        else:
            if cross[ 1 ] < 1 and cross[ 2 ] > 0  and cross[ 0 ][ 0 ] + cross_width + 20 > x and cross[ 0 ][ 0 ] + cross_width < x:
                return [ [ x , y ] , speed ]
    for car_near in cars:
        if speed > 0:
            if car_near[ 0 ][ 0 ] - 30 < x and car_near[ 0 ][ 0 ] > x and car_near[ 1 ] >= 0:
                return [ [ x , y ] , speed ]
        else:
            if car_near[ 0 ][ 0 ] + 30 > x and car_near[ 0 ][ 0 ] < x and car_near[ 1 ] < 0:
                return [ [ x , y ] , speed ]
    for human in humans:
        if speed > 0:
            if human[ 2 ] == 1 and human[ 0 ][ 0 ] - 30 < x and human[ 0 ][ 0 ] > x and ((human[ 1 ][ 1 ] >= 0 and human[ 0 ][ 1 ] < road_y) or human[ 1 ][ 1 ] <= 0):
                return [ [ x , y ] , speed ]
        else:
            if human[ 2 ] == 1 and human[ 0 ][ 0 ] + 30 > x and human[ 0 ][ 0 ] < x and ((human[ 1 ][ 1 ] <= 0 and human[ 0 ][ 1 ] > road_y) or human[ 1 ][ 1 ] >= 0):
                return [ [ x , y ] , speed ]
    x += speed
    return [ [ x , y ] , speed ]


def new_system( humans , a , b ): #使わないかも
    sum = 0
    count = 0
    for human in humans:
        if human[ 0 ][ 0 ] > a and human[ 0 ][ 0 ] < b:
            sum += human[ 0 ][ 0 ]
            count += 1
    if count == 0:
        return [0,0]
    else:
        return [ sum / count , 195 ]
    

def old_human( human , crosses , cross_width , human2_1_y ,human2_2_y): #従来の人の動き
    x = human[ 0 ][ 0 ]
    y = human[ 0 ][ 1 ]
    x_speed = human[ 1 ][ 0 ]
    y_speed = human[ 1 ][ 1 ]
    statas = human[ 2 ]
    want = human[ 3 ]
    wait = human[ 4 ]
    if statas == 0:
        for cross in crosses:
            if cross[ 0 ][ 0 ] < x and x < cross[ 0 ][ 0 ] + cross_width and cross[ 1 ] < 1:
                if cross_width / (abs( x_speed ) * 4) < cross[ 2 ] and cross_width / (abs( x_speed ) * 2) > cross[ 2 ]:
                    statas = 1
                    if y == human2_1_y:
                        y_speed = 2 * abs( x_speed )
                        x_speed = 0
                    else:
                        y_speed = -2 * abs( x_speed )
                        x_speed = 0
                    break
                if cross_width / (abs( x_speed ) * 2) < cross[ 2 ]:
                    statas = 1
                    if y == human2_1_y:
                        y_speed = abs( x_speed )
                        x_speed = 0
                    else:
                        y_speed = -abs( x_speed )
                        x_speed = 0
                    break    
    else:
        if y_speed > 0 and y > human2_2_y:
            statas = 2
        elif y_speed < 0 and y < human2_1_y:
            statas = 2
    x += x_speed
    y += y_speed
    return [ [ x , y ] , [ x_speed , y_speed ] , statas , want ,wait]


def old_human2( human , crosses , cross_width , human2_1_y ,human2_2_y ):
    x = human[ 0 ][ 0 ]
    y = human[ 0 ][ 1 ]
    x_speed = human[ 1 ][ 0 ]
    y_speed = human[ 1 ][ 1 ]
    statas = human[ 2 ]
    want=human[3]
    want_cross = human[ 4 ]
    wait= human[ 5 ]
    if statas == 0:
        for cross in crosses:
            if cross[ 0 ][ 0 ] < x and x < cross[ 0 ][ 0 ] + cross_width and cross[ 1 ] < 1:
                if cross_width / (abs( x_speed ) * 4) < cross[ 2 ] and cross_width / (abs( x_speed ) * 2) > cross[ 2 ]:
                    statas = 1
                    if y == human2_1_y:
                        y_speed = 2 * abs( x_speed )
                        x_speed = 0
                    else:
                        y_speed = -2 * abs( x_speed )
                        x_speed = 0
                    break
                if cross_width / (abs( x_speed ) * 2) < cross[ 2 ]:
                    statas = 1
                    if y == human2_1_y:
                        y_speed = abs( x_speed )
                        x_speed = 0
                    else:
                        y_speed = -abs( x_speed )
                        x_speed = 0
                    break    
        if  len(crosses) == 0 and x - 5 < want_cross < x + 5:
            return [ [ x , y ] , [ x_speed , y_speed ] , statas , want ,want_cross,wait]
    else:
        if y_speed > 0 and y > human2_2_y:
            statas = 2
        elif y_speed < 0 and y < human2_1_y:
            statas = 2
    x += x_speed
    y += y_speed
    return [ [ x , y ] , [ x_speed , y_speed ] , statas , want ,want_cross,wait]


def new_human( human , crosses , cross_width , human1_1_y , human1_2_y ): #未来の人の動き
    x = human[ 0 ][ 0 ]
    y = human[ 0 ][ 1 ]
    x_speed = human[ 1 ][ 0 ]
    y_speed = human[ 1 ][ 1 ]
    statas = human[ 2 ]
    want = human[ 3 ]
    wait=human[4]
    color=human[5]
    if statas == 0:

        for cross in crosses:
            if cross[ 1 ] > 0 and cross[ 0 ][ 0 ] < x and x < cross[ 0 ][ 0 ] + cross_width :
                return [ [ x , y ] , [ x_speed , y_speed ] , statas , want ,wait,color]
            if cross[ 1 ] < 1 and cross[ 2 ] > 0 and cross[ 0 ][ 0 ] < x and x < cross[ 0 ][ 0 ] + cross_width:
                if cross_width / (abs( x_speed ) * 4) < cross[ 2 ] and cross_width / (abs( x_speed ) * 2) > cross[ 2 ]:
                    statas = 1
                    if y == human1_1_y:
                        y_speed = 2 * abs( x_speed )
                        x_speed = 0
                    else:
                        y_speed = -2 * abs( x_speed )
                        x_speed = 0
                    break
                if cross_width / (abs( x_speed ) * 2) < cross[ 2 ]:
                    statas = 1
                    if y == human1_1_y:
                        y_speed = abs( x_speed )
                        x_speed = 0
                    else:
                        y_speed = -abs( x_speed )
                        x_speed = 0
                    break    
    else:
        if y_speed > 0 and y > human1_2_y:
            statas = 2
        elif y_speed < 0 and y < human1_1_y:
            statas= 2
    x += x_speed
    y += y_speed
    return [ [ x , y ] , [ x_speed , y_speed ] , statas , want ,wait,color]

def make_human_waiting_time( human , road_width,cross_width): #人の待ち時間計算
    def human_waiting_time( locate , start_time , end_time ):
        x = human[ 0 ][ 0 ]
        want =human[3]
        
        x_speed = human[ 1 ][ 0 ]
        w=np.exp(0.003*(-abs(x_speed)*(want-x)/x_speed))
        if ( locate - x ) / x_speed < 0:
            return (3000-(want-x)/x_speed)*w*2
        elif x_speed > 0 and locate < start_time * x_speed + x:
            return (start_time - ( locate - x ) / x_speed-min((want-locate-cross_width)/x_speed,0)*2)*w
        elif x_speed > 0 and locate > start_time * x_speed + x and locate + road_width / 2 < end_time * x_speed + x:
            return -min((want-locate)/x_speed,0)*2*w
        elif x_speed > 0 and locate + road_width / 2 >= end_time * x_speed + x:
            return (3000-(want-x)/x_speed)*w*2
        elif locate+cross_width > start_time * x_speed + x:
            return (start_time - ( locate - x ) / x_speed-min((want-locate-cross_width)/x_speed,0)*2)*w
        elif locate+cross_width < start_time * x_speed + x and locate - road_width / 2> end_time * x_speed + x:
            return -min((want-locate-cross_width)/x_speed,0)*2*w
        else:
            return (3000-(want-x)/x_speed)*w*2
    return human_waiting_time

def make_car_waiting_time( car , cross_width ): #車の待ち時間計算
    def car_waiting_time( locate , start_time , end_time ):
        x = car[ 0 ][ 0 ]
        x_speed=car[ 1 ]
        if x_speed > 0 and x + x_speed * start_time < locate + cross_width and locate < x + x_speed * end_time:
            return end_time - ( locate - x ) / x_speed
        elif x_speed < 0 and x + x_speed * start_time > locate and locate + cross_width > x + x_speed * end_time:
            return end_time - ( locate - x ) / x_speed
        else:
            return 0

    return car_waiting_time

def make_human_waiting_time2( human , road_width,cross_width,a,b):
    func=make_human_waiting_time(human,road_width,cross_width)
    def human_waiting_time2( locate , start_time , end_time ):
        return func(locate , start_time , end_time)-func(human[0][0],a,b)
    return human_waiting_time2
    
def multipurpose(humans1above,humans1below , cars , a , b ,cross_width , road_width,virtual_time):
    func_list=[]
    car_func=[]
    humans=humans1above+humans1below
    for human in humans:
        if a - virtual_time*human[1][0]-30 < human[ 0 ][ 0 ] < b - virtual_time*human[1][0]+ 30:
            func_list.append( make_human_waiting_time2( human , road_width,cross_width,200,1500) )
    for car in cars:
        car_func.append( make_car_waiting_time( car , cross_width) )
    min1=10000000000000
    min2=10000000000000
    min_locate = 0
    min_start_time = 0
    min_end_time = 0
    for start_time in range( 200 , 1000 , 30):
        for end_time in range( start_time+200 , 1500, 30 ):

            for locate in range( a-40 , b+40 , 10 ):
                human_value=[func(locate,start_time,end_time) for func in func_list]
                car_value=[func(locate,start_time,end_time) for func in car_func]
                sum1 = 0
                sum2=0
                for i in human_value:
                    sum1+=i**2
                if sum1<min1:
                    min1=sum1
                    for i in human_value:
                        sum2+=i
                    for i in car_value:
                        sum2+=i
                    if sum2<min2:
                        min2=sum2
                        min_locate = locate
                        min_start_time = start_time
                        min_end_time = end_time
    return min_locate , min_start_time , min_end_time


def calculate2( humans1above,humans1below , cars , a , b ,cross_width , road_width,virtual_time): #横断歩道の最適化
    func_list=[]
    humans=humans1above+humans1below
    for human in humans:
        if a - virtual_time*human[1][0]-30 < human[ 0 ][ 0 ] < b - virtual_time*human[1][0]+ 30:
            func_list.append( make_human_waiting_time( human , road_width,cross_width) )
    for car in cars:
        func_list.append( make_car_waiting_time( car , cross_width) )
    min = 10000000
    min_locate = 0
    min_start_time = 0
    min_end_time = 0


    for start_time in range( 200 , 1000 , 30):
        for end_time in range( start_time+200 , 1500, 30 ):

            for locate in range( a-40 , b+40 , 10 ):

                sum = 0
                for func in func_list:
                    sum += func( locate , start_time , end_time )
                if min > sum:
                    min = sum
                    min_locate = locate
                    min_start_time = start_time
                    min_end_time = end_time
    return min_locate , min_start_time , min_end_time

def group_numbers_by_threshold(numbers, threshold):

    groups = []
    current_group = [numbers[0]]

    for i in range(1, len(numbers)):
        if numbers[i] - current_group[-1] <= threshold:
            # 現在の数字とグループの最後の数字の差が閾値以内なら、同じグループに追加
            current_group.append(numbers[i])
        else:
            # 閾値を超えたら新しいグループを開始
            groups.append(current_group)
            current_group = [numbers[i]]
    
    # 最後のグループを追加
    groups.append(current_group)
    
    return groups

def group_numbers_greedy_min_groups(numbers, max_group_width):


    groups = []
    current_group_start_value = numbers[0]
    current_group = [numbers[0]]

    for i in range(1, len(numbers)):
        # 現在の要素が、現在のグループの開始値からmax_group_widthの範囲内にあるか
        if numbers[i] - current_group_start_value <= max_group_width:
            current_group.append(numbers[i])
        else:
            # 範囲を超えたら新しいグループを開始
            groups.append(current_group)
            current_group_start_value = numbers[i]
            current_group = [numbers[i]]
    
    # 最後のグループを追加
    groups.append(current_group)
    
    return groups
def calculate3(humans1below , humans1above ):
    _range=[]
    li=[]
    new_below = [x[0][0] for x in humans1below]
    new_below.sort()
    new_above = [x[0][0] for x in humans1above]
    new_above.sort()
    below_group = group_numbers_by_threshold(new_below, 30)
    above_group = group_numbers_by_threshold(new_above, 30)
    print(below_group)
    print(above_group)
    for L in below_group:
        _range.append((min(L)+max(L))/2-75)
    for L in above_group:
        _range.append((min(L)+max(L))/2+75)
    _range.sort()
    group = group_numbers_greedy_min_groups( _range , 150)
    for L in group:
        li.append(sum(L)/len(L))
    print(li)
    return li

def calculate3(humans1below , humans1above ):
    _range=[]
    li=[]
    new_below = [x[0][0] for x in humans1below]
    new_below.sort()
    new_above = [x[0][0] for x in humans1above]
    new_above.sort()
    below_group = group_numbers_by_threshold(new_below, 30)
    above_group = group_numbers_by_threshold(new_above, 30)
    print(below_group)
    print(above_group)
    for L in below_group:
        _range.append((min(L)+max(L))/2-75)
    for L in above_group:
        _range.append((min(L)+max(L))/2+75)
    _range.sort()
    group = group_numbers_greedy_min_groups( _range , 150)
    for L in group:
        li.append(sum(L)/len(L))
    print(li)
    return li
    
    
def calculate4(humans1below , humans1above ,virtual_time):
    li=[]
    new_below = [x[0][0]+virtual_time*x[1][0] for x in humans1below]
    new_above = [x[0][0]+virtual_time*x[1][0] for x in humans1above]
    future_human_list=new_above+new_below
    future_human_list.sort()
    group = group_numbers_greedy_min_groups( future_human_list , 300)
    for L in group:
        li.append([min(L),max(L)])
    return li

def to_be_able_to_cross(x,speed,vec,crosses,road_width):
    
    for cross in crosses:
        if 0<(cross[0][0]-x)/(speed*vec)+road_width/(4*speed)<cross[2]:
            return vec
    for cross in crosses:
        if 0<(cross[0][0]-x)/(-speed*vec)+road_width/(4*speed)<cross[2]:
            return -vec  
    return vec    
    