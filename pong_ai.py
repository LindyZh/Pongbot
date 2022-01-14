import math,random

prev_ball_pos = [0,0]
prev_paddle_pos = 0
paddle_speed = 1

def pong_ai(paddle_frect, other_paddle_frect, ball_frect, table_size):
    global prev_ball_pos,prev_paddle_pos,paddle_speed
    #get centers and change frame
    ball_center = [ball_frect.pos[0] + ball_frect.size[0]/2,
                  ball_frect.pos[1]]
    paddle_center = [paddle_frect.pos[0] + paddle_frect.size[0]/2,
                     paddle_frect.pos[1] + paddle_frect.size[1]/2\
                     -ball_frect.size[1]/2]
    other_center = [other_paddle_frect.pos[0] + other_paddle_frect.size[0]/2,
                    other_paddle_frect.pos[1] + other_paddle_frect.size[1]/2\
                     -ball_frect.size[1]/2]
    table_height=table_size[1]-ball_frect.size[1]
    #get direction of the ball
    dis = abs(paddle_center[0] - ball_center[0])
    dis_last = abs(paddle_center[0] - prev_ball_pos[0])
    #get ball speed and paddle speed
    ball_speed = [ball_center[0] - prev_ball_pos[0],ball_center[1]-prev_ball_pos[1]]
    prev_ball_pos = [ball_center[0],ball_center[1]]
    if abs(paddle_center[1]-prev_paddle_pos)>0:
        paddle_speed = abs(paddle_center[1]-prev_paddle_pos)
    prev_paddle_pos = paddle_center[1]
    #move to center if ball is moving away    
    if dis >= dis_last:
        if paddle_center[1] < table_height/2:
            return "down"
        else:
            return "up"
    #if ball speed in x direction is 0, return to aviod error
    if ball_speed[0]==0:
        return


    #calculate final y location of the ball
    ball_to_pad = dis-paddle_frect.size[0]/2-ball_frect.size[0]/2
    ending_est = ball_center[1] + ball_speed[1]*abs(ball_to_pad/ball_speed[0])
    in_board = False
    if ending_est > table_height:
        ending_est = ending_est - table_height
    elif ending_est < 0:
        pass
    else:
        in_board = True
    if not in_board:
        num_reflex = abs(ending_est)//(table_height)
        remain_d = abs(ending_est) % (table_height)
        if num_reflex%2 ==1:
            if ball_speed[1]>=0:
                ending_est = remain_d
            else:
                ending_est = table_height - remain_d
        elif num_reflex%2 ==0:
            if ball_speed[1]>=0:
                ending_est = table_height - remain_d
            else:
                ending_est = remain_d
            ball_speed[1]=-ball_speed[1]
    
    #calculate the return speed and direction of the ball
    bounce_speed=[-ball_speed[0],ball_speed[1]]
    bounce_speed_mag=math.sqrt(bounce_speed[0]**2+bounce_speed[1]**2)
    if bounce_speed_mag!=0:
        bounce_speed=[bounce_speed[0]/bounce_speed_mag,
                     bounce_speed[1]/bounce_speed_mag]
        final_pos=[paddle_center[0],ending_est]

        #see if a position is reachable
        def valid(end):
            diff=paddle_frect.size[1]/2-ball_frect.size[1]/2
            return end>=diff and end<=table_height-diff
        #get the position to hit to a target
        def get_ending_est(target,cur_pos,bounce_speed,paddle_size):
            target_vec=[target[0]-cur_pos[0],target[1]-cur_pos[1]]
            target_vec_mag=math.sqrt(target_vec[0]**2+target_vec[1]**2)
            if target_vec_mag!=0:
                target_vec=[target_vec[0]/target_vec_mag,
                            target_vec[1]/target_vec_mag]
                cos_angle=target_vec[0]*bounce_speed[0]+\
                           target_vec[1]*bounce_speed[1]
                angle=math.acos(cos_angle)/math.pi*180
                if angle<=45:
                    dis_from_center=angle/45 *paddle_size/2
                    if target_vec[1]<bounce_speed[1]:
                        return cur_pos[1]+dis_from_center
                    else:
                        return cur_pos[1]-dis_from_center
            return -1

        if abs(other_center[1]-table_height/2)<paddle_speed:
            other_pos='middle'
        elif other_center[1]>table_height/2:
            other_pos='bottom'
        else:
            other_pos='top'

        found=False
        for i in range(5):
            if i%2==0:
                top=[other_center[0],-i*(table_height+ball_frect.size[1])]
                bot=[other_center[0],table_height+i*(table_height+ball_frect.size[1])]
            else:
                top=[other_center[0],table_height+i*(table_height+ball_frect.size[1])]
                bot=[other_center[0],-i*(table_height+ball_frect.size[1])]
            top_end=get_ending_est(top,final_pos,bounce_speed,paddle_frect.size[1])
            bot_end=get_ending_est(bot,final_pos,bounce_speed,paddle_frect.size[1])

            if valid(top_end) and valid(bot_end):
                if other_pos=='middle':
                    if abs(top_end-paddle_center[1])<\
                       abs(bot_end-paddle_center[1]):
                        ending_est=top_end
                    else:
                        ending_est=bot_end
                elif other_pos=='bottom':
                    ending_est=top_end
                else:
                    ending_est=bot_end
                found=True
            elif valid(top_end):
                ending_est=top_end
                found=True
            elif valid(bot_end):
                ending_est=bot_end
                found=True

            if found:
                break
            
        if not found:
            if ending_est>table_height/2:
                ending_est-=paddle_frect.size[1]*0.5
            else:
                ending_est+=paddle_frect.size[1]*0.5
                

    if paddle_center[1] < ending_est:
        return "down"
    else:
        return "up"

    
