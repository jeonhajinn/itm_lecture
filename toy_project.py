import turtle
import random

# 1. 화면 설정
screen = turtle.Screen()
screen.title("거북이를 지켜라!")
screen.bgcolor("#E0E0E0") 
screen.setup(width=600, height=600)
screen.tracer(0)

# 2. 플레이어 (나)
player = turtle.Turtle()
player.shape("turtle")
player.color("green") 
player.penup()
player.goto(0, -250)
player.setheading(90)
player.hideturtle() 

# 이동 속도 변수
player.dx = 0 
player_speed = 0.4 

# 3. 떨어지는 과제(적)
bomb = turtle.Turtle()
bomb.shape("circle")
bomb.color("black", "#B0E0E6") 
bomb.penup()
bomb.goto(0, 260)
bomb.hideturtle() 

# 4. 점수 및 메시지 펜
pen = turtle.Turtle()
pen.speed(0)
pen.color("#333333")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

# 5. START 버튼 만들기
# (주의: 버튼 객체는 그림만 그리고 숨깁니다. 클릭은 좌표로 계산합니다.)
start_button = turtle.Turtle()
start_button.speed(0)
start_button.shape("square")
start_button.color("black", "white") # 테두리 검정, 내부 흰색
start_button.shapesize(stretch_wid=2.5, stretch_len=6)
start_button.penup()
start_button.goto(0, 0)
# ★ 중요: 박스를 도장처럼 찍고(stamp), 거북이는 숨김 (글씨를 가리지 않게)
start_button.stamp() 
start_button.hideturtle()

# 버튼 위에 글씨 쓰기
button_pen = turtle.Turtle()
button_pen.speed(0)
button_pen.color("black") 
button_pen.penup()
button_pen.hideturtle()
button_pen.goto(0, -12) # 위치 미세 조정
# ★ 폰트: Arial, 크기 20, 굵게(bold) - 아주 잘 보임
button_pen.write("START !", align="center", font=("Arial", 20, "bold"))

# 게임 변수
bomb_speed = 0.1 
score = 0
game_state = "ready" 

# --- 함수 정의 ---

def start_game(x, y):
    """화면을 클릭했을 때 실행되는 함수"""
    global game_state
    
    # ready 상태이고, 클릭한 위치(x,y)가 버튼 근처일 때만 실행
    if game_state == "ready":
        if -70 < x < 70 and -30 < y < 30: # 버튼 좌표 범위 체크
            game_state = "playing"
            
            # 버튼 그림(스탬프) 지우기 & 글씨 지우기
            start_button.clear() 
            button_pen.clear()
            
            # 게임 요소 보이기
            player.showturtle()
            bomb.showturtle()
            
            # 점수판 표시
            pen.clear()
            pen.write(f"점수: {score}", align="center", font=("Courier", 24, "bold"))

def start_left():
    if game_state == "playing":
        player.dx = -player_speed
        player.setheading(180)

def start_right():
    if game_state == "playing":
        player.dx = player_speed
        player.setheading(0)

def stop_move():
    player.dx = 0

def reset_game():
    global score, bomb_speed, game_state
    
    if game_state == "gameover":
        score = 0
        bomb_speed = 0.1
        game_state = "playing"
        
        player.goto(0, -250)
        player.dx = 0 
        bomb.goto(0, 260)
        
        pen.clear()
        pen.goto(0, 260)
        pen.write(f"점수: {score}", align="center", font=("Courier", 24, "bold"))

# 키보드 연결
screen.listen()
screen.onkeypress(start_left, "Left")
screen.onkeypress(start_right, "Right")
screen.onkeyrelease(stop_move, "Left")
screen.onkeyrelease(stop_move, "Right")
screen.onkeypress(reset_game, "r")
screen.onkeypress(reset_game, "R")

# ★ 화면 전체 클릭 감지 -> start_game 함수에서 좌표 확인
screen.onclick(start_game)

# 6. 메인 게임 루프
while True:
    screen.update()
    
    if game_state == "playing":
        # 플레이어 이동
        player.setx(player.xcor() + player.dx)
        
        # 벽 막힘 처리
        if player.xcor() < -280:
            player.setx(-280)
        elif player.xcor() > 280:
            player.setx(280)
            
        # 적 이동
        y = bomb.ycor()
        y -= bomb_speed
        bomb.sety(y)
        
        # 점수 획득
        if y < -300:
            bomb.goto(random.randint(-280, 280), 280)
            score += 10
            bomb_speed += 0.01
            pen.clear()
            pen.write(f"점수: {score}", align="center", font=("Courier", 24, "bold"))

        # 충돌 (게임 오버)
        if player.distance(bomb) < 25:
            game_state = "gameover"
            pen.goto(0, 0)
            pen.write(f"GAME OVER\n최종 점수: {score}\n[R]키로 재시작", align="center", font=("Courier", 24, "bold"))
            
    else:
        pass

