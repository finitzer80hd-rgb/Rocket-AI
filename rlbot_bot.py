"""RLBot v5 entry point for the Rocket AI starter.

This baseline drives toward the ball in an offline RLBot match. It is a safe,
testable integration point for a learned policy; it is not a competitive bot yet.
"""
from __future__ import annotations

import math

from rlbot.flat import ControllerState, GamePacket
from rlbot.managers import Bot


def _clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


class RocketAIBot(Bot):
    """Minimal RLBot v5 bot with ball-chasing baseline behavior."""

    def get_output(self, packet: GamePacket) -> ControllerState:
        controls = ControllerState()
        if not packet.balls or self.index >= len(packet.players):
            return controls

        car = packet.players[self.index]
        ball = packet.balls[0]
        car_pos = car.physics.location
        ball_pos = ball.physics.location
        dx = float(ball_pos.x - car_pos.x)
        dy = float(ball_pos.y - car_pos.y)
        yaw = float(car.physics.rotation.yaw)

        # Convert target direction into the car's local coordinate frame.
        local_x = dx * math.cos(yaw) + dy * math.sin(yaw)
        local_y = -dx * math.sin(yaw) + dy * math.cos(yaw)
        angle = math.atan2(local_y, local_x)

        controls.steer = _clamp(angle * 4.0)
        controls.throttle = 1.0

        distance = math.sqrt(dx * dx + dy * dy + float(ball_pos.z - car_pos.z) ** 2)
        speed = math.sqrt(
            float(car.physics.velocity.x) ** 2
            + float(car.physics.velocity.y) ** 2
            + float(car.physics.velocity.z) ** 2
        )
        # Use boost only when broadly pointed toward the ball and not near top speed.
        controls.boost = abs(angle) < 0.22 and speed < 2200 and car.boost > 10
        # A conservative ground approach; aerial logic will be learned/added later.
        controls.jump = False
        return controls


if __name__ == "__main__":
    RocketAIBot("finitzer80hd-rgb/rocket-ai").run()
