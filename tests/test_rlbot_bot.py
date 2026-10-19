from rlbot_bot import _clamp


def test_clamp_keeps_controls_in_safe_range():
    assert _clamp(-2.0) == -1.0
    assert _clamp(0.25) == 0.25
    assert _clamp(2.0) == 1.0
