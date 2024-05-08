from ..utils.streamlit_utils import st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier 

class ModelTraining:
    def __init__(_self, X_train, y_train):
        _self.X_train = X_train
        _self.y_train = y_train

    @st.cache_data(show_spinner="Training Selected Models...")
    def train_models(_self, models):
        if "Logistic Regression" in models:
            with st.spinner("Training Logistic/Linear Regression model..."):
                lr = LogisticRegression()
                lr.fit(_self.X_train, _self.y_train)
                st.success("Logistic Regression model training complete!")
                st.write("Default Hyperparameters for Logistic Regression model:")
                params_df = pd.DataFrame.from_dict(lr.get_params(), orient='index', columns=['Value'])
                params_df.reset_index(inplace=True)
                params_df.columns = ['Hyperparameter', 'Value']
                st.dataframe(params_df)

                st.session_state.default_params['Logistic Regression'] = params_df
                st.session_state.trained_models.append(lr)
                st.session_state.trained_models_dict['Logistic Regression'] = lr

        if "Decision Tree" in models:
            with st.spinner("Training Decision Tree model..."):
                dtree = DecisionTreeClassifier()
                dtree.fit(_self.X_train, _self.y_train)
                st.success("Decision Tree model training complete!")
                st.write("Default Hyperparameters for Decision Tree model:")
                params_df = pd.DataFrame.from_dict(dtree.get_params(), orient='index', columns=['Value'])
                params_df.reset_index(inplace=True)
                params_df.columns = ['Hyperparameter', 'Value']
                st.dataframe(params_df)

                st.session_state.default_params['Decision Tree'] = params_df
                st.session_state.trained_models.append(dtree)
                st.session_state.trained_models_dict['Decision Tree'] = dtree

        if "Random Forest" in models:
            with st.spinner("Training Random Forest model..."):
                rf = RandomForestClassifier()
                rf.fit(_self.X_train, _self.y_train)
                st.success("Random Forest model training complete!")
                st.write("Default Hyperparameters for Random Forest model:")
                params_df = pd.DataFrame.from_dict(rf.get_params(), orient='index', columns=['Value'])
                params_df.reset_index(inplace=True)
                params_df.columns = ['Hyperparameter', 'Value']
                st.dataframe(params_df)

                st.session_state.default_params['Random Forest'] = params_df
                st.session_state.trained_models.append(rf)
                st.session_state.trained_models_dict['Random Forest'] = rf

        if "XGBoost" in models:
            with st.spinner("Training XGBoost model..."):
                xgb = XGBClassifier()
                xgb.fit(_self.X_train, _self.y_train)
                st.success("XGBoost model training complete!")
                st.write("Default Hyperparameters for XGBoost model:")
                params_df = pd.DataFrame.from_dict(xgb.get_params(), orient='index', columns=['Value'])
                params_df.reset_index(inplace=True)
                params_df.columns = ['Hyperparameter', 'Value']
                st.dataframe(params_df)

                st.session_state.default_params['XGBoost'] = params_df
                st.session_state.trained_models.append(xgb)
                st.session_state.trained_models_dict['XGBoost'] = xgb

        if "AdaBoost" in models:
            with st.spinner("Training AdaBoost model..."):
                ada = AdaBoostClassifier()
                ada.fit(_self.X_train, _self.y_train)
                st.success("AdaBoost model training complete!")
                st.write("Default Hyperparameters for AdaBoost model:")
                params_df = pd.DataFrame.from_dict(ada.get_params(), orient='index', columns=['Value'])
                params_df.reset_index(inplace=True)
                params_df.columns = ['Hyperparameter', 'Value']
                st.dataframe(params_df)

                st.session_state.default_params['AdaBoost'] = params_df
                st.session_state.trained_models.append(ada)
                st.session_state.trained_models_dict['AdaBoost'] = ada

        if "LightGBM" in models:
            with st.spinner("Training SVM model..."):
                lgbm = LGBMClassifier(max_depth = 7, num_leaves = 80)
                lgbm.fit(_self.X_train, _self.y_train)
                st.success("LightGBM model training complete!")
                st.write("Default Hyperparameters for LightGBM model:")
                params_df = pd.DataFrame.from_dict(lgbm.get_params(), orient='index', columns=['Value'])
                params_df.reset_index(inplace=True)
                params_df.columns = ['Hyperparameter', 'Value']
                st.dataframe(params_df)

                st.session_state.default_params['LightGBM'] = params_df
                st.session_state.trained_models.append(lgbm)     
                st.session_state.trained_models_dict['LightGBM'] = lgbm