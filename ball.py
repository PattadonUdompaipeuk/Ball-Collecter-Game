import turtle
import math


class Ball:
    def __init__(self, size, x, y, vx, vy, color):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = 100 * size ** 2
        self.count = 0
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1] * 1.5

    def draw(self):
        # draw a circle of radius equals to size centered at (x, y) and paint it with color
        turtle.penup()
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.goto(self.x, self.y - self.size)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()

    def bounce_off(self, that):
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx * dvx + dy * dvy  # dv dot dr
        dist = self.size + that.size  # distance between particle centers at collison

        overlap = dist - math.sqrt(dx ** 2 + dy ** 2)
        if overlap > 0:
            correction_factor = overlap / dist
            self.x -= correction_factor * dx / 2
            self.y -= correction_factor * dy / 2
            that.x += correction_factor * dx / 2
            that.y += correction_factor * dy / 2

        # magnitude of normal force
        magnitude = 2 * self.mass * that.mass * dvdr / ((self.mass + that.mass) * dist)

        # normal force, and in x and y directions
        fx = magnitude * dx / dist
        fy = magnitude * dy / dist

        # update velocities according to normal force
        self.vx += fx / self.mass
        self.vy += fy / self.mass
        that.vx -= fx / that.mass
        that.vy -= fy / that.mass

        # update collision counts
        self.count += 1
        that.count += 1

    def distance(self, that):
        x1 = self.x
        y1 = self.y
        x2 = that.x
        y2 = that.y
        d = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return d

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def bounce_off_wall(self):
        if self.x + self.size >= self.canvas_width or self.x - self.size <= -self.canvas_width:
            self.vx = -self.vx
        if self.y + self.size >= self.canvas_height or self.y - self.size <= -self.canvas_height:
            self.vy = -self.vy

    def __str__(self):
        return str(self.x) + ":" + str(self.y) + ":" + str(self.vx) + ":" + str(self.vy) + ":" + str(self.count)
