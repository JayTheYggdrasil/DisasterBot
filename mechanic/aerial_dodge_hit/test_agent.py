from mechanic.base_test_agent import BaseTestAgent
from mechanic.base_mechanic import BaseMechanic
from mechanic.aerial_dodge_hit.aerial_dodge_hit import AerialDodgeHit
from rlbot.utils.game_state_util import GameState, CarState, BallState, Physics, Vector3, Rotator
from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

import time
import math
class TestAgent(BaseTestAgent):
    def create_mechanic(self) -> BaseMechanic:
        return AerialDodgeHit()

    def get_mechanic_controls(self) -> SimpleControllerState:
        return self.mechanic.step(self.info.my_car, self.info.ball.pos)

    def test_process(self, game_tick_packet: GameTickPacket):
        if self.mechanic.finished or time.time() - self.timer > 3:
            self.car_physics = Physics(velocity=Vector3(0, 300, 0), location = Vector3(0, 0, 0), rotation = Rotator(0, math.pi/2, 0))
            self.ball_state = BallState(physics=Physics(velocity=Vector3(0, 0, 200), location=Vector3(0, 400, 400)))
            self.set_game_state(GameState(cars={self.index: CarState(physics=self.car_physics)}, ball=self.ball_state))
            self.mechanic = self.create_mechanic()
            self.timer = time.time()

        self.renderer.begin_rendering()
        self.renderer.draw_string_2d(0, 100, 3, 3, str(self.mechanic.state), self.renderer.white() )
        self.renderer.end_rendering()

    def initialize_agent(self):
        self.timer = time.time()
