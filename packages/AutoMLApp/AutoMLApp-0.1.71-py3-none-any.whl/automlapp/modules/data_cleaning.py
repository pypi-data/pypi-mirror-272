import numpy as np
import pandas as pd
from utils.streamlit_utils import hide_icons, remove_whitespaces, st

class DataCleaning:
    def __init__(_self, df):
        _self.df = df.copy()

    def detect_outliers(_self, lower_percentile=5, upper_percentile=95):
        lower_bound, upper_bound = _self.df.quantile(lower_percentile/100), _self.df.quantile(upper_percentile/100)
        
        # Count outliers in each column
        outlier_counts = ((_self.df < lower_bound) | (_self.df > upper_bound)).sum()
        return pd.DataFrame({'Column': outlier_counts.index, 'Outliers': outlier_counts.values})

    def remove_outliers(_self, lower=5, upper=95, columns=None):
        if columns is None:
            columns = _self.df.columns
        lower_bound = _self.df[columns].quantile(lower/100)
        upper_bound = _self.df[columns].quantile(upper/100)
        mask = (_self.df[columns] >= lower_bound) & (_self.df[columns] <= upper_bound)
        df_cleaned = _self.df[mask.all(axis=1)]
        return df_cleaned

    def cap_outliers(_self, lower=5, upper=95, columns=None):
        if columns is None:
            columns = _self.df.columns
        lower_bound, upper_bound = _self.df[columns].quantile(lower/100), _self.df[columns].quantile(upper/100)
        df_capped = _self.df.copy()
        df_capped[columns] = _self.df[columns].clip(lower=lower_bound, upper=upper_bound, axis=1)
        return df_capped

    def impute_outliers(_self, lower=5, upper=95, columns=None):
        if columns is None:
            columns = _self.df.columns
        df_imputed = _self.df.copy()
        lower_bound, upper_bound = df_imputed[columns].quantile(lower/100), df_imputed[columns].quantile(upper/100)

        # Identify integer categorical columns
        categorical_cols = [col for col in columns if df_imputed[col].nunique() <= 7 and df_imputed[col].dtype == 'int']

        # Impute outliers in categorical columns with mode
        for col in categorical_cols:
            mode = df_imputed[col].mode()[0]
            df_imputed[col] = np.where((df_imputed[col] < lower_bound[col]) | (df_imputed[col] > upper_bound[col]), mode, df_imputed[col])

        # Impute outliers in other columns with median
        numeric_cols = list(set(columns) - set(categorical_cols))
        for col in numeric_cols:
            median = df_imputed[col].median()
            df_imputed[col] = np.where((df_imputed[col] < lower_bound[col]) | (df_imputed[col] > upper_bound[col]), median, df_imputed[col])
        return df_imputed

    def treat_outliers(_self, lower, upper, outlier_tech, columns=None):
        if outlier_tech == "Remove Outliers":
            _self.df = _self.remove_outliers(lower, upper, columns)
        elif outlier_tech == "Cap Outliers":
            _self.df = _self.cap_outliers(lower, upper, columns)
        elif outlier_tech == "Impute Outliers":
            _self.df = _self.impute_outliers(lower, upper, columns)
        return _self.df

    def impute_missing(_self, cols_select, imp_method):
        if imp_method == "Mean":
            mean_dict = _self.df[cols_select][_self.df[cols_select] > 0].mean().to_dict()
            _self.df[cols_select] = _self.df[cols_select].fillna(mean_dict)
        elif imp_method == "Median":
            median_dict = _self.df[cols_select][_self.df[cols_select] > 0].median().to_dict()
            _self.df[cols_select] = _self.df[cols_select].fillna(median_dict)
        elif imp_method == "Mode":
            mode_dict = _self.df[cols_select][_self.df[cols_select] > 0].mode().iloc[0].to_dict()
            _self.df[cols_select] = _self.df[cols_select].fillna(mode_dict)
        return _self.df
    
    def impute_special(_self, cols_select, imp_method, special_vals=None):
        if special_vals:
            mean_dict = _self.df[cols_select][_self.df[cols_select] > 0].mean().to_dict()
            median_dict = _self.df[cols_select][_self.df[cols_select] > 0].median().to_dict()
            mode_dict = _self.df[cols_select][_self.df[cols_select] > 0].mode().iloc[0].to_dict()

            special_vals = [int(val) for val in special_vals.split(',')]
            _self.df[cols_select] = _self.df[cols_select].replace({val: np.nan for val in special_vals})
            if imp_method == "Mean":
                _self.df[cols_select] = _self.df[cols_select].fillna(mean_dict)
            elif imp_method == "Median":
                _self.df[cols_select] = _self.df[cols_select].fillna(median_dict)
            elif imp_method == "Mode":
                _self.df[cols_select] = _self.df[cols_select].fillna(mode_dict)
        return _self.df

    def replace_special(_self, cols_select, special_vals=None, replace_with=None):
        if cols_select and replace_with is not None and special_vals is not None:  
            special_vals = [int(val) for val in special_vals.split(',')]
            for col in cols_select:
                # Infer the data type of the column
                col_type = _self.df[col].dtype

                # Convert replace_with to that data type
                if col_type == np.int64:
                    replace_with = int(replace_with)
                elif col_type == np.float64:
                    replace_with = float(replace_with)

                _self.df[col] = _self.df[col].replace({val: replace_with for val in special_vals})
        return _self.df