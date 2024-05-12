import pandas as pd

def extract_features(df, addressed_sensor_col):

    def find_correlated_columns(df, addressed_sensor_col):
        correlated_columns = []

        # Create a new DataFrame with the addressed sensor column
        new_df = pd.DataFrame(df[addressed_sensor_col])

        # Find correlated columns to the addressed sensor
        for col in df.columns:
            if col != addressed_sensor_col:
                correlation_coefficient = df[addressed_sensor_col].corr(df[col])
                if abs(correlation_coefficient) > 0.7:
                    correlated_columns.append(col)
                    new_col_name = f"{col}"
                    new_df[new_col_name] = df[col]

        # Find pairs of correlated columns that are also correlated to each other
        correlated_pairs = []
        for i, col1 in enumerate(correlated_columns):
            for col2 in correlated_columns[i+1:]:
                correlation_coefficient = df[col1].corr(df[col2])
                print(col1,col2,correlation_coefficient)
                if abs(correlation_coefficient) > 0.65:
                    correlated_pairs.append([col1, col2])

        return new_df, correlated_pairs
    correlated_df, correlated_pairs =find_correlated_columns(df, addressed_sensor_col)
    rest_columns = df.iloc[:, 1:]  # Selecting the rest of the columns
    first_column = df.iloc[:, 0]
    df_corollated = df
    for col in df_corollated.columns[1:]:
        differences = addressed_sensor_col - df_corollated[col]
        df[f'Difference_{col}'] = differences

    df_main_diff = df_corollated.diff()
    prev_first_column= first_column.shift()
    df = pd.concat([df, df_main_diff.add_prefix('speed_change_')], axis=1)
    PRD = ((abs(first_column - prev_first_column)) / ((first_column + prev_first_column)*0.5))*100
    df['PRD'] = ((abs(first_column - prev_first_column)) / ((first_column + prev_first_column)*0.5))
    for pair in correlated_pairs:
        col1, col2 = pair
        difference_col_name = f'{col1}_{col2}_difference'
        df[difference_col_name] = df_corollated[col1] - df_corollated[col2]
    return df,correlated_pairs




