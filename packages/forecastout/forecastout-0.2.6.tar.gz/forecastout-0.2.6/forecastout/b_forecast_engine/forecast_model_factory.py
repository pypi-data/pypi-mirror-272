# Main forecasting c_forecast_models
# -- Python main packages
from forecastout.c_forecast_models.autoarima_model import AutoArimaModel
from forecastout.c_forecast_models.prophet_model import ProphetModel
from forecastout.c_forecast_models.holtwinters_model import HoltWintersModel
from forecastout.c_forecast_models.naive_seasonal import NaiveSeasonalModel


class ForecastModelFactory:
    @staticmethod
    def get_model(model, df_train_y, dict_config, series_train_dates):
        if model == "autoarima":
            return AutoArimaModel(
                df_train_y=df_train_y,
                dict_config=dict_config
            )
        if model == "prophet":
            return ProphetModel(
                df_train_y=df_train_y,
                dict_config=dict_config,
                series_train_dates=series_train_dates
            )
        if model == "holtwinters":
            return HoltWintersModel(
                df_train_y=df_train_y,
                dict_config=dict_config,
                series_train_dates=series_train_dates
            )
        if model == "seasonalnaive":
            return NaiveSeasonalModel(
                df_train_y=df_train_y,
                dict_config=dict_config,
                series_train_dates=series_train_dates
            )
