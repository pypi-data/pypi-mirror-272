from ..utils.streamlit_utils import st

def print_shape(df):
    st.dataframe(df)
    st.write(f"Number of Samples: :red[{df.shape[0]}]")
    st.write(f"Number of Features: :red[{df.shape[1]}]")