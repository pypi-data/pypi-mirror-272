from ..utils.streamlit_utils import st
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

class ModelTrainingWithUserParams:
    def __init__(_self, X_train, y_train):
        _self.X_train = X_train
        _self.y_train = y_train

    @st.cache_data(experimental_allow_widgets=True)
    def get_user_params(_self, models):
        user_params = {}
        with st.container(border = True):
            if "Logistic Regression" in models:
                penalty = st.selectbox("Penalty", ["l1", "l2", "elasticnet"])
                C = st.slider("C", 0.1, 10.0, 1.0, 0.1)
                solver = st.selectbox("Solver", ["newton-cg", "lbfgs", "liblinear", "sag", "saga"])
                user_params["Logistic Regression"] = {"penalty": penalty, "C": C, "solver": solver}

            if "Decision Tree" in models:
                max_depth = st.slider("Max Depth", 5, 30, 10, 5)
                min_samples_leaf = st.slider("Min Samples Leaf", 1, 10, 5, 1)
                max_leaf_nodes = st.slider("Max Leaf Nodes", 5, 20, 15, 5)
                user_params["Decision Tree"] = {"max_depth": max_depth, "min_samples_leaf": min_samples_leaf, "max_leaf_nodes": max_leaf_nodes}

            if "Random Forest" in models:
                n_estimators = st.slider("Number of Estimators", 100, 1000, 200, 100)
                max_depth = st.slider("Max Depth", 5, 50, 15, 5)
                min_samples_split = st.slider("Min Samples Split", 2, 10, 5, 1)
                min_samples_leaf = st.slider("Min Samples Leaf", 1, 5, 1, 1)
                user_params["Random Forest"] = {"n_estimators": n_estimators, "max_depth": max_depth, "min_samples_split": min_samples_split, "min_samples_leaf": min_samples_leaf}

            if "XGBoost" in models:
                n_estimators = st.slider("Number of Estimators", 50, 500, 100, 50)
                learning_rate = st.slider("Learning Rate", 0.01, 0.5, 0.1, 0.01)
                max_depth = st.slider("Max Depth", 3, 10, 5, 1)
                colsample_bytree = st.slider("Column Sample by Tree", 0.5, 1.0, 1.0, 0.1)
                gamma = st.slider("Gamma", 0.0, 0.5, 0.0, 0.1)
                min_child_weight = st.slider("Min Child Weight", 1, 5, 1, 1)
                user_params["XGBoost"] = {"n_estimators": n_estimators, "learning_rate": learning_rate, "max_depth": max_depth, "colsample_bytree": colsample_bytree, "gamma": gamma, "min_child_weight": min_child_weight}

            if "AdaBoost" in models:
                n_estimators = st.slider("Number of Estimators", 50, 200, 100, 50)
                learning_rate = st.slider("Learning Rate", 0.001, 1.0, 0.01, 0.001)
                user_params["AdaBoost"] = {"n_estimators": n_estimators, "learning_rate": learning_rate}

            if "LightGBM" in models:
                n_estimators = st.slider("Number of Estimators", 50, 500, 200, 50)
                learning_rate = st.slider("Learning Rate", 0.01, 0.2, 0.1, 0.01)
                max_depth = st.slider("Max Depth", 3, 15, 7, 1)
                colsample_bytree = st.slider("Column Sample by Tree", 0.3, 0.7, 0.7, 0.1)
                user_params["LightGBM"] = {"n_estimators": n_estimators, "learning_rate": learning_rate, "max_depth": max_depth, "colsample_bytree": colsample_bytree}
        return user_params

    @st.cache_data(show_spinner="Training Models with Custom Parameters...")
    def train_with_user_params(_self, models, user_params):
        if "Logistic Regression" in models:
            with st.spinner("Training Logistic Regression model..."):
                lr = LogisticRegression(**user_params["Logistic Regression"])
                lr.fit(_self.X_train, _self.y_train)
                st.success("Logistic Regression model training complete!")
                st.session_state.trained_models_custom.append(lr)
                st.session_state.trained_models_custom_dict['Logistic Regression'] = lr

        if "Decision Tree" in models:
            with st.spinner("Training Decision Tree model..."):
                dtree = DecisionTreeClassifier(**user_params["Decision Tree"])
                dtree.fit(_self.X_train, _self.y_train)
                st.success("Decision Tree model training complete!")
                st.session_state.trained_models_custom.append(dtree)
                st.session_state.trained_models_custom_dict['Decision Tree'] = dtree

        if "Random Forest" in models:
            with st.spinner("Training Random Forest model..."):
                rf = RandomForestClassifier(**user_params["Random Forest"])
                rf.fit(_self.X_train, _self.y_train)
                st.success("Random Forest model training complete!")
                st.session_state.trained_models_custom.append(rf)
                st.session_state.trained_models_custom_dict['Random Forest'] = rf

        if "XGBoost" in models:
            with st.spinner("Training XGBoost model..."):
                xgb = XGBClassifier(**user_params["XGBoost"])
                xgb.fit(_self.X_train, _self.y_train)
                st.success("XGBoost model training complete!")
                st.session_state.trained_models_custom.append(xgb)
                st.session_state.trained_models_custom_dict['XGBoost'] = xgb

        if "AdaBoost" in models:
            with st.spinner("Training AdaBoost model..."):
                ada = AdaBoostClassifier(**user_params["AdaBoost"])
                ada.fit(_self.X_train, _self.y_train)
                st.success("AdaBoost model training complete!")
                st.session_state.trained_models_custom.append(ada)
                st.session_state.trained_models_custom_dict['AdaBoost'] = ada

        if "LightGBM" in models:
            with st.spinner("Training LightGBM model..."):
                lgbm = LGBMClassifier(**user_params["LightGBM"])
                lgbm.fit(_self.X_train, _self.y_train)
                st.success("LightGBM model training complete!")
                st.session_state.trained_models_custom.append(lgbm)
                st.session_state.trained_models_custom_dict['LightGBM'] = lgbm