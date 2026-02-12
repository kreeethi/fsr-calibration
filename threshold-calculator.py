import pandas as pd
import numpy as np

df = pd.read_csv("[input file name here]")

def moving_average(x, w=15):
    return pd.Series(x).rolling(window=w, center=True, min_periods=1).mean().to_numpy()

thresholds = {}

for sensor_id, d in df.groupby("sensor_id"):
    d = d.copy()
    d["adc_smooth"] = moving_average(d["adc"].to_numpy(), w=15)

    # T1 (avoid false touches, prevents vibrations)
    base = d[d["label"] == "none"]["adc_smooth"].to_numpy()
    T1 = np.percentile(base, 99) # potential cut off point for no touch

    # current approach: use median as cut off point.
    light = d[d["label"] == "light"]["adc_smooth"].to_numpy()
    medium = d[d["label"] == "medium"]["adc_smooth"].to_numpy()
    hard = d[d["label"] == "hard"]["adc_smooth"].to_numpy()

    light_mid = np.median(light)
    medium_mid = np.median(medium)
    hard_mid = np.median(hard)

    T2 = (light_mid + medium_mid) / 2
    T3 = (medium_mid + hard_mid) / 2

    # prevent flicker
    min_gap = 10 # filler number, can change
    if T2 < T1 + min_gap: T2 = T1 + min_gap
    if T3 < T2 + min_gap: T3 = T2 + min_gap

    thresholds[sensor_id] = (float(T1), float(T2), float(T3))

print("Computed thresholds (T1, T2, T3): ")
for sid, (T1, T2, T3) in thresholds.items():
    print(f"Sensor {sid}: {T1:.1f}, {T2:.1f}, {T3:.1f}")