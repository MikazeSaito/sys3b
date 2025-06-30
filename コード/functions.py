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


def old_car( car , crosses , cars , humans , cross_width): #従来の車の動き
    x = car[ 0 ][ 0 ]
    y = car[ 0 ][ 1 ]
    speed = car[ 1 ]
    for cross in crosses:
        if speed > 0:
            if cross[ 0 ] - 20 < x and cross[ 0 ] > x:
                return [ [ x , y ] , speed ]
        else:
            if cross[ 0 ] + cross_width + 20 > x and cross[ 0 ] + cross_width < x:
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
            if human[ 2 ] == 1 and human[ 0 ][ 0 ] - 30 < x and human[ 0 ][ 0 ] > x:
                return [ [ x , y ] , speed ]
        else:
            if human[ 2 ] == 1 and human[ 0 ][ 0 ] + 30 > x and human[ 0 ][ 0 ] < x:
                return [ [ x , y ] , speed ]
    x += speed
    return [ [ x , y ] , speed ]


def new_car( car , crosses , cars , humans , cross_width): #未来の車の動き
    x = car[ 0 ][ 0 ]
    y = car[ 0 ][ 1 ]
    speed = car[ 1 ]
    for cross in crosses:
        if speed > 0:
            if cross[ 1 ] < 1 and cross[ 2 ] > 0 and cross[ 0 ][ 0 ] - 20 < x and cross[ 0 ][ 0 ] > x:
                return [ [ x , y ] , speed ] 
        else:
            if cross[ 1 ] < 1 and cross[ 2 ] > 0  and cross[ 0 ][ 0 ] + cross_width + 20 > x and cross[ 0 ][ 0 ] + cross_width < x:
                return [ [ x , y ] , speed ]
    for car_near in cars:
        if speed > 0:
            if car_near[ 0 ][ 0 ] - 30 < x and car_near[ 0 ][ 0 ] > x and car_near[ 1 ] > 0:
                return [ [ x , y ] , speed ]
        else:
            if car_near[ 0 ][ 0 ] + 30 > x and car_near[ 0 ][ 0 ] < x and car_near[ 1 ] < 0:
                return [ [ x , y ] , speed ]
    for human in humans:
        if speed > 0:
            if human[ 2 ] == 1 and human[ 0 ][ 0 ] - 30 < x and human[ 0 ][ 0 ] > x:
                return [ [ x , y ] , speed ]
        else:
            if human[ 2 ] == 1 and human[ 0 ][ 0 ] + 30 > x and human[ 0 ][ 0 ] < x:
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
    

def old_human( human , cross , cross_width , human2_1_y ,human2_2_y): #従来の人の動き
    x = human[ 0 ][ 0 ]
    y = human[ 0 ][ 1 ]
    x_speed = human[ 1 ][ 0 ]
    y_speed = human[ 1 ][ 1 ]
    statas = human[ 2 ]
    want = human[ 3 ]
    if statas == 0:
        for cross in cross:
            if cross[ 0 ] < x and x < cross[ 0 ] + cross_width:
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
    return [ [ x , y ] , [ x_speed , y_speed ] , statas , want ]


def new_human( human , cross , cross_width , human1_1_y , human1_2_y ): #未来の人の動き
    x = human[ 0 ][ 0 ]
    y = human[ 0 ][ 1 ]
    x_speed = human[ 1 ][ 0 ]
    y_speed = human[ 1 ][ 1 ]
    statas = human[ 2 ]
    want = human[ 3 ]
    if statas == 0:

        for cross in cross:
            if cross[ 1 ] > 0 and cross[ 0 ][ 0 ] < x and x < cross[ 0 ][ 0 ] + cross_width :
                return [ [ x , y ] , [ x_speed , y_speed ] , statas , want ]
            if cross[ 1 ] < 1 and cross[ 2 ] > 0 and cross[ 0 ][ 0 ] < x and x < cross[ 0 ][ 0 ] + cross_width:
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
    return [ [ x , y ] , [ x_speed , y_speed ] , statas , want ]

def make_human_waiting_time( human ): #人の待ち時間計算
    def human_waiting_time( locate , start_time , end_time ):
        x = human[ 0 ][ 0 ]
        x_speed = human[ 1 ][ 0 ]
        if ( locate - x ) / x_speed < 0:
            return 1500
        elif x_speed > 0 and locate < start_time * x_speed + x:
            return start_time - ( locate - x ) / x_speed
        elif x_speed > 0 and locate > start_time * x_speed + x and locate < end_time * x_speed + x:
            return 0
        elif x_speed > 0 and locate >= end_time * x_speed + x:
            return 1500
        elif locate > start_time * x_speed + x:
            return start_time - ( locate - x ) / x_speed
        elif locate < start_time * x_speed + x and locate > end_time * x_speed + x:
            return 0
        else:
            return 1500
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


def calculate2( humans , cars , a , b ,cross_width ): #横断歩道の最適化
    func_list=[]
    for human in humans:
        if a - 30 < human[ 0 ][ 0 ] < b + 30:
            func_list.append( make_human_waiting_time( human ) )
    for car in cars:
        func_list.append( make_car_waiting_time( car , cross_width) )
    min = 10000000
    min_locate = 0
    min_start_time = 0
    min_end_time = 0
    for locate in range( a , b , 10 ):
        for start_time in range( 100 , 1000 , 10):
            for end_time in range( start_time , 1500, 10 ):
                sum = 0
                for func in func_list:
                    sum += func( locate , start_time , end_time )
                if min > sum:
                    min = sum
                    min_locate = locate
                    min_start_time = start_time
                    min_end_time = end_time
    return min_locate , min_start_time , min_end_time