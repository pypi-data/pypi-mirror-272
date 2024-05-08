import pandas as pd
import os.path as op
from src.forecastout.forecastout import ForecastOut

# -- set options
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

if __name__ == "__main__":
    # -- Read Data
    current_path = op.dirname(__file__)
    df = pd.read_csv(op.join(current_path, 'z_data_test/data_test2.csv'))
    # -- ForecastOut
    forecastout = ForecastOut(
        df=df.copy(),
        sum_aggregation=True,
        horizon=3,
        months_to_backtest=3,
        models_to_use=['autoarima', 'holtwinters', 'prophet'],
        average_top_models_number=1
    )
    # -- Outputs
    print(forecastout.df_monthly_forecast)
    print(forecastout.df_predictions_by_model)
    print(forecastout.df_daily_forecast)
    print(forecastout.df_ts_decomposition)
    print(forecastout.df_predictions_bt)
    print(forecastout.df_daily_shares)
