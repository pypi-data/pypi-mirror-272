from streamlit_extras.colored_header import colored_header
import pandas as pd
import plotly.express as px
from scipy.stats import skew
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from .utils.streamlit_utils import hide_icons, remove_whitespaces, st
from .utils.print_utils import print_shape
from streamlit_modal import Modal
import pickle
import os, warnings, zipfile

from .modules.data_input import DataInput
from .modules.data_summarization import DataSummarization
from .modules.data_cleaning import DataCleaning
from .modules.data_visualization import DataVisualization
from .modules.data_woeiv import DataWOEIV
from .modules.data_preprocessing import DataPreprocessing
from .modules.model_training import ModelTraining
from .modules.model_evaluation import ModelEvaluation
from .modules.hyperparameter_tuning import HyperparameterTuning
from .modules.train_user_params import ModelTrainingWithUserParams
from .launcher import launch_streamlit

warnings.filterwarnings("ignore")

plot_colors = px.colors.sequential.Blues[::-2]

st.set_page_config(layout="wide")
hide_icons()
remove_whitespaces()

# Title of the Web App
colored_header(label="Automated Credit Underwriting Web Application", description="", color_name="light-blue-70")

# Info displayed in the sidebar
sidebar = st.sidebar
with sidebar:
    #st.image('automlapp\logo.png', use_column_width='always')
    st.markdown("""
        <div style="padding-left: 40px; padding-top: 5px; border-radius: 5px;">
            <h4 style="color: white;">1. Upload Dataset</h4>
            <h4 style="color: white;">2. View Dataset Summary</h4>
            <h4 style="color: white;">3. Data Visualization and EDA</h4>
            <h4 style="color: white;">4. Data Cleaning</h4>
            <h4 style="color: white;">5. WOE & IV Analysis</h4>
            <h4 style="color: white;">6. Data Preprocessing</h4>
            <h4 style="color: white;">7. Model Training</h4>
            <h4 style="color: white;">8. Model Evaluation</h4>
            <h4 style="color: white;">9. Download Models and Results</h4>
        </div>
    """, unsafe_allow_html=True)

# Create a modal
modal = Modal(key="Info Key", title="Automated Credit Underwriting Web Application")

# Create a button at the bottom of the sidebar to open the modal
open_modal = sidebar.button('About The App', type="primary", use_container_width=True)

if open_modal:
    with modal.container():
        st.markdown("""
        This AutoML Web App revolutionizes the credit underwriting process by automating critical steps, including data preprocessing, model fitting, and hyperparameter tuning, to ensure accurate risk assessments. Designed to streamline the workflow, it significantly enhances efficiency and precision in lending risk management for both individuals and businesses.

        **Features:**
        - **Streamlined Credit Underwriting:** Traditionally, credit underwriting has been a meticulous process essential for evaluating lending risks. This app simplifies these complexities, transforming how risk assessments are conducted.
        - **Overcoming Manual Constraints:** The manual fitting of models for credit underwriting is both time-consuming and prone to human error, potentially leading to suboptimal algorithm selection and overlooked risks. Our app addresses these challenges by automating model selection.
        - **Efficient Model Selection:** The AutoML Web App stands out by enabling the efficient selection of machine learning models tailored to specific tasks. It sifts through a targeted set of algorithms to find the best fit, balancing automation with user control to achieve optimal outcomes.
        - **No-Code Solution:** With the goal of democratizing technology, the app eliminates the need for intricate coding. It offers a user-friendly interface where complex underwriting tasks can be executed with just a few clicks, making sophisticated data analysis accessible to all.
        - **Precision and Efficiency:** By offering a carefully curated selection of options at each stage of the underwriting process, the app ensures that both efficiency and precision are not just promised but delivered. This meticulous approach guarantees that every dataset is handled with the optimal blend of speed and accuracy.

        **Developed By**: [Shivam Nikam](mailto:shivam.nikam@think360.ai) & [Aditya Jikamade](mailto:aditya.jikamade@think360.ai)
        """)

#Initializing the dataframe from session state
if 'df' not in st.session_state:
    st.session_state.df = None
else:
    df = st.session_state.df

train_df = None
if 'train_df' not in st.session_state:
    st.session_state.train_df = train_df
else:
    train_df = st.session_state.train_df

test_df = None
if 'test_df' not in st.session_state:
    st.session_state.test_df = test_df
else:
    test_df = st.session_state.test_df

st.session_state.eval, st.session_state.tuned = False, False

