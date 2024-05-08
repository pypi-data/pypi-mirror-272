# <Copyright 2022, Argo AI, LLC. Released under the MIT license.>

"""Constants used throughout the SinD motion forecasting API."""

from typing import Final

SIND_SCENARIO_OBS_TIMESTEPS: Final[int] = 11        # 历史步长
SIND_SCENARIO_PRED_TIMESTEPS: Final[int] = 30       # 预测步长
SIND_SCENARIO_TOTAL_TIMESTEPS: Final[int] = SIND_SCENARIO_OBS_TIMESTEPS + SIND_SCENARIO_PRED_TIMESTEPS
SIND_SCENARIO_GENERATION_STEP: Final[int] = 100       # 采样步长

SIND_SCENARIO_RECORD_STEP_HZ: Final[float] = 29.97  # 采集帧率
SIND_SCENARIO_TRACK_STEP_HZ: Final[int] = 10        # 轨迹采样频率
SIND_SCENARIO_TRAFFICLIGHT_STEP_HZ: Final[int] = 30 # 红绿灯采样频率
