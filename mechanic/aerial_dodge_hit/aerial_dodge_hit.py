from mechanic.base_mechanic import BaseMechanic
from rlbot.agents.base_agent import SimpleControllerState
from mechanic.aerial_turn.face_vector import FaceVectorRLU
from RLUtilities.LinearAlgebra import vec3
from RLUtilities.Simulation import Car
from RLUtilities.Maneuvers import AirDodge
from enum import Enum

class States(Enum):
    INITIAL = 0
    JUMPING = 1
    FACING = 2
    WAITING = 3
    DODGING = 4

class BaseAerialDodgeHit(BaseMechanic):
    def __init__(self):
        super().__init__()
    def is_viable(self, car: Car, target: vec3) -> bool:
        pass

class AerialDodgeHit(BaseAerialDodgeHit):
    def __init__(self):
        super().__init__()
        self.face_vector = FaceVectorRLU()
        self.state = States.INITIAL
        self.dodge = None

    def step(self, car: Car, target: vec3, dodge_distance: float = 220, dt: float =  0.01667) -> SimpleControllerState:
        if car.on_ground and not car.jumped:
            self.controls.jump = not self.controls.jump
            self.state = States.JUMPING
        else:
            self.controls.jump = False
            if not self.face_vector.finished:
                self.state = States.FACING
                self.face_vector.step(car, target)
                self.controls.pitch = self.face_vector.controls.pitch
                self.controls.yaw = self.face_vector.controls.yaw
                self.controls.roll = self.face_vector.controls.roll
            else:
                self.state = States.WAITING
                self.controls.pitch = 0
                self.controls.yaw = 0
                self.controls.roll = 0
                self.controls.jump = False

            if magnitude(car.pos - target) <= dodge_distance or self.state == States.DODGING:
                self.state = States.DODGING
                if self.dodge == None:
                    self.dodge = AirDodge(car, target = target)

                if self.dodge.finished:
                    self.finished = True
                else:
                    self.dodge.step(dt)
                    self.controls = self.dodge.controls

        return self.controls

def magnitude(v: vec3) -> float:
    return (v[0]**2 + v[1]**2 + v[2]**2)**0.5
