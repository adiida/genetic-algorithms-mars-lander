class Time():
    def __init__(self, seconds):
        self.seconds = seconds

    def __str__(self):
        return f"Current seconds: {self.seconds}"


class Speed():
    """Represent speed as a vector which allow add them
    speed1 + speed2 = new speed
    direction: instance of Vector class
    """
    def __init__(self, direction):
        self.direction = direction
        self.h_speed = direction.dx
        self.v_speed = direction.dy

    def __str__(self):
        return f"(hSpeed:{self.h_speed:.2f}, vSpeed:{self.v_speed:.2f})"

    def __add__(self, speed):
        return Speed(self.direction + speed.direction)


class Acceleration():
    """Represent speed as a vector which allow add them
    acc1 + acc2 = new acc
    Acceleration * Time -> Speed
    """
    def __init__(self, vector):
        self.vector = vector

    def __str__(self):
        return self.vector.__str__()

    def __add__(self, acceleration):
        return Acceleration(self.vector + acceleration.vector)

    def __mul__(self, time):
        return Speed(self.vector * time.seconds)


class Particle():
    """Represent something with an initial point and speed
    and on which an acceleration can be applied
    position: instance of Point class
    speed: instance of Speed class
    """
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed

    def __str__(self):
        return (f"x={self.position.x:.2f}, y={self.position.y:.2f}; "
                f"speed: {self.speed}")

    def accelerate(self, acceleration, time):
        new_position = (self.position + self.speed.direction * time.seconds
                        + acceleration.vector * time.seconds ** 2 * 0.5)
        new_position.x = round(new_position.x)
        new_position.y = round(new_position.y)

        new_speed = Speed(self.speed.direction + acceleration.vector
                          * time.seconds)
        new_speed.h_speed = round(new_speed.h_speed)
        new_speed.v_speed = round(new_speed.v_speed)

        return Particle(new_position, new_speed)
