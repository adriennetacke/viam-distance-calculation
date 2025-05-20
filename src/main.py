import asyncio
from viam.module.module import Module
try:
    from models.ultrasonic_distance_calculation import UltrasonicDistanceCalculation
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.ultrasonic_distance_calculation import UltrasonicDistanceCalculation


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
