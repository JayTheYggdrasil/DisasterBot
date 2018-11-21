import math

from action.base_action import BaseAction
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from RLUtilities.GameInfo import GameInfo
from RLUtilities.Simulation import Car, Ball
from RLUtilities.LinearAlgebra import vec3, dot, clip


class Kickoff(BaseAction):
    def get_output(self, info: GameInfo) -> SimpleControllerState:

        ball = info.ball
        car = info.my_car

        local_coords = dot(ball.pos - car.pos, car.theta)

        self.controls.steer = math.copysign(1.0, local_coords[1])

        # just set the throttle to 1 so the car is always moving forward
        self.controls.throttle = 1.0

        return self.controls

    def get_possible(self, info: GameInfo):
        return True
