import pandas as pd

class StockTransactionAnalyzer:
    """
    A Python class to analyze stock transactions.
    """

    def __init__(self, transactions_df, scenarios_df):
        """
        Initializes the StockTransactionAnalyzer with transactions and scenarios DataFrames.

        Args:
            transactions_df (DataFrame): DataFrame containing transaction data.
            scenarios_df (DataFrame): DataFrame containing scenario data.
        """
        self.transactions_df = transactions_df
        self.scenarios_df = scenarios_df

    def split(self):
        """
        Splits the transactions DataFrame based on scenarios and returns a list of DataFrames.

        Returns:
            list: A list of DataFrames, each containing filtered transactions for a scenario.
        """
        filtered_data = []

        # Iterate through each scenario
        for _, scenario in self.scenarios_df.iterrows():
            scenario_name = scenario["key"]
            scenario_stocks = scenario["stocks"]

            # Filter transactions DataFrame for the current scenario
            scenario_filtered_df = pd.DataFrame()

            # Iterate through each stock in the scenario
            for stock_obj in scenario_stocks:
                stock = stock_obj["stock"]
                transaction_type = stock_obj["transaction_type"]

                # Filter transactions DataFrame based on stock and transaction type
                stock_filtered_df = self.transactions_df[
                    (self.transactions_df['stock'] == stock) &
                    (self.transactions_df['transaction_type'] == transaction_type)
                ]

                # Concatenate filtered DataFrame with the current scenario's DataFrame
                scenario_filtered_df = pd.concat([scenario_filtered_df, stock_filtered_df])

            # Append filtered DataFrame to the list
            filtered_data.append((scenario_name, scenario_filtered_df))

        return filtered_data
