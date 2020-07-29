from plane import Vector
from motion import Time, Acceleration
import enum

GRAVITY = Acceleration(Vector(0.0, -3.711))
MAX_X = 6999
MIN_X = 0


class ControlCommands():
    """Commands for controlling Mars lander
    - power : 0, 1, 2, 3, 4
    - angle : -90, -75, ... , 0, +15, +30, ..., +75, +90
    """
    def __init__(self, angle, power):
        self.angle = angle
        self.power = power


class State():
    """Current state of Mars lander
    - fuel: integer
    - power : 0, 1, 2, 3, 4
    - angle : -90, -75, ... , 0, +15, +30, ..., +75, +90
    - particle: instance of Particle class
    """
    def __init__(self, fuel, power, angle, particle):
        self.fuel = fuel
        self.power = power
        self.angle = angle
        self.particle = particle
        self.position = particle.position
        self.speed = particle.speed


class FlyState(enum.Enum):
    Landed = 1
    Crashed = 2
    Flying = 3


class LandingZone():
    """Find landing zone (two points with equal y coordinates)"""
    def __init__(self, points):
        self.points = points
        self.landing_points = None

    def find_landing_zone(self):
        for i in range(1, len(self.points)):
            if self.points[i-1].y == self.points[i].y:
                self.landing_points = (self.points[i-1], self.points[i])
                break


class Lander():
    """All physics of Mars lander (speed, acceleration, trajectory, ...)"""
    def __init__(self, init_state, commands, ground):
        self.trajectory = [init_state]
        self.flystate = FlyState.Flying
        self.commands = commands
        self.ground = ground
        self.landing_zone = []
        self.fitness = 0.0
        self.compute_trajectory()
        self.calculate_fitness()

    def compute_trajectory(self):
        for i, cmd in enumerate(self.commands):
            next_state = self.compute_next_state(self.trajectory[i], cmd)
            self.trajectory.append(next_state)

            if self.evaluate_outside(next_state):
                return 1
            if self.evaluate_hit_the_ground(next_state):
                return 1
            if self.evaluate_no_fuel(next_state):
                return 1

    def evaluate_outside(self, next_state):
        if next_state.position.x > MAX_X or next_state.position.x < MIN_X:
            self.flystate = FlyState.Crashed
            return True
        return False

    def evaluate_hit_the_ground(self, next_state):
        if (self.ground > next_state.position):
            if (next_state.angle == 0
                and abs(next_state.speed.v_speed) <= 40
                and abs(next_state.speed.h_speed) <= 20
                    and self.ground.is_horizontal_at_x(next_state.position.x)):
                self.flystate = FlyState.Landed
            else:
                self.flystate = FlyState.Crashed
            return True
        return False

    def evaluate_no_fuel(self, next_state):
        if next_state.fuel <= 0:
            self.flystate = FlyState.Crashed
            return True
        return False

    def coerce_range(self, value, min_value, max_value):
        if value < min_value:
            return min_value
        if value > max_value:
            return max_value
        return value

    def compute_next_state(self, curr_state, cmd, time=Time(1)):
        new_angle = (curr_state.angle +
                     self.coerce_range(cmd.angle - curr_state.angle, -15, 15))
        new_power = (curr_state.power +
                     self.coerce_range(cmd.power - curr_state.power, -1, 1))

        thrust = (Vector(0.0, 1.0) * new_power).rotate(new_angle)
        thrust_acceleration = Acceleration(thrust)
        acceleration = GRAVITY + thrust_acceleration
        new_particle = curr_state.particle.accelerate(acceleration, time)
        new_fuel = curr_state.fuel - new_power

        return State(new_fuel, new_power, new_angle, new_particle)

    def hit_landing_area(self):
        land = LandingZone(self.ground.points)
        land.find_landing_zone()
        self.landing_zone = land.landing_points
        lander_last_position = self.trajectory[-2].position
        lander_hit_area = self.ground.get_segment_for(lander_last_position.x)
        if (self.landing_zone[0].x == lander_hit_area[0].x
            and self.landing_zone[0].y == lander_hit_area[0].y
            and self.landing_zone[1].x == lander_hit_area[1].x
                and self.landing_zone[1].y == lander_hit_area[1].y):
            return True
        return False

    def calculate_fitness(self):
        if not self.hit_landing_area():
            last_position = self.trajectory[-2].position
            distance = self.landing_zone[0].distance_to(last_position)
            self.fitness = 1 / distance
        else:
            last_speed = self.trajectory[-2].speed
            x_pen = 0
            if abs(last_speed.h_speed) > 20:
                x_pen = (abs(last_speed.h_speed) - 20)

            y_pen = 0
            if last_speed.v_speed < -40:
                y_pen = (-40 - last_speed.v_speed)

            self.fitness = 1 - (1 / (x_pen + y_pen))
