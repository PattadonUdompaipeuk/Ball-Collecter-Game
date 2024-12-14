import ball
import turtle
import random
import paddle
import time
import emoji


class BallCollectorGame:
    def __init__(self):
        self.time_limit = 0
        self.start_time = time.time()
        self.ball_list = []
        self.score = 0
        self.target_score = 0
        self.ball_speed_multiplier = 0
        self.spawn_time = 0
        self.ball_speed = 0
        self.is_running = False
        self.spawn_rate = [0, 0, 0, 0]
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        turtle.bgcolor('black')
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1] * 1.5

        tom = turtle.Turtle()
        self.my_paddle = paddle.Paddle(140, 20, "yellow", tom)
        self.my_paddle.set_location([0, -self.canvas_height + 40])

        self.screen = turtle.Screen()
        self.left_key_pressed = False
        self.right_key_pressed = False

    def draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color("white")
        for i in range(2):
            turtle.forward(2 * self.canvas_width)
            turtle.left(90)
            turtle.forward(2 * self.canvas_height)
            turtle.left(90)

    def redraw(self):
        turtle.clear()
        self.my_paddle.clear()
        self.draw_border()
        self.my_paddle.draw()
        for i in range(len(self.ball_list)):
            self.ball_list[i].draw()
        self.draw_scores()
        turtle.update()

    def move_left(self):
        if (self.my_paddle.location[0] - self.my_paddle.width / 2 - 40) >= -self.canvas_width:
            self.my_paddle.set_location([self.my_paddle.location[0] - 20, self.my_paddle.location[1]])

    def move_right(self):
        if (self.my_paddle.location[0] + self.my_paddle.width / 2 + 40) <= self.canvas_width:
            self.my_paddle.set_location([self.my_paddle.location[0] + 20, self.my_paddle.location[1]])

    def move_continuous(self):
        if self.is_running:
            if self.left_key_pressed:
                self.move_left()
            if self.right_key_pressed:
                self.move_right()
            self.screen.ontimer(self.move_continuous, 20)

    def start_move_left(self):
        self.left_key_pressed = True

    def start_move_right(self):
        self.right_key_pressed = True

    def stop_move_left(self):
        self.left_key_pressed = False

    def stop_move_right(self):
        self.right_key_pressed = False

    def spawn_balls(self):
        ball_radius = 0.05 * self.canvas_width
        x = random.uniform(-self.canvas_width + ball_radius, self.canvas_width - ball_radius)
        y = self.canvas_height - ball_radius
        vx = (random.randint(-self.ball_speed, self.ball_speed)
              * random.uniform(-self.ball_speed_multiplier, self.ball_speed_multiplier))
        vy = -self.ball_speed * 0.5

        ball_type = ["red", "green", "blue", "gold"]
        probability = self.spawn_rate
        ball_color = random.choices(ball_type, probability)[0]
        self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color))

    def catch_ball(self, balls):
        if (self.my_paddle.location[1] - self.my_paddle.height / 2 <= balls.y-balls.size <= self.my_paddle.location[1] +
                self.my_paddle.height / 2 and self.my_paddle.location[0] - self.my_paddle.width / 2 <= balls.x <=
                self.my_paddle.location[0] + self.my_paddle.width / 2):
            return True
        return False

    def draw_scores(self):
        turtle.penup()
        turtle.goto(-self.canvas_width + 20, self.canvas_height - 40)
        turtle.color("white")
        turtle.write(f"Score: {self.score} / {self.target_score}", align="left", font=("Arial", 16, "normal"))

        remaining_time = max(0, int(self.time_limit - (time.time() - self.start_time)))
        turtle.goto(self.canvas_width - 20, self.canvas_height - 40)
        turtle.write(f"Time: {remaining_time}s", align="right", font=("Arial", 16, "normal"))

    def check_winner(self):
        if self.score >= self.target_score:
            self.show_end_game("You Win!")
            return True
        elif time.time() - self.start_time >= self.time_limit:
            self.show_end_game("You Lose!")
            return True
        return False

    def show_end_game(self, msg):
        self.my_paddle.clear()
        turtle.clear()
        self.draw_border()
        turtle.penup()
        turtle.goto(0, 50)
        turtle.color("white")
        if msg == "You Lose!":
            turtle.write(emoji.emojize(f":crying_face: {msg} :crying_face:"), align="center",
                         font=("Arial", 24, "bold"))
        elif msg == "You Win!":
            turtle.write(emoji.emojize(f":smiling_face_with_sunglasses: {msg} :smiling_face_with_sunglasses:"),
                         align="center", font=("Arial", 24, "bold"))
        turtle.goto(0, 0)
        turtle.write(f"Your Score: {self.score}", align="center", font=("Arial", 18, "normal"))
        turtle.goto(0, -50)
        turtle.write("Press 'R' to Restart or Close to Exit", align="center", font=("Arial", 16, "italic"))
        turtle.update()
        self.is_running = False

    def restart_game(self):
        self.is_running = False
        self.left_key_pressed = False
        self.right_key_pressed = False
        self.score = 0
        self.ball_list.clear()
        self.start_time = time.time()
        self.my_paddle.set_location([0, -self.canvas_height + 40])
        turtle.clear()
        self.show_select_difficulty()

    def show_select_difficulty(self):
        turtle.clear()
        self.draw_border()
        turtle.bgcolor("black")
        turtle.penup()
        turtle.goto(0, self.canvas_height - 100)
        turtle.color("cyan")
        turtle.write("Ball Collector Game", align="center", font=("Arial", 32, "bold"))
        turtle.goto(0, self.canvas_height - 130)
        turtle.color("white")
        turtle.write(emoji.emojize(":oncoming_fist: Hit the target score and get win :oncoming_fist:"),
                     align="center", font=("Arial", 14, "normal"))
        turtle.goto(0, 120)
        turtle.color("white")
        turtle.write("Please select level", align="center", font=("Arial", 22, "italic"))
        turtle.goto(0, 60)
        turtle.color("green")
        turtle.write("Easy [Press 1]", align="center", font=("Arial", 16, "normal"))
        turtle.goto(0, 0)
        turtle.color("orange")
        turtle.write("Medium [Press 2]", align="center", font=("Arial", 16, "normal"))
        turtle.goto(0, -60)
        turtle.color("red")
        turtle.write("Hard [Press 3]", align="center", font=("Arial", 16, "normal"))
        turtle.goto(0, -self.canvas_height + 60)
        turtle.color("white")
        turtle.write("Use Arrow Keys to Move Paddle", align="center", font=("Arial", 12, "normal"))
        turtle.update()

        self.screen.onkey(self.easy_mode, "1")
        self.screen.onkey(self.medium_mode, "2")
        self.screen.onkey(self.hard_mode, "3")
        self.screen.listen()

    def easy_mode(self):
        self.is_running = True
        self.start_time = time.time()
        self.ball_speed = 25
        self.target_score = 10
        self.time_limit = 60
        self.spawn_time = 1
        self.ball_speed_multiplier = 1.2
        self.spawn_rate = [0.2, 0.8, 0.025, 0.001]
        print("Easy Mode Selected")
        self.run()

    def medium_mode(self):
        self.is_running = True
        self.start_time = time.time()
        self.ball_speed = 30
        self.target_score = 15
        self.time_limit = 50
        self.spawn_time = 0.9
        self.ball_speed_multiplier = 1.25
        self.spawn_rate = [0.3, 0.7, 0.030, 0.010]
        print("Medium Mode Selected")
        self.run()

    def hard_mode(self):
        self.is_running = True
        self.start_time = time.time()
        self.ball_speed = 35
        self.target_score = 20
        self.time_limit = 40
        self.spawn_time = 0.8
        self.ball_speed_multiplier = 1.5
        self.spawn_rate = [0.4, 0.6, 0.040, 0.020]
        print("Hard Mode Selected")
        self.run()

    def run(self):
        last_spawn_time = time.time()
        self.screen.listen()
        self.screen.onkeypress(self.start_move_left, "Left")
        self.screen.onkeypress(self.start_move_right, "Right")
        self.screen.onkeyrelease(self.stop_move_left, "Left")
        self.screen.onkeyrelease(self.stop_move_right, "Right")
        self.move_continuous()

        while self.is_running:
            current_time = time.time()
            if current_time - last_spawn_time >= self.spawn_time:
                self.spawn_balls()
                last_spawn_time = current_time

            self.redraw()

            for i in range(len(self.ball_list)):  # Check ball collision
                for j in range(i + 1, len(self.ball_list)):
                    ball1 = self.ball_list[i]
                    ball2 = self.ball_list[j]
                    if ball1.distance(ball2) <= ball1.size + ball2.size:
                        ball1.bounce_off(ball2)

            for balls in self.ball_list:
                balls.move(0.05)
                if balls.y - balls.size < -self.canvas_height + 10 and balls.color != "red":
                    self.ball_list.remove(balls)
                elif self.catch_ball(balls) and balls.color == "green":
                    self.score += 1
                    self.ball_list.remove(balls)
                elif self.catch_ball(balls) and balls.color == "red":
                    self.score -= 1
                    self.ball_list.remove(balls)
                elif self.catch_ball(balls) and balls.color == "blue":
                    self.time_limit += 3
                    self.ball_list.remove(balls)
                elif self.catch_ball(balls) and balls.color == "gold":
                    self.score += 3
                    self.ball_list.remove(balls)
                else:
                    balls.bounce_off_wall()

            if self.check_winner():
                break
        turtle.done()


my_game = BallCollectorGame()
my_game.show_select_difficulty()
my_game.screen.onkey(my_game.restart_game, "r")
my_game.screen.listen()
turtle.done()
