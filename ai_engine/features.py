import math
import numpy as np
import pandas as pd

def compute_dew_point_array(temp_c, humidity):
    """Vectorized Magnus formula for dew point calculation."""
    a = 17.27
    b = 237.7
    # Clip humidity safely
    h = np.clip(humidity, 1.0, 100.0)
    alpha = ((a * temp_c) / (b + temp_c)) + np.log(h / 100.0)
    dp = (b * alpha) / (a - alpha)
    return np.round(dp, 2)

def compute_heat_index_array(temp_c, humidity):
    """Vectorized NOAA heat index calculation."""
    T = (temp_c * 9.0 / 5.0) + 32.0
    R = np.clip(humidity, 0.0, 100.0)

    # Simplified Steadman
    hi_simple = 0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (R * 0.094))
    
    # Rothfusz equation
    hi_full = (-42.379 + 
               2.04901523 * T + 
               10.14333127 * R - 
               0.22475541 * T * R - 
               0.00683783 * (T**2) - 
               0.05481717 * (R**2) + 
               0.00122874 * (T**2) * R + 
               0.00085282 * T * (R**2) - 
               0.00000199 * (T**2) * (R**2))

    hi = np.where(hi_simple < 80.0, hi_simple, hi_full)
    hi_c = (hi - 32.0) * 5.0 / 9.0
    return np.round(hi_c, 2)

def generate_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw atmospheric records into high-accuracy meteorological feature matrix.
    Expected columns: ['timestamp', 'temperature', 'humidity', 'pressure']
    Optional: ['precipitation', 'wind_speed', 'cloud_cover']
    """
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    if hasattr(df['timestamp'].dt, 'tz') and df['timestamp'].dt.tz is not None:
        df['timestamp'] = df['timestamp'].dt.tz_localize(None)

    df = df.sort_values('timestamp').reset_index(drop=True)

    # 1. Cyclical Time Encodings
    hour = df['timestamp'].dt.hour
    day_of_year = df['timestamp'].dt.dayofyear
    month = df['timestamp'].dt.month

    df['hour_sin'] = np.sin(2 * np.pi * hour / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * hour / 24.0)
    df['day_sin'] = np.sin(2 * np.pi * day_of_year / 365.25)
    df['day_cos'] = np.cos(2 * np.pi * day_of_year / 365.25)
    df['month_sin'] = np.sin(2 * np.pi * month / 12.0)
    df['month_cos'] = np.cos(2 * np.pi * month / 12.0)

    # 2. Regional Climate Regimes (Chennai / Poonamallee specific)
    # Northeast Monsoon (October, November, December) brings ~60% of annual rainfall
    df['is_ne_monsoon'] = month.isin([10, 11, 12]).astype(float)
    # Southwest Monsoon (June to September)
    df['is_sw_monsoon'] = month.isin([6, 7, 8, 9]).astype(float)
    # Peak summer heat (April, May - Agni Natchathiram)
    df['is_summer'] = month.isin([4, 5]).astype(float)

    # 3. Derived Thermodynamics
    df['dew_point'] = compute_dew_point_array(df['temperature'].values, df['humidity'].values)
    df['dew_point_depression'] = df['temperature'] - df['dew_point']
    df['heat_index'] = compute_heat_index_array(df['temperature'].values, df['humidity'].values)

    # 4. Differentials & Rates of Change
    df['pressure_diff_1h'] = df['pressure'].diff(1).fillna(0.0)
    df['pressure_diff_3h'] = df['pressure'].diff(3).fillna(0.0)
    df['pressure_diff_6h'] = df['pressure'].diff(6).fillna(0.0)
    df['temp_diff_1h'] = df['temperature'].diff(1).fillna(0.0)
    df['temp_diff_3h'] = df['temperature'].diff(3).fillna(0.0)
    df['humidity_diff_1h'] = df['humidity'].diff(1).fillna(0.0)

    # 5. Moving Averages and Volatility
    df['temp_roll_mean_6h'] = df['temperature'].rolling(window=6, min_periods=1).mean()
    df['temp_roll_std_6h'] = df['temperature'].rolling(window=6, min_periods=1).std().fillna(0.0)
    df['pressure_roll_mean_6h'] = df['pressure'].rolling(window=6, min_periods=1).mean()
    df['humidity_roll_mean_6h'] = df['humidity'].rolling(window=6, min_periods=1).mean()

    # 6. Lagged Sensor States (historical context)
    for lag in [1, 2, 3, 6, 12, 24]:
        df[f'temp_lag_{lag}h'] = df['temperature'].shift(lag).bfill()
        df[f'pressure_lag_{lag}h'] = df['pressure'].shift(lag).bfill()
        df[f'humidity_lag_{lag}h'] = df['humidity'].shift(lag).bfill()

    return df
