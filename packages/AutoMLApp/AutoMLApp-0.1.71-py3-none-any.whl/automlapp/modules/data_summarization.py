from utils.streamlit_utils import st

class DataSummarization:
    def __init__(_self, df):
        _self.df = df

    def summarize(_self):
        if _self.df is not None:
            desc_stats = _self.df.describe().T
            additional_percentiles = [0.01, 0.05, 0.10, 0.90, 0.95, 0.99]
            for percentile in additional_percentiles:
                desc_stats[f'P{int(percentile * 100)}'] = _self.df.quantile(percentile)
            desc_stats['missing'] = _self.df.isna().sum()
            desc_stats = desc_stats.rename(columns = {'min': 'P0 (min)', '25%': 'P25', '50%': 'P50 (median)', '75%': 'P75', 'max': 'P100 (max)'})
            st.write(desc_stats[['count', 'missing', 'mean', 'std', 'P0 (min)', 'P1', 'P5', 'P10', 'P25', 'P50 (median)', 'P75', 'P90', 'P95', 'P99', 'P100 (max)']])
        
            st.write(f"Total number of missing values (entire row missing): :red[{_self.df.isna().sum().sum()}]")
            st.write(f"Total number of duplicated values (entire row duplicated): :red[{_self.df.duplicated().sum().sum()}]")