import pandas as pd
from src.forecastout.a_data_engine.data_handler import DataHandler


class InputChecker:

    def __init__(
            self,
            df: pd.DataFrame,
            sum_aggregation: bool = True,
            horizon: int = None,
            months_to_backtest: int = None,
            models_to_use: list = None,
            average_top_models_number: int = None
    ):
        # -- Main inputs
        self.df = df
        self.sum_aggregation = sum_aggregation
        self.horizon = horizon
        self.months_to_backtest = months_to_backtest
        self.models_to_use = models_to_use
        self.average_top_models_number = average_top_models_number
        # -- Preliminary Checks
        self.__check_df_column_names()
        self.__check_sum_aggregation()
        self.__check_horizon()
        self.__check_months_to_backtest()
        self.__check_models_to_use()
        self.__check_average_top_models_number()
        self.__check_backtesting_consistency()

    def __check_df_column_names(self):
        column_names_list = ['date', 'value']
        for column in self.df.columns:
            if column not in column_names_list:
                error_string = (
                    f"Column name '{column}' for the input " +
                    f"DataFrame is not acceptable. The acceptable " +
                    f"column names for a DataFrame to be " +
                    f"accepted are: {column_names_list}."
                )
                raise ValueError(error_string)

    def __check_backtesting_consistency(self):
        # -- Checks of DF
        data_handler = DataHandler(
            df=self.df,
            horizon=self.horizon,
            sum_aggregation=self.sum_aggregation
        )
        df_monthly = data_handler.df_monthly.copy()
        # -- df_monthly
        num_of_monthly_observations = df_monthly.dropna()['date'].count()
        if num_of_monthly_observations - self.months_to_backtest < 24:
            error_string = (
                f"Your data consists in  " +
                f"'{num_of_monthly_observations}' observations, " +
                f"while the input parameter 'months_to_backtest' " +
                f"is set to '{self.months_to_backtest}'. " +
                f"Make sure that the number of observations " +
                f"minus the input parameter 'months_to_backtest' " +
                f"is larger than 24."
            )

            raise ValueError(error_string)

    def __check_sum_aggregation(self):
        aggregation_names_list = ['sum', 'avg']
        if not isinstance(self.sum_aggregation, bool):
            error_string = (
                f"sum_aggregation input parameter" +
                f"'{self.sum_aggregation}' is not acceptable. " +
                f"The acceptable sum_aggregation input " +
                f"names are: {aggregation_names_list}."
            )
            raise ValueError(error_string)

    def __check_horizon(self):
        if not isinstance(self.horizon, int):
            error_string = (
                f"horizon input type " +
                f"'{self.horizon}' is not acceptable." +
                f"The acceptable horizon input type " +
                f"is an integer. E.g. 3."
            )
            raise ValueError(error_string)

    def __check_months_to_backtest(self):
        if not isinstance(self.months_to_backtest, int):
            error_string = (
                f"months_to_backtest input type " +
                f"'{self.months_to_backtest}' is not acceptable. " +
                f"The acceptable months_to_backtest input type " +
                f"is an integer. E.g. 3."
            )
            raise ValueError(error_string)

    def __check_models_to_use(self):
        model_names_list = [
            'autoarima',
            'holtwinters',
            'prophet',
            'seasonalnaive'
        ]
        for model in self.models_to_use:
            if model not in model_names_list:
                error_string = (
                    f"Model name '{model}' is not acceptable. " +
                    f"The acceptable model names are: " +
                    f"{model_names_list}."
                )
                raise ValueError(error_string)

    def __check_average_top_models_number(self):
        if not isinstance(self.average_top_models_number, int):
            error_string = (
                f"average_top_models_number input type " +
                f"'{self.average_top_models_number}' is not acceptable. " +
                f"The acceptable average_top_models_number input " +
                f"type is an integer. E.g. 1."
            )
            raise ValueError(error_string)
