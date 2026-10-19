# Integration adapters

Implement these as separate modules once the core pipeline passes tests:

- `rocketsim_adapter.py`: map normalized observations/actions to the installed RocketSim API; validate coordinate frames, units, tick rate, reset behavior and collisions.
- `rlbot_adapter.py`: map official RLBot game-state packets to the shared observation schema and map policy outputs to the supported controller-state object.
- `live_observer.py`: ingest authorized live observations or replay files, with explicit recording consent and timestamps. It should not inject inputs into protected online matchmaking.

Do not assume a particular RocketSim or RLBot API version. Pin the chosen release and write a small contract test against its actual installed API before implementing the adapter.
