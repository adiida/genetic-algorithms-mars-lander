import math


class Point():
    """A point in a 2 dimensions cartesian plane
    Point + Vector -> Point
    Point - Point  -> Vector
    Point to Point distance -> Vector
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point(x:{self.x}, y:{self.y})"

    def __add__(self, vector):
        return Point(self.x + vector.dx, self.y + vector.dy)

    def __sub__(self, point):
        return Vector(self.x - point.x, self.y - point.y)

    def distance_to(self, point):
        return (point - self).magnitude()


class Vector():
    """A vector in a 2 dimensional cartesian plane
    Vector + Vector -> Vector
    Vector * Scalar -> Vector
    Vector rotation: Angle in radians -> Vector
    Vector magnitude: Vector -> Scalar
    """
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return f"Vector: [{self.dx}, {self.dy}]"

    def __add__(self, vector):
        return Vector(self.dx + vector.dx, self.dy + vector.dy)

    def __mul__(self, scalar):
        return Vector(self.dx * scalar, self.dy * scalar)

    def rotate(self, angle):
        """Angle given in degrees"""
        theta = math.radians(angle)
        cs = math.cos(theta)
        sn = math.sin(theta)
        return Vector(self.dx * cs - self.dy * sn, self.dx * sn + self.dy * cs)

    def magnitude(self):
        return math.sqrt(self.dx ** 2 + self.dy ** 2)


class Line():
    """A line is a List of point
    It is comparable to point:   Line (<, <=, ==, >=, >, !=) Point
    """
    def __init__(self, points):
        if len(points) < 2:
            raise ValueError('Line should have at least 2 points!')
        self.points = points

    def __lt__(self, point):
        return self.get_y_for_x(point.x) < point.y

    def __le__(self, point):
        return self.get_y_for_x(point.x) <= point.y

    def __eq__(self, point):
        return self.get_y_for_x(point.x) == point.y

    def __ge__(self, point):
        return self.get_y_for_x(point.x) >= point.y

    def __gt__(self, point):
        return self.get_y_for_x(point.x) > point.y

    def __ne__(self, point):
        return self.get_y_for_x(point.x) != point.y

    def get_segment_for(self, x):
        for i in range(1, len(self.points)):
            if self.points[i-1].x <= x and x <= self.points[i].x:
                return (self.points[i-1], self.points[i])

    def is_horizontal_at_x(self, x):
        points = self.get_segment_for(x)
        return points[0].y == points[1].y

    def get_y_for_x(self, x):
        points = self.get_segment_for(x)
        return (points[0].y + (x - points[0].x) * (points[1].y - points[0].y)
                / (points[1].x - points[0].x))
