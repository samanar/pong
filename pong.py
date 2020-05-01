import turtle


class Window:
    title = "PONG"

    def __init__(self, width, height):
        self.win = turtle.Screen()
        self.win.title(self.title)
        self.win.bgcolor("black")
        self.width = width
        self.height = height
        self.win.setup(width, height)
        self.win.tracer(0)
        self.win.listen()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class Paddle:
    step = 20
    stretch_len = 0.7
    dimension = 10
    stretch_wid = 5

    def __init__(self, initial_position):
        self.paddle = turtle.Turtle()
        self.paddle.speed(0)
        self.paddle.color('white')
        self.paddle.shape('square')
        self.paddle.penup()
        self.paddle.shapesize(stretch_wid=self.stretch_wid, stretch_len=self.stretch_len)
        self.paddle.goto(initial_position, 0)
        self.initial_position = initial_position

    def move_up(self):
        y = self.paddle.ycor() + self.step
        self.paddle.sety(y)

    def move_down(self):
        self.paddle.sety(self.paddle.ycor() - self.step)

    def get_borders(self):
        side_margin = self.dimension * self.stretch_len
        height_margin = self.dimension * self.stretch_wid
        side = self.initial_position + side_margin if self.initial_position < 0 else self.initial_position - side_margin
        top = self.paddle.ycor() + height_margin
        bottom = self.paddle.ycor() - height_margin
        return top, side, bottom


class Ball:
    dimension = 20
    dx = 0.035
    dy = 0.035

    def __init__(self, window_width, window_height):
        self.window_height = window_height
        self.window_width = window_width
        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.color('white')
        self.ball.shape('circle')
        self.ball.penup()
        self.ball.goto(0, 0)

    def get_dimension(self):
        return self.dimension

    def reverse_dx(self):
        self.dx *= -1

    def goto(self, x, y):
        self.ball.goto(x, y)

    def xcor(self):
        return self.ball.xcor()

    def ycor(self):
        return self.ball.ycor()

    def setx(self, x):
        self.ball.setx(x)

    def sety(self, y):
        self.ball.sety(y)

    def reset_reverse_position(self):
        self.ball.goto(0, 0)
        self.reverse_dx()

    def __reflect_if_out(self):
        top_border = (self.window_height / 2) - (self.dimension / 2)
        bottom_border = top_border * -1

        if self.ball.ycor() > top_border:
            self.ball.sety(top_border)
            self.dy *= -1

        elif self.ball.ycor() < bottom_border:
            self.ball.sety(bottom_border)
            self.dy *= -1

    def move(self):
        self.ball.sety(self.ball.ycor() + self.dy)
        self.ball.setx(self.ball.xcor() + self.dx)
        self.__reflect_if_out()


class Game:
    WIDTH = 800
    HEIGHT = 600
    PADDLE_MARGIN = 50
    PADDLE_A_POSITION = -(WIDTH / 2) + PADDLE_MARGIN
    PADDLE_B_POSITION = WIDTH / 2 - PADDLE_MARGIN

    def __init__(self):
        self.player_left = 0
        self.player_right = 0
        self.window = Window(self.WIDTH, self.HEIGHT)
        self.paddle_left = Paddle(self.PADDLE_A_POSITION)
        self.paddle_right = Paddle(self.PADDLE_B_POSITION)
        self.ball = Ball(window_width=self.window.get_width(), window_height=self.window.get_height())
        self.__bind_keys()

    def __bind_keys(self):
        self.window.win.onkeypress(self.paddle_left.move_up, 'w')
        self.window.win.onkeypress(self.paddle_left.move_down, 's')
        self.window.win.onkeypress(self.paddle_right.move_up, 'Up')
        self.window.win.onkeypress(self.paddle_right.move_down, 'Down')
        self.window.win.onkeypress(self.hit_paddle, 't')

    def is_goal(self):
        right_border = (self.window.get_width() / 2) - self.ball.get_dimension() / 2
        left_border = right_border * -1

        if self.ball.xcor() > right_border:
            self.player_left += 1
            self.ball.reset_reverse_position()

        elif self.ball.xcor() < left_border:
            self.player_right += 1
            self.ball.reset_reverse_position()

    def hit_paddle(self):
        left_top, left_side, left_bottom = self.paddle_left.get_borders()
        print(left_side, left_top, left_bottom)
        right_top, right_side, right_bottom = self.paddle_right.get_borders()
        print(right_side, right_top, right_bottom)

    def run(self):
        while True:
            self.window.win.update()
            self.ball.move()
            self.is_goal()


game = Game()
game.run()
