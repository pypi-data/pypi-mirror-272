from ..utils.streamlit_utils import st
import pandas as pd
import numpy as np
from scipy.stats import skew, boxcox
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

@st.cache_data
def log_transform(x):
    if np.any(x < 0):
        st.error(f"Negative or zero values encountered in '{x.name}' during Log transformation and hence cannot be applied")
        return x
    return np.log1p(x)

@st.cache_data
def boxcox_transform(x):
    if np.any(x <= 0):
        st.error(f"Negative or zero values encountered in '{x.name}' during Box-Cox transformation an hence cannot be applied")
        return x
    return boxcox(x - x.min() + 1)[0]

@st.cache_data
def sqrt_transform(x):
    if np.any(x < 0):
        st.error(f"Negative values encountered in '{x.name}' during Square Root transformation and hence transformation cannot be applied")
        return x
    return np.sqrt(x)

@st.cache_data
def reciprocal_transform(x):
    return 1 / (x + 1e-6)

transformations = {
    'Log Transformation': log_transform,
    'Box-Cox Transformation': boxcox_transform,
    'Square Root Transformation': sqrt_transform,
    'Reciprocal Transformation': reciprocal_transform
}

class DataPreprocessing:
    def __init__(_self, df, target):
        _self.df = df.copy()
        _self.target = target

    @st.cache_data
    def transform_columns(_self, method, S):
        skew_values = _self.df.apply(lambda x: skew(x))
        high_skew_columns = skew_values[skew_values > S].index

        transform = transformations[method]
        _self.df[high_skew_columns] = _self.df[high_skew_columns].apply(transform)
        
        return _self.df

    @st.cache_data
    def balance_dataset(_self, sample_tech, sample_st):
        X, y = _self.df.drop(_self.target, axis=1), _self.df[_self.target]
        if sample_tech == "Over Sampling":
            X_resampled, y_resampled = RandomOverSampler(random_state=0, sampling_strategy=sample_st).fit_resample(X, y)
        elif sample_tech == "Under Sampling":
            X_resampled, y_resampled = RandomUnderSampler(random_state=0, sampling_strategy=sample_st).fit_resample(X, y)
        elif sample_tech == "Combined":
            X_resampled, y_resampled = SMOTEENN(random_state=0, sampling_strategy=sample_st).fit_resample(X, y)
        _self.df = pd.DataFrame(X_resampled, columns=_self.df.columns[:-1])
        _self.df[_self.target] = y_resampled
        return _self.df

    @st.cache_data
    def scale_dataset(_self, scale_method):
        X, y = _self.df.drop(_self.target, axis = 1), _self.df[_self.target]
        if scale_method == "Standard Scaling":
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
        elif scale_method == "Min-Max Scaling":
            scaler = MinMaxScaler()
            X_scaled = scaler.fit_transform(X)
        elif scale_method == "Robust Scaling":
            scaler = RobustScaler()
            X_scaled = scaler.fit_transform(X)
        _self.df = pd.DataFrame(X_scaled, columns=_self.df.columns[:-1])
        _self.df[_self.target] = y
        return _self.df