import pandas as pd
import numpy as np

df = pd.read_csv("fsr-calibration-data")

def moving_average(x, w=15):
    return pd.Series(x).rolling(window=w, center=True, min_periods=1).mean().to_numpy()

thresholds = {}

# group by BOTH sensor_id and frustum
for (sensor_id, frustum), d in df.groupby(["sensor_id", "frustum"]):
    d = d.copy()
    d["adc_smooth"] = moving_average(d["adc"].to_numpy(), w=15)

    # T1: based on baseline/no-touch values
    base = d[d["label"] == "none"]["adc_smooth"].to_numpy()
    if len(base) == 0:
        print(f"Skipping sensor {sensor_id}, frustum {frustum}: no baseline data")
        continue
    T1 = np.percentile(base, 99)

    # Thresholds for light / medium / hard
    light = d[d["label"] == "light"]["adc_smooth"].to_numpy()
    medium = d[d["label"] == "medium"]["adc_smooth"].to_numpy()
    hard = d[d["label"] == "hard"]["adc_smooth"].to_numpy()

    if len(light) == 0 or len(medium) == 0 or len(hard) == 0:
        print(f"Skipping sensor {sensor_id}, frustum {frustum}: missing light/medium/hard data")
        continue

    light_mid = np.median(light)
    medium_mid = np.median(medium)
    hard_mid = np.median(hard)

    T2 = (light_mid + medium_mid) / 2
    T3 = (medium_mid + hard_mid) / 2

    # prevent flicker
    min_gap = 10
    if T2 < T1 + min_gap:
        T2 = T1 + min_gap
    if T3 < T2 + min_gap:
        T3 = T2 + min_gap

    thresholds[(sensor_id, frustum)] = (float(T1), float(T2), float(T3))

print("Computed thresholds (T1, T2, T3):")
for (sid, fr), (T1, T2, T3) in thresholds.items():
    print(f"Sensor {sid}, Frustum {fr}: T1={T1:.1f}, T2={T2:.1f}, T3={T3:.1f}")