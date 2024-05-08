from utils.streamlit_utils import st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

class HyperparameterTuning:
    def __init__(_self, X_train, y_train):
        _self.X_train = X_train
        _self.y_train = y_train

    @st.cache_data(show_spinner="Tuning Hyperparameters...")
    def tune_models(_self, models):
        if "Logistic Regression" in models:
            with st.spinner("Finding best parameters for Logistic Regression model..."):
                param_grid = {"penalty" : ['l1', 'l2', 'elasticnet'], 
                              "C" : [0.1, 1, 10], 
                              "solver" : ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}
                grid = GridSearchCV(LogisticRegression(), param_grid, cv=5, scoring='accuracy')
                grid.fit(_self.X_train, _self.y_train)
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Default Hyperparameters:")
                    st.dataframe(st.session_state.default_params['Logistic Regression'])
                with col2:
                    st.write("Best Hyperparameters Found:")
                    params_df = pd.DataFrame.from_dict(grid.best_params_, orient='index', columns=['Value'])
                    params_df.reset_index(inplace=True)
                    params_df.columns = ['Hyperparameter', 'Value']
                    st.dataframe(params_df)
            with st.spinner("Training Logistic Regression model..."):
                lr = grid.best_estimator_
                lr.fit(_self.X_train, _self.y_train)
                st.success("Logistic Regression model training complete!")
                st.session_state.tuned_models.append(lr)
                st.session_state.tuned_models_dict['Logistic Regression'] = lr

        if "Decision Tree" in models:
            with st.spinner("Finding best parameters for Decision Tree model..."):
                param_grid = {"max_depth": range(5, 31, 5),
                              "min_samples_leaf": [5, 7, 10],
                              "max_leaf_nodes": [5, 10, 15],
                              "min_impurity_decrease": [0.01, 0.1]}
                grid = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=3, scoring='accuracy')
                grid.fit(_self.X_train, _self.y_train)
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Default Hyperparameters:")
                    st.dataframe(st.session_state.default_params['Decision Tree'])
                with col2:
                    st.write("Best Hyperparameters Found:")
                    params_df = pd.DataFrame.from_dict(grid.best_params_, orient='index', columns=['Value'])
                    params_df.reset_index(inplace=True)
                    params_df.columns = ['Hyperparameter', 'Value']
                    st.dataframe(params_df)
            with st.spinner("Training Decision Tree model..."):
                dtree = grid.best_estimator_
                dtree.fit(_self.X_train, _self.y_train)
                st.success("Decision Tree model training complete!")
                st.session_state.tuned_models.append(dtree)
                st.session_state.tuned_models_dict['Decision Tree'] = dtree

        if "Random Forest" in models:
            with st.spinner("Finding best parameters for Random Forest model..."):
                param_grid = {
                    'n_estimators': [100, 300, 500],
                    'max_depth': [5, 10, 20, 40],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4],
                }
                grid = RandomizedSearchCV(RandomForestClassifier(), param_grid, cv=3, scoring='accuracy')
                grid.fit(_self.X_train, _self.y_train)
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Default Hyperparameters:")
                    st.dataframe(st.session_state.default_params['Random Forest'])
                with col2:
                    st.write("Best Hyperparameters Found:")
                    params_df = pd.DataFrame.from_dict(grid.best_params_, orient='index', columns=['Value'])
                    params_df.reset_index(inplace=True)
                    params_df.columns = ['Hyperparameter', 'Value']
                    st.dataframe(params_df)
            with st.spinner("Training Random Forest model..."):
                rf = grid.best_estimator_
                rf.fit(_self.X_train, _self.y_train)
                st.success("Random Forest model training complete!")
                st.session_state.tuned_models.append(rf)
                st.session_state.tuned_models_dict['Random Forest'] = rf

        if "XGBoost" in models:
            with st.spinner("Finding best parameters for XGBoost model..."):
                param_grid = {
                    'n_estimators': [50, 100, 200, 500],
                    'learning_rate': [0.01, 0.1, 0.5],
                    'max_depth': [3, 5, 7, 10],
                    'colsample_bytree': [0.5, 1],
                    'gamma': [0.0, 0.1, 0.2],
                    'min_child_weight': [1, 3, 5]
                }
                grid = GridSearchCV(XGBClassifier(), param_grid, cv=3, scoring='accuracy')
                grid.fit(_self.X_train, _self.y_train)
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Default Hyperparameters:")
                    st.dataframe(st.session_state.default_params['XGBoost'])
                with col2:
                    st.write("Best Hyperparameters Found:")
                    params_df = pd.DataFrame.from_dict(grid.best_params_, orient='index', columns=['Value'])
                    params_df.reset_index(inplace=True)
                    params_df.columns = ['Hyperparameter', 'Value']
                    st.dataframe(params_df)
            with st.spinner("Training XGBoost model..."):
                xgb = grid.best_estimator_
                xgb.fit(_self.X_train, _self.y_train)
                st.success("XGBoost model training complete!")
                st.session_state.tuned_models.append(xgb)
                st.session_state.tuned_models_dict['XGBoost'] = xgb

        if "AdaBoost" in models:
            with st.spinner("Finding best parameters for AdaBoost model..."):
                param_grid = {
                    'n_estimators': [50, 100, 150, 200],
                    'learning_rate': [0.001, 0.01, 0.1, 1.0]
                }
                grid = GridSearchCV(AdaBoostClassifier(), param_grid, cv=3, scoring='accuracy')
                grid.fit(_self.X_train, _self.y_train)
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Default Hyperparameters:")
                    st.dataframe(st.session_state.default_params['AdaBoost'])
                with col2:
                    st.write("Best Hyperparameters Found:")
                    params_df = pd.DataFrame.from_dict(grid.best_params_, orient='index', columns=['Value'])
                    params_df.reset_index(inplace=True)
                    params_df.columns = ['Hyperparameter', 'Value']
                    st.dataframe(params_df)
            with st.spinner("Training AdaBoost model..."):
                ada = grid.best_estimator_
                ada.fit(_self.X_train, _self.y_train)
                st.success("AdaBoost model training complete!")
                st.session_state.tuned_models.append(ada)
                st.session_state.tuned_models_dict['AdaBoost'] = ada

        if "LightGBM" in models:
            with st.spinner("Finding best parameters for LightGBM model..."):
                param_grid = {
                    'n_estimators': [50, 100, 200, 500],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7, 15],
                    'colsample_bytree': [0.3, 0.7],
                }
                grid = GridSearchCV(LGBMClassifier(), param_grid, cv=3, scoring='accuracy')
                grid.fit(_self.X_train, _self.y_train)
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Default Hyperparameters:")
                    st.dataframe(st.session_state.default_params['LightGBM'])
                with col2:
                    st.write("Best Hyperparameters Found:")
                    params_df = pd.DataFrame.from_dict(grid.best_params_, orient='index', columns=['Value'])
                    params_df.reset_index(inplace=True)
                    params_df.columns = ['Hyperparameter', 'Value']
                    st.dataframe(params_df)
            with st.spinner("Training LightGBM model..."):
                lgbm = grid.best_estimator_
                lgbm.fit(_self.X_train, _self.y_train)
                st.success("LightGBM model training complete!")
                st.session_state.tuned_models.append(lgbm)
                st.session_state.tuned_models_dict['LightGBM'] = lgbm