# ---------------------------------
# Upload dataset section
with st.expander("**Upload Data**", expanded = True):        
    option = st.radio('How would you like to upload your data?', ('Upload one file for the entire dataset', 'Upload separate training and testing data'))
    if option == 'Upload one file for the entire dataset':
        uploaded_file = st.file_uploader("**Upload a file for your dataset**", type = ['csv', 'tsv', 'txt', 'xlsx', 'zip'], accept_multiple_files = False, help = "While uploading zipped archive, ensure that it has a single CSV file")
        if uploaded_file is not None:
            data_input = DataInput(uploaded_file)
            df = data_input.upload_dataset()            

            st.markdown('---')
            st.subheader("Target Variable")
            target_feat_selection = st.selectbox(label = 'Select the target variable of the entered dataset:', options = list(df.columns), help = 'Select the target variable of the entered dataset:')

            if target_feat_selection:
                st.subheader("Target Variable Value Counts")
                st.markdown("""
                    <style>
                        table {margin-left: auto; margin-right: auto;}
                        table th {text-align: center !important;}
                        table td {text-align: center !important;}
                    </style>
                    """, unsafe_allow_html=True)
                st.table(pd.DataFrame({"Count": df[target_feat_selection].value_counts(), "Percentage": df[target_feat_selection].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'}))

            st.session_state.df = df
            st.session_state.target = target_feat_selection

    elif option == 'Upload separate training and testing data':
        # Train data
        train_file = st.file_uploader("**Upload a file for your training set**", type = ['csv', 'tsv', 'txt', 'xlsx', 'zip'], accept_multiple_files = False, help = "While uploading zipped archive, ensure that it has a single CSV file")
        if train_file is not None:
            data_input = DataInput(train_file, 'train')
            train_df = data_input.upload_dataset()

        # Test data
        test_file = st.file_uploader("**Upload a file for your testing set**", type = ['csv', 'tsv', 'txt', 'xlsx', 'zip'], accept_multiple_files = False, help = "While uploading zipped archive, ensure that it has a single CSV file")
        if test_file is not None:
            data_input = DataInput(test_file, 'test')
            test_df = data_input.upload_dataset()
        
        if train_df is not None and test_df is not None:
            st.markdown('---')
            st.subheader("Target Variable")
            target_feat_selection = st.selectbox(label = 'Select the target variable of the entered dataset:', options = list(train_df.columns), help = 'Select the target variable of the entered dataset:')

            if target_feat_selection:
                st.subheader("Target Variable Value Counts")
                st.markdown("""
                    <style>
                    table {margin-left: auto; margin-right: auto;}
                    table th {text-align: center !important;}
                    table td {text-align: center !important;}
                    </style>
                    """, unsafe_allow_html=True)
                st.table(pd.DataFrame({"Count": train_df[target_feat_selection].value_counts(), "Percentage": train_df[target_feat_selection].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'}))

            st.session_state.train_df, st.session_state.test_df = train_df, test_df
            st.session_state.target = target_feat_selection

# ---------------------------------
# Data Summarization
with st.expander("**Data Summary**"):
    if option == 'Upload one file for the entire dataset':
        if "df" in st.session_state:
            df = st.session_state.df

            if df is not None:
                data_summarize = DataSummarization(df)
                data_summarize.summarize()

    elif option == 'Upload separate training and testing data':
        if "train_df" in st.session_state and "test_df" in st.session_state:
            train_df, test_df = st.session_state.train_df, st.session_state.test_df

            if train_df is not None and test_df is not None:
                st.subheader('Train Set')
                data_summarize = DataSummarization(train_df)
                data_summarize.summarize()
        
                st.markdown("---")
                st.subheader('Test Set')
                data_summarize = DataSummarization(test_df)
                data_summarize.summarize()

# ---------------------------------
# Data Cleaning
with st.expander("**Data Cleaning**"):
    if option == 'Upload one file for the entire dataset':
        if "cleaned_df" in st.session_state:
            df = st.session_state.cleaned_df
        elif "df" in st.session_state:
            df = st.session_state.df

        if df is not None:
            data_cleaning = DataCleaning(df)
            target = st.session_state.target
            st.subheader("Select Cleaning Options")
            st.markdown("---")
            st.subheader("Drop Missing Values, Duplicates or Specific Columns")
            drop_na0 = st.checkbox("Drop rows with missing values", help="This will drop the rows containing missing values in the selected subset of columns")
            if drop_na0:
                cols_select_drop = st.multiselect("Select columns to drop missing values from:", df.drop(target, axis = 1).columns,key="I")
            drop_na1 = st.checkbox("Drop columns with all values missing", help="This will drop the columns which contain all missing values")
            drop_duplicates = st.checkbox("Drop rows with all values duplicated", help = "This will drop rows with all values duplicated while retaining first occurrence")
            
            st.markdown("---")
            st.subheader("Treat Outliers")
            treat_outliers = st.checkbox("Drop, Cap or Impute Outliers", help="Drop Outliers or Cap or Impute them with Mean, Median or Mode")
            if treat_outliers:
                lower, upper = st.slider("Select threshold", min_value=0, max_value=100, step=1, value=(5, 95))
                # Detecting Outliers
                outliers = data_cleaning.detect_outliers(lower, upper)
                st.write("Outliers detected: ")
                st.dataframe(outliers)
                outlier_cols = st.multiselect("Select columns to handle outliers in:", df.drop(target, axis = 1).columns, key="Outlier")
                outlier_tech = st.selectbox("Select outlier handling technique", ["Remove Outliers", "Cap Outliers", "Impute Outliers"])

            st.markdown("---")
            st.subheader("Impute Missing Values or Special Values")
            impute_missing_ch = st.checkbox("Impute Missing Values with Mean, Median or Mode", help="Impute missing values in selected subset of columns with Mean, Median or Mode")
            if impute_missing_ch:
                col1, col2 = st.columns(2)
                with col1:
                    cols_select_missing = st.multiselect("Select columns to impute missing values in:", df.drop(target, axis = 1).columns,key="I1")
                with col2:
                    imp_method_missing = st.selectbox("Select Imputation Method", ["Mean", "Median", "Mode"],key="IS1")

            impute_special_ch = st.checkbox("Impute Special Values with Mean, Median or Mode", help="Impute special values in particular columns selected with Mean, Median or Mode") 
            if impute_special_ch:
                col1, col2 = st.columns(2)
                with col1:
                    cols_select_impute = st.multiselect("Select columns to impute special values in:", df.drop(target, axis = 1).columns,key="I3")
                with col2:
                    imp_method_spec = st.selectbox("Select Imputation Method", ["Mean", "Median", "Mode"],key="IS2")
                special_vals_imp = st.text_input("Enter special values :point_down: (Comma-separated)", key="placeholder")

            replace_special_ch = st.checkbox("Replace Special Values with Custom Value", help="Replace all special values with the new entered value")
            if replace_special_ch:
                col1, col2 = st.columns(2)
                with col1:
                    cols_select_replace = st.multiselect("Select columns to replace special values in:", df.drop(target, axis=1).columns, key="I4")
                with col2:
                    special_vals_rep = st.text_input("Enter special values :point_down: (Comma-separated)", key="placeholder1")
                replace_with = st.text_input("Enter value to replace with")

            st.markdown("---")
            st.subheader("Exclude Certain Features")
            drop_columns = st.checkbox("Drop specific columns", help = "Exclude certain features from analysis")
            if drop_columns:
                columns = st.multiselect("Select columns to drop", df.drop(target, axis = 1).columns)
            st.markdown("---")
            
            if "clicked_clean" not in st.session_state:
                st.session_state.clicked_clean = False
            if st.button("Apply data cleaning"):
                if drop_na0:
                    df = df.dropna(axis=0, subset = cols_select_drop)
                    data_cleaning.df = df
                if drop_na1:
                    df = df.dropna(axis=1, how = 'all')
                    data_cleaning.df = df
                if drop_duplicates:
                    df = df.drop_duplicates()
                    data_cleaning.df = df
                if treat_outliers:
                    df = data_cleaning.treat_outliers(lower, upper, outlier_cols, outlier_tech)
                    data_cleaning.df = df
                if impute_missing_ch:
                    df = data_cleaning.impute_missing(cols_select_missing, imp_method_missing)
                    data_cleaning.df = df
                if impute_special_ch:
                    df = data_cleaning.impute_special(cols_select_impute, imp_method_spec, special_vals_imp)
                    data_cleaning.df = df
                if replace_special_ch:
                    df = data_cleaning.replace_special(cols_select_replace, special_vals_rep, replace_with)
                    data_cleaning.df = df
                if drop_columns:
                    df = df.drop(columns, axis=1)
                    data_cleaning.df = df
                st.session_state.cleaned_df = data_cleaning.df
                st.session_state.clicked_clean = True
                print_shape(st.session_state.cleaned_df)
                st.write(f"Total number of missing values remaining: :red[{data_cleaning.df.isna().sum().sum()}]")

            if st.button("Summarize Cleaned Dataset"):
                if st.session_state.clicked_clean:
                    st.subheader("Cleaned Dataset")
                    print_shape(st.session_state.cleaned_df)
                    st.write(f"Total number of missing values remaining: :red[{st.session_state.cleaned_df.isna().sum().sum()}]")

                if "cleaned_df" in st.session_state:
                    st.subheader("Summary of Cleaned Dataset")
                    data_summarize = DataSummarization(st.session_state.cleaned_df)
                    data_summarize.summarize()
                else:
                    st.error("Please clean the dataset first!")
    
    elif option == 'Upload separate training and testing data':
        if "cleaned_train_df" in st.session_state and "cleaned_test_df" in st.session_state:
            train_df, test_df = st.session_state.cleaned_train_df, st.session_state.cleaned_test_df
        elif "train_df" in st.session_state and "test_df" in st.session_state:
            train_df, test_df = st.session_state.train_df, st.session_state.test_df

        if train_df is not None and test_df is not None:
            data_cleaning_train, data_cleaning_test = DataCleaning(train_df), DataCleaning(test_df)
            target = st.session_state.target
            st.subheader("Select Cleaning Options")
            st.markdown("---")
            st.subheader("Drop Missing Values, Duplicates or Specific Columns")
            drop_na0 = st.checkbox("Drop rows with missing values", help="This will drop the rows containing missing values in the selected subset of columns")
            if drop_na0:
                cols_select_drop = st.multiselect("Select columns to drop missing values from:", train_df.drop(target, axis = 1).columns,key="II")

            drop_na1 = st.checkbox("Drop columns with all values missing", help="This will drop the columns which contain all missing values")
            drop_duplicates = st.checkbox("Drop rows with all values duplicated", help = "This will drop rows with all values duplicated while retaining first occurrence")

            st.markdown("---")
            st.subheader("Treat Outliers")
            treat_outliers = st.checkbox("Drop, Cap or Impute Outliers", help="Drop Outliers or Cap or Impute them with Mean, Median or Mode")
            if treat_outliers:
                lower, upper = st.slider("Select threshold", min_value=0, max_value=100, step=1, value=(5, 95))
                
                # Detecting Outliers
                outliers = data_cleaning_train.detect_outliers(lower, upper)
                st.write("Outliers detected: ")
                st.dataframe(outliers)
                outlier_cols = st.multiselect("Select columns to handle outliers in:", train_df.drop(target, axis = 1).columns, key="outlier")
                outlier_tech = st.selectbox("Select outlier handling technique", ["Remove Outliers", "Cap Outliers", "Impute Outliers"])

            st.markdown("---")
            st.subheader("Impute Missing Values or Special Values")
            impute_missing_ch = st.checkbox("Impute Missing Values with Mean, Median or Mode", help="Impute missing values in selected subset of columns with Mean, Median or Mode")
            if impute_missing_ch:
                col1, col2 = st.columns(2)
                with col1:
                    cols_select_missing = st.multiselect("Select columns to impute missing values in:", train_df.drop(target, axis = 1).columns,key="II1")
                with col2:
                    imp_method_missing = st.selectbox("Select Imputation Method", ["Mean", "Median", "Mode"],key="IIS1")

            impute_special_ch = st.checkbox("Impute Special Values with Mean, Median or Mode", help="Impute special values in particular columns selected with Mean, Median or Mode") 
            if impute_special_ch:
                col1, col2 = st.columns(2)
                with col1:
                    cols_select_impute = st.multiselect("Select columns to impute special values in:", train_df.drop(target, axis = 1).columns,key="II2")
                with col2:
                    imp_method_spec = st.selectbox("Select Imputation Method", ["Mean", "Median", "Mode"],key="IIS2")
                special_vals_imp = st.text_input("Enter special values :point_down: (Comma-separated)", key="placeholder")

            replace_special_ch = st.checkbox("Replace Special Values with Custom Value", help="Replace all special values with the new entered value")
            if replace_special_ch:
                col1, col2 = st.columns(2)
                with col1:
                    cols_select_replace = st.multiselect("Select columns to replace special values in:", train_df.drop(target, axis=1).columns, key="II3")
                with col2:
                    special_vals_rep = st.text_input("Enter special values :point_down: (Comma-separated)", key="placeholder1")
                replace_with = st.text_input("Enter value to replace with")

            st.markdown("---")
            st.subheader("Exclude Certain Features")
            drop_columns = st.checkbox("Drop specific columns", help = "Exclude certain features from analysis")
            if drop_columns:
                columns = st.multiselect("Select columns to drop", train_df.drop(target, axis = 1).columns)
            st.markdown("---")

            if "clicked_clean" not in st.session_state:
                st.session_state.clicked_clean = False
            if st.button("Apply data cleaning"):
                if drop_na0:
                    train_df, test_df = train_df.dropna(axis=0, subset=cols_select_drop), test_df.dropna(axis=0, subset=cols_select_drop)
                    data_cleaning_train.df, data_cleaning_test.df = train_df, test_df
                if drop_na1:
                    train_df, test_df = train_df.dropna(axis=1, how = 'all'), test_df.dropna(axis=1, how = 'all')
                    data_cleaning_train.df, data_cleaning_test.df = train_df, test_df
                if drop_duplicates:
                    train_df, test_df = train_df.drop_duplicates(), test_df.drop_duplicates()
                    data_cleaning_train.df, data_cleaning_test.df = train_df, test_df
                if treat_outliers:
                    train_df, test_df = data_cleaning_train.treat_outliers(lower, upper,outlier_cols, outlier_tech), data_cleaning_test.treat_outliers(lower, upper, outlier_cols, outlier_tech)
                    data_cleaning_train.df, data_cleaning_test.df = train_df, test_df
                if impute_missing_ch:
                    train_df, test_df = data_cleaning_train.impute_missing(cols_select_missing, imp_method_missing), data_cleaning_test.impute_missing(cols_select_missing, imp_method_missing)
                    data_cleaning_train.df, data_cleaning_test.df = train_df, test_df
                if impute_special_ch:
                    train_df, test_df = data_cleaning_train.impute_special(cols_select_impute, imp_method_spec, special_vals_imp), data_cleaning_test.impute_special(cols_select_impute, imp_method_spec, special_vals_imp)
                    data_cleaning_train.df, data_cleaning_test.df = train_df, test_df
                if replace_special_ch:
                    train_df, test_df = data_cleaning_train.replace_special(cols_select_replace, special_vals_rep, replace_with), data_cleaning_test.replace_special(cols_select_replace, special_vals_rep, replace_with)
                    data_cleaning_train.df, data_cleaning_test.df = train_df, test_df
                if drop_columns:
                    train_df, test_df = train_df.drop(columns, axis=1), test_df.drop(columns, axis=1)
                    data_cleaning_train.df, data_cleaning_test.df = train_df, test_df
                st.session_state.cleaned_train_df, st.session_state.cleaned_test_df = data_cleaning_train.df, data_cleaning_test.df
                st.session_state.clicked_clean = True
                print_shape(train_df)
                st.write(f"Total number of missing values remaining: :red[{train_df.isna().sum().sum()}]")

                print_shape(test_df)
                st.write(f"Total number of missing values remaining: :red[{test_df.isna().sum().sum()}]")
            
            if st.button("Summarize Cleaned Dataset"):
                if st.session_state.clicked_clean:
                    st.subheader("Cleaned Dataset")
                    print_shape(st.session_state.cleaned_train_df)
                    st.write(f"Total number of missing values remaining: :red[{st.session_state.cleaned_train_df.isna().sum().sum()}]")

                if "cleaned_train_df" in st.session_state and "cleaned_test_df" in st.session_state:
                    st.subheader("Summary of Cleaned Dataset")
                    data_summarize = DataSummarization(st.session_state.cleaned_train_df)
                    data_summarize.summarize()
                else:
                    st.error("Please clean the dataset first!")

# ---------------------------------
# Data Visualization
with st.expander("**Data Visualization**"):
    if option == 'Upload one file for the entire dataset':
        # Loading the dataset from session state
        if "cleaned_df" in st.session_state:
            df = st.session_state.cleaned_df
        elif "df" in st.session_state:
            df = st.session_state.df
        # Creating the plots
        if df is not None:
            data_visualization = DataVisualization(df)
            data_visualization.visualize()

    elif option == 'Upload separate training and testing data':
        if "cleaned_train_df" in st.session_state:
            train_df = st.session_state.cleaned_train_df
        elif "train_df" in st.session_state:
            train_df = st.session_state.train_df
        # Creating the plots
        if train_df is not None:
            data_visualization = DataVisualization(train_df)
            data_visualization.visualize()

# ---------------------------------
# WOE and IV
with st.expander('**Perform WOE and IV Analysis**'):
    if option == "Upload one file for the entire dataset":
        if "cleaned_df" in st.session_state:
            df = st.session_state.cleaned_df
        elif "df" in st.session_state:
            df = st.session_state.df

        if df is not None:
            data_woeiv = DataWOEIV(df)
            data_woeiv.apply_woe_iv()
            data_woeiv.display_chart()
            cols_to_drop = st.multiselect("Select columns to drop (if any) based on WOE IV analysis", df.drop(target, axis = 1).columns, default = None, key = "WOEIV1")
            drop_button = st.button("Drop Columns")
            if cols_to_drop and drop_button:
                df = df.drop(cols_to_drop, axis=1)
                data_woeiv.df = df
                st.session_state.cleaned_df = data_woeiv.df
                print_shape(df)

    elif option == "Upload separate training and testing data":
        if "cleaned_train_df" in st.session_state and "cleaned_test_df" in st.session_state:
            train_df, test_df = st.session_state.cleaned_train_df, st.session_state.cleaned_test_df
        elif "train_df" in st.session_state and "test_df" in st.session_state:
            train_df, test_df = st.session_state.train_df, st.session_state.test_df

        if train_df is not None and test_df is not None:
            data_woeiv_train, data_woeiv_test = DataWOEIV(train_df), DataWOEIV(test_df)
            data_woeiv_train.apply_woe_iv()
            data_woeiv_train.display_chart()
            cols_to_drop = st.multiselect("Select columns to drop (if any) based on WOE IV analysis", train_df.drop(target, axis = 1).columns, default = None, key = "WOEIV2")
            drop_button = st.button("Drop Columns")
            if cols_to_drop and drop_button:
                train_df, test_df = train_df.drop(cols_to_drop, axis=1), test_df.drop(cols_to_drop, axis = 1)
                data_woeiv_train.df, data_woeiv_test.df = train_df, test_df
                st.session_state.cleaned_train_df, st.session_state.cleaned_test_df = data_woeiv_train.df, data_woeiv_test.df
                st.subheader("Train Set")
                print_shape(train_df)

                st.subheader("Test Set")
                print_shape(test_df)

# ---------------------------------
# Data Preprocessing
with st.expander("**Data Preprocessing**"):
    if option == 'Upload one file for the entire dataset':
        # Loading the dataset from session state
        if "cleaned_df" in st.session_state:
            df = st.session_state.cleaned_df
        elif "df" in st.session_state:
            df = st.session_state.df

        if df is not None:
            target = st.session_state.target
            data_preprocess = DataPreprocessing(df, target)

            st.subheader("Select preprocessing options")
            balance = st.checkbox("Balance Dataset", help="Remove imbalance in the dataset by using either Oversampling, Undersampling or a combination of both")
            if balance:
                container = st.container(border = True)
                container.write("**Important Notes:**\n1) **Under Sampling:** Balance the dataset by reducing the size of the abundant class. This method is used when the quantity of data is sufficient.\n2) **Over Sampling:** Over-sampling is used when the amount of data collected is insufficient. A popular over-sampling technique is SMOTE (Synthetic Minority Over-sampling Technique), which creates synthetic samples by randomly sampling the characteristics from occurrences in the minority class.\n3) **Combine:** Combine over- and under-sampling using SMOTE and Edited Nearest Neighbours.")
                sample_tech = st.selectbox("Select sampling technique", ["Over Sampling", "Under Sampling", "Combined"])
                sample_st = st.slider("Select Sampling Strategy", min_value=0.0, max_value=1.0, step=0.1, value=0.5, help="desired ratio of the number of samples in the minority class over the number of samples in the majority class after resampling")

            transforms = st.checkbox("Apply Transformations", help="Transform the data to handle skew and improve model performance")
            if transforms:
                container = st.container(border = True)
                container.write("**Rules of Thumb:**\n1) For skewness values between -0.5 and 0.5, the data exhibits approximate symmetry and no transformations are required.\n2) Skewness values within the range of -1 and -0.5 (negative skewed) or 0.5 and 1(positive skewed) indicate slightly skewed data distributions.\n3) Data with skewness values less than -1 (negative skewed) or greater than 1 (positive skewed) are considered highly skewed. In this case, logarithmic, square root, or reciprocal transformations can be used to reduce skewness.")
                skew_values = df.apply(lambda x: skew(x))
                S = st.slider("Select Skewness Threshold (S)", min_value=0.0, max_value=10.0, step=0.1, value=3.0)
                high_skew_columns = skew_values[skew_values > S]

                st.subheader("High Skew Columns and Skew Values")
                if not high_skew_columns.empty:
                    st.write("Skew Values:")
                    st.write(high_skew_columns)
                else:
                    st.info("No columns have skewness greater than given Threshold.")
            
                transform_method = st.radio("Select Transformation Method", ['Log Transformation', 'Box-Cox Transformation', 'Square Root Transformation', 'Reciprocal Transformation'])

            scale_options = st.checkbox("Apply Scaling", help="Scale the data to standardize its range")
            if scale_options:
                scale_method = st.radio("Select Scaling Method", ['Standard Scaling', 'Min-Max Scaling', 'Robust Scaling'])

            pca = st.checkbox("Apply PCA", help="Reduce the dimensionality of the data using Principal Component Analysis")
            if pca:
                container = st.container(border = True)
                container.write("**Important Notes:**\n1) Principal component analysis (PCA) is a powerful technique for reducing the dimensionality of multivariate data sets, such as images, text, or surveys. PCA transforms the original variables into new ones, called principal components, that capture the maximum amount of variation in the data.\n2) Dimensionality reduction is useful for several reasons as below:")
                
                container.write("&nbsp;&nbsp;&nbsp;&nbsp;1) It can help you simplify and visualize your data, by removing noise and irrelevant features.")
                container.write("&nbsp;&nbsp;&nbsp;&nbsp;2) It can improve the performance and efficiency of your machine learning models, by reducing the computational complexity and the risk of overfitting.")
                container.write("&nbsp;&nbsp;&nbsp;&nbsp;3) It can help you discover and interpret the underlying patterns and structures in your data, by revealing the most important factors or dimensions.")

                container.write("3) To select the best number of components, you can use cross-validation to evaluate the performance of your machine learning model on unseen data by splitting your data into training and testing sets. You can choose the number of principal components that maximizes or optimizes your desired metric. If interpretability is important for your task, you might want to choose a smaller number of components, which can offer a simpler and more understandable description of your data")

                n_components = st.number_input("Number of PCA components", min_value=1, max_value=min(df.shape[0], df.shape[1]), value=2)

            if st.button("Apply Data Preprocessing"):
                if balance:
                    df = data_preprocess.balance_dataset(sample_tech, sample_st)
                    data_preprocess.df = df

                if transforms:
                    df = data_preprocess.transform_columns(method=transform_method, S=S)
                    data_preprocess.df = df

                if scale_options:
                    df = data_preprocess.scale_dataset(scale_method)
                    data_preprocess.df = df

                if pca:
                    try:
                        pca = PCA(n_components=n_components)
                        X, y = df.drop(target, axis=1), df[target]
                        df = pca.fit_transform(X)
                        df = pd.DataFrame(df)
                        df[target] = y
                    except Exception as e:
                        if df.isna().sum().sum() > 0:
                            st.error("Your dataset contains NaN values. Please remove them in the Data Cleaning section and try again")
                        else:
                            st.error(e)
                    data_preprocess.df = df

                st.session_state.prepro_df = data_preprocess.df
                print_shape(df)

    elif option == 'Upload separate training and testing data':
        if "cleaned_train_df" in st.session_state and "cleaned_test_df" in st.session_state:
            train_df, test_df = st.session_state.cleaned_train_df, st.session_state.cleaned_test_df
        elif "train_df" in st.session_state and "test_df" in st.session_state:
            train_df, test_df = st.session_state.train_df, st.session_state.test_df

        if train_df is not None and test_df is not None:
            target = st.session_state.target
            data_preprocess_train, data_preprocess_test = DataPreprocessing(train_df, target), DataPreprocessing(test_df, target)

            st.subheader("Select preprocessing options")
            balance = st.checkbox("Balance your dataset", help="Remove imbalance in the dataset by using either Oversampling, Undersampling or a combination of both")
            if balance:
                container = st.container(border = True)
                container.write("**Important Notes:**\n1) **Under Sampling:** Balance the dataset by reducing the size of the abundant class. This method is used when the quantity of data is sufficient.\n2) **Over Sampling:** Over-sampling is used when the amount of data collected is insufficient. A popular over-sampling technique is SMOTE (Synthetic Minority Over-sampling Technique), which creates synthetic samples by randomly sampling the characteristics from occurrences in the minority class.\n3) **Combine:** Combine over- and under-sampling using SMOTE and Edited Nearest Neighbours.")
                sample_tech = st.selectbox("Select sampling technique", ["Over Sampling", "Under Sampling", "Combined"])
                sample_st = st.slider("Select Sampling Strategy", min_value=0.0, max_value=1.0, step=0.1, value=0.5, help="desired ratio of the number of samples in the minority class over the number of samples in the majority class after resampling")

            transforms = st.checkbox("Apply Transformations", help="Transform the data to handle skew and improve model performance")
            if transforms:
                container = st.container(border = True)
                container.write("**Rules of Thumb:**\n1) For skewness values between -0.5 and 0.5, the data exhibits approximate symmetry and no transformations are required.\n2) Skewness values within the range of -1 and -0.5 (negative skewed) or 0.5 and 1(positive skewed) indicate slightly skewed data distributions.\n3) Data with skewness values less than -1 (negative skewed) or greater than 1 (positive skewed) are considered highly skewed. In this case, logarithmic, square root, or reciprocal transformations can be used to reduce skewness.")
                skew_values = train_df.apply(lambda x: skew(x))
                S = st.slider("Select Skewness Threshold (S)", min_value=0.0, max_value=10.0, step=0.1, value=3.0)
                high_skew_columns = skew_values[skew_values > S]

                st.subheader("High Skew Columns and Skew Values")
                if not high_skew_columns.empty:
                    st.write("Skew Values:")
                    st.write(high_skew_columns)
                else:
                    st.info("No columns have skewness greater than given Threshold.")
                transform_method = st.radio("Select Transformation Method", ['Log Transformation', 'Box-Cox Transformation', 'Square Root Transformation', 'Reciprocal Transformation'])

            scale_options = st.checkbox("Apply Scaling", help="Scale the data to standardize its range")
            if scale_options:
                scale_method = st.radio("Select Scaling Method", ['Standard Scaling', 'Min-Max Scaling', 'Robust Scaling'])

            pca = st.checkbox("Apply PCA", help="Reduce the dimensionality of the data using Principal Component Analysis")
            if pca:
                container = st.container(border = True)
                container.write("**Important Notes:**\n1) Principal component analysis (PCA) is a powerful technique for reducing the dimensionality of multivariate data sets, such as images, text, or surveys. PCA transforms the original variables into new ones, called principal components, that capture the maximum amount of variation in the data.\n2) Dimensionality reduction is useful for several reasons as below:")
                
                container.write("&nbsp;&nbsp;&nbsp;&nbsp;1) It can help you simplify and visualize your data, by removing noise and irrelevant features.")
                container.write("&nbsp;&nbsp;&nbsp;&nbsp;2) It can improve the performance and efficiency of your machine learning models, by reducing the computational complexity and the risk of overfitting.")
                container.write("&nbsp;&nbsp;&nbsp;&nbsp;3) It can help you discover and interpret the underlying patterns and structures in your data, by revealing the most important factors or dimensions.")

                container.write("3) To select the best number of components, you can use cross-validation to evaluate the performance of your machine learning model on unseen data by splitting your data into training and testing sets. You can choose the number of principal components that maximizes or optimizes your desired metric. If interpretability is important for your task, you might want to choose a smaller number of components, which can offer a simpler and more understandable description of your data")

                n_components = st.number_input("Number of PCA components", min_value=1, max_value=min(train_df.shape[0], train_df.shape[1]), value=2)

            if st.button("Apply Data Preprocessing"):
                if balance:
                    train_df = data_preprocess_train.balance_dataset(sample_tech, sample_st)
                    data_preprocess_train.df = train_df

                if transforms:
                    train_df = data_preprocess_train.transform_columns(transform_method, S)
                    data_preprocess_train.df = train_df

                    st.subheader("High Skew Columns and Skew Values in Test Set")
                    skew_values = test_df.apply(lambda x: skew(x))
                    high_skew_columns = skew_values[skew_values > S]

                    if not high_skew_columns.empty:
                        st.write("Skew Values:")
                        st.write(high_skew_columns)
                    else:
                        st.info("No columns have skewness greater than given Threshold.")

                    test_df = data_preprocess_test.transform_columns(transform_method, S)
                    data_preprocess_test.df = test_df

                if scale_options:
                    train_df, test_df = data_preprocess_train.scale_dataset(scale_method), data_preprocess_test.scale_dataset(scale_method)
                    data_preprocess_train.df, data_preprocess_test = train_df, test_df
                    
                if pca:
                    try:
                        pca = PCA(n_components=n_components)
                        X_train, y_train, X_test, y_test = train_df.drop(target, axis=1), train_df[target], test_df.drop(target, axis=1), test_df[target]

                        train_df = pca.fit_transform(X_train)
                        train_df = pd.DataFrame(train_df)
                        train_df[target] = y_train

                        test_df = pd.DataFrame(pca.transform(X_test))
                        test_df[target] = y_test
                    except Exception as e:
                        if train_df.isna().sum().sum() > 0:
                            st.error("Your dataset contains NaN values. Please remove them in the Data Cleaning section and try again")
                        else:
                            st.error(e)
                    data_preprocess_train.df, data_preprocess_test.df = train_df, test_df

                st.session_state.prepo_train_df, st.session_state.prepo_test_df = data_preprocess_train.df, data_preprocess_test.df
                print_shape(train_df)
                print_shape(test_df)

# -----------------------------------
# Model Training  
with st.expander("**Model Training**"):
    models_list = ["Logistic Regression", "Decision Tree", "Random Forest", "XGBoost", "AdaBoost", "LightGBM"]
    if option == 'Upload one file for the entire dataset':
        if "prepro_df" in st.session_state:
            df = st.session_state.prepro_df
        elif "cleaned_df" in st.session_state:
            df = st.session_state.cleaned_df
        elif "df" in st.session_state:
            df = st.session_state.df

        if df is not None:
            target = st.session_state.target
            st.write("Dataset to be used for training")
            st.dataframe(df)

            test_data_size = st.slider("Test data split (%)", 10, 90, 20, 5)
            models = st.multiselect("Select ML models to train", models_list)

            if st.button("Train models"):
                if len(models) == 0:
                    st.error("Please select at least one model to train")
                else:
                    st.session_state.trained_models, st.session_state.model_names, st.session_state.trained_models_dict, st.session_state.default_params = [], models, {}, {}
                    X, y = df.drop(target, axis=1), df[target]
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_data_size/100)
                    st.session_state.X_train, st.session_state.X_test, st.session_state.y_train, st.session_state.y_test = X_train, X_test, y_train, y_test
                    model_training = ModelTraining(X_train, y_train)
                    try:
                        model_training.train_models(models)
                        st.session_state.eval = True
                    except Exception as e:
                        if df.isna().sum().sum() > 0:
                            st.error("Your dataset contains NaN values. Please remove them in the Data Cleaning section and try again")
                        else:
                            st.error(e)

    elif option == 'Upload separate training and testing data':
        if "prepo_train_df" in st.session_state and "prepo_test_df" in st.session_state:
            train_df, test_df = st.session_state.prepo_train_df, st.session_state.prepo_test_df 
        elif "cleaned_train_df" in st.session_state and "cleaned_test_df" in st.session_state:
            train_df, test_df = st.session_state.cleaned_train_df, st.session_state.cleaned_test_df
        elif "train_df" in st.session_state and "test_df" in st.session_state:
            train_df, test_df = st.session_state.train_df, st.session_state.test_df 

        if train_df is not None and test_df is not None:
            target = st.session_state.target
            st.write("Dataset to be used for training")
            st.dataframe(train_df)

            models = st.multiselect("Select ML models to train", models_list)

            if st.button("Train models"):
                if len(models) == 0:
                    st.error("Please select at least one model to train")
                else:
                    st.session_state.trained_models, st.session_state.model_names, st.session_state.trained_models_dict, st.session_state.default_params = [], models, {}, {}
                    X_train, X_test, y_train, y_test = train_df.drop(target, axis = 1), test_df.drop(target, axis = 1), train_df[target], test_df[target]
                    st.session_state.X_train, st.session_state.X_test, st.session_state.y_train, st.session_state.y_test = X_train, X_test, y_train, y_test
                    model_training = ModelTraining(X_train, y_train)  
                    try:
                        model_training.train_models(models)
                        st.session_state.eval = True
                    except Exception as e:
                        if train_df.isna().sum().sum() > 0:
                            st.error("Your dataset contains NaN values. Please remove them in the Data Cleaning section and try again")
                        else:
                            st.error(e)

# -----------------------------------
# Model Evaluation
with st.expander("**Model Evaluation**"):
    if option == "Upload one file for the entire dataset":
        if "evaluated" not in st.session_state:
            st.session_state.evaluated = False
        if ("df" in st.session_state and "X_test" in st.session_state and "y_test" in st.session_state and st.session_state.eval) or st.session_state.evaluated:
            model_evaluation = ModelEvaluation(st.session_state.df, st.session_state.X_train, st.session_state.y_train, st.session_state.X_test, st.session_state.y_test)
            model_evaluation.evaluate_models()
            st.session_state.evaluated = True
    
    elif option == "Upload separate training and testing data":
        if "evaluated" not in st.session_state:
            st.session_state.evaluated = False
        if ("train_df" in st.session_state and "test_df" in st.session_state and "X_test" in st.session_state and "y_test" in st.session_state and st.session_state.eval) or st.session_state.evaluated:
            model_evaluation = ModelEvaluation(st.session_state.train_df, st.session_state.X_train, st.session_state.y_train, st.session_state.X_test, st.session_state.y_test)
            model_evaluation.evaluate_models()
            st.session_state.evaluated = True

# -----------------------------------
# Hyperparameter Tuning
with st.expander("**Hyperparameter Tuning**"):
    if option == "Upload one file for the entire dataset":
        if "X_train" in st.session_state and "y_train" in st.session_state:
            X_train, y_train = st.session_state.X_train, st.session_state.y_train
            if "model_names" in st.session_state:
                models_select = st.multiselect("Select trained models to tune hyperparameters", st.session_state.model_names, key = "HP1")
                if st.button("Tune Model Hyperparameters"):
                    if len(models_select) == 0:
                        st.error("Please select at least one model for hyperparameter tuning.")
                    else:
                        st.session_state.tuned_models, st.session_state.tuned_model_names, st.session_state.tuned_models_dict = [], models_select, {}
                        hyperparameter_tune = HyperparameterTuning(X_train, y_train)
                        model_evaluation_tuned = ModelEvaluation(st.session_state.df, st.session_state.X_train, st.session_state.y_train, st.session_state.X_test, st.session_state.y_test)
                        try:
                            hyperparameter_tune.tune_models(models_select)
                            model_evaluation_tuned.evaluate_tuned_models()
                            st.session_state.tuned = True
                        except Exception as e:
                            if df.isna().sum().sum() > 0:
                                st.error("Your dataset contains NaN values. Please remove them in the Data Cleaning section and try again")
                            else:
                                st.error(e)
    
    elif option == "Upload separate training and testing data":
        if "X_train" in st.session_state and "y_train" in st.session_state:
            X_train, y_train = st.session_state.X_train, st.session_state.y_train
            if "model_names" in st.session_state:
                models_select = st.multiselect("Select trained models to tune hyperparameters", st.session_state.model_names, key = "HP2")
                if st.button("Tune Model Hyperparameters"):
                    if len(models_select) == 0:
                        st.error("Please select at least one model for hyperparameter tuning.")
                    else:
                        st.session_state.tuned_models, st.session_state.tuned_model_names, st.session_state.tuned_models_dict = [], models_select, {}
                        hyperparameter_tune = HyperparameterTuning(X_train, y_train)
                        model_evaluation_tuned = ModelEvaluation(st.session_state.train_df, st.session_state.X_train, st.session_state.y_train, st.session_state.X_test, st.session_state.y_test)
                        try:
                            hyperparameter_tune.tune_models(models_select)
                            model_evaluation_tuned.evaluate_tuned_models()
                            st.session_state.tuned = True
                        except Exception as e:
                            if train_df.isna().sum().sum() > 0:
                                st.error("Your dataset contains NaN values. Please remove them in the Data Cleaning section and try again")
                            else:
                                st.error(e)

# -----------------------------------
# Model Training on Custom parameters
with st.expander("**Model Training on Custom Parameters**"):
    models_list = ["Logistic Regression", "Decision Tree", "Random Forest", "XGBoost", "AdaBoost", "LightGBM"]
    if option == 'Upload one file for the entire dataset':
        if "prepro_df" in st.session_state:
            df = st.session_state.prepro_df
        elif "cleaned_df" in st.session_state:
            df = st.session_state.cleaned_df
        elif "df" in st.session_state:
            df = st.session_state.df
 
        if df is not None:
            target = st.session_state.target
 
            test_data_size = st.slider("Test data split (%)", 10, 90, 20, 5, key = "User")
            models_select_custom = st.selectbox("Select ML models to train", models_list)
           
            st.session_state.trained_models_custom, st.session_state.custom_model_names, st.session_state.trained_models_custom_dict = [], [models_select_custom], {}
            X, y = df.drop(target, axis=1), df[target]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_data_size/100)
            st.session_state.X_train, st.session_state.X_test, st.session_state.y_train, st.session_state.y_test = X_train, X_test, y_train, y_test
            user_model_training = ModelTrainingWithUserParams(X_train, y_train)
            model_evaluation_custom = ModelEvaluation(st.session_state.df, st.session_state.X_train, st.session_state.y_train, st.session_state.X_test, st.session_state.y_test)
            params = user_model_training.get_user_params(models_select_custom)
            if st.button("Train With Custom Parameters"):
                try:
                    user_model_training.train_with_user_params(models_select_custom, params)
                    model_evaluation_custom.evaluate_custom_models()
                except Exception as e:
                    if df.isna().sum().sum() > 0:
                        st.error("Your dataset contains NaN values. Please remove them in the Data Cleaning section and try again")
                    else:
                        st.error(e)
 
    elif option == 'Upload separate training and testing data':
        if "prepo_train_df" in st.session_state and "prepo_test_df" in st.session_state:
            train_df, test_df = st.session_state.prepo_train_df, st.session_state.prepo_test_df
        elif "cleaned_train_df" in st.session_state and "cleaned_test_df" in st.session_state:
            train_df, test_df = st.session_state.cleaned_train_df, st.session_state.cleaned_test_df
        elif "train_df" in st.session_state and "test_df" in st.session_state:
            train_df, test_df = st.session_state.train_df, st.session_state.test_df
 
        if train_df is not None and test_df is not None:
            target = st.session_state.target
 
            models_select_custom = st.selectbox("Select ML models to train", models_list)
 
            st.session_state.trained_models_custom, st.session_state.custom_model_names, st.session_state.trained_models_custom_dict = [], models_select_custom, {}
            X_train, X_test, y_train, y_test = train_df.drop(target, axis = 1), test_df.drop(target, axis = 1), train_df[target], test_df[target]
            st.session_state.X_train, st.session_state.X_test, st.session_state.y_train, st.session_state.y_test = X_train, X_test, y_train, y_test
            model_evaluation_custom = ModelEvaluation(st.session_state.train_df, st.session_state.X_train, st.session_state.y_train, st.session_state.X_test, st.session_state.y_test)
            user_model_training = ModelTrainingWithUserParams(X_train, y_train)
            params = user_model_training.get_user_params(models_select_custom)
            if st.button("Train With Custom Parameters"):
                try:
                    user_model_training.train_with_user_params(models_select_custom, params)
                    model_evaluation_custom.evaluate_custom_models()
                except Exception as e:
                    if train_df.isna().sum().sum() > 0:
                        st.error("Your dataset contains NaN values. Please remove them in the Data Cleaning section and try again")
                    else:
                        st.error(e)

# Decile Analysis
with st.expander("**Decile Analysis**"):
    if "evaluated" not in st.session_state:
        st.session_state.evaluated = False
    if ("df" in st.session_state and "X_train" in st.session_state and "y_train" in st.session_state and "X_test" in st.session_state and "y_test" in st.session_state and st.session_state.eval) or st.session_state.evaluated:
        if "models" in st.session_state or "tuned_models" in st.session_state or "tuned_models_custom" in st.session_state or st.session_state.evaluated:
            model_type_decile = st.radio("Select model type for Decile Analysis", ("Model With Default Hyperparameters", "Model With Tuned Hyperparameters", "Model With Custom Hyperparameters"))
            decile_model = st.selectbox(label = 'Select model to perform decile analysis', options = list(st.session_state.model_names), help = 'Select the model to make predictions for decile analysis')
            if st.button("Get Decile Analysis"):
                decile_analysis = ModelEvaluation(st.session_state.df, st.session_state.X_train, st.session_state.y_train, st.session_state.X_test, st.session_state.y_test)
                st.subheader("Train Set")
                decile_analysis.calculate_deciles(model_type_decile, decile_model, "train")
                st.subheader("Test Set")
                decile_analysis.calculate_deciles(model_type_decile, decile_model, "test")                

# -----------------------------------
# Model Persistence    
with st.expander("**Model Persistence**"):
    if "models" in st.session_state or "tuned_models" in st.session_state or "tuned_models_custom" in st.session_state:
        model_type = st.radio("Select model type to download", ("Models With Default Hyperparameters", "Models With Tuned Hyperparameters", "Model With Custom Hyperparameters"), key="ModelChoice")
        if model_type == "Models With Default Hyperparameters":
            if "models" not in st.session_state:
                st.error("Please train atleast one model!")
            else:
                models_select = st.multiselect("Select default models to download", st.session_state.model_names, key="MP1")
                models = st.session_state.trained_models
        elif model_type == "Models With Tuned Hyperparameters":
            if "tuned_models" not in st.session_state:
                st.error("Please perform hyperparameter tuning first!")
            else:
                models_select = st.multiselect("Select tuned models to download", st.session_state.tuned_model_names, key="MP2")    
                models = st.session_state.tuned_models
        else:
            if "trained_models_custom" not in st.session_state:
                st.error("Please perform model training with custom hyperparameters first!")
            else:
                models_select = st.session_state.custom_model_names  
                models = st.session_state.trained_models_custom
    
        if len(models_select) == 0:
            st.error("Please select at least one model to download.")
        else:
            # Temporary directory to store the models
            os.makedirs("temp", exist_ok=True)
            for model_name, model in zip(st.session_state.model_names, models):
                if model_name in models_select:
                    pickle.dump(model, open("temp/" + model_name + ".pkl", 'wb'))
            # Zip file containing all the models
            with zipfile.ZipFile("models.zip", 'w') as zipf:
                for file in os.listdir("temp"):
                    zipf.write("temp/" + file)
            # Download button for the zip file
            st.download_button(
                label="Download Models",
                data=open("models.zip", 'rb'),
                file_name="models.zip",
                mime="application/octet-stream"
            )
            # Clean up the temporary directory and the zip file
            for file in os.listdir("temp"):
                os.remove("temp/" + file)
            os.rmdir("temp")
            os.remove("models.zip")

        
#if __name__ == "__main__":
    #launch_streamlit()