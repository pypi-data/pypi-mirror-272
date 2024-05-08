from ..utils.streamlit_utils import st
import plotly.express as px

class DataVisualization:
    def __init__(self, df):
        self.df = df
        self.plot_colors = px.colors.sequential.YlOrRd[::-2]

    def visualize(self):
        if "target" in st.session_state:
            target = st.session_state.target
            # Correlation Analysis
            # st.subheader("Correlation Matrix")
            with st.popover("Correlation Matrix", use_container_width=True):
                fig = px.imshow(self.df.corr(numeric_only=True), width = 980, text_auto = ".2f", color_continuous_scale="electric")
                fig.update_layout(autosize=False, width=700, height=600, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig)

            # Box Plots
            # st.subheader("Univariate Analysis (Box Plot)")
            with st.popover("Univariate Analysis (Box Plot)", use_container_width=True):
                all_cols_less_40 = [col for col in self.df.columns if self.df[col].nunique() < 40]
                cols_to_show = st.multiselect("Select columns to show", self.df.drop(target, axis = 1).columns, default=self.df.drop(target, axis = 1).columns[0], key = 'key1')
                for col in cols_to_show:
                    st.write(col)
                    fig = px.box(self.df, y=col, width=980, color_discrete_sequence=self.plot_colors[1:])
                    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                    st.plotly_chart(fig)

            # Bar Plots
            # st.subheader("Univariate Analysis (Bar Chart)")
            with st.popover("Univariate Analysis (Bar Chart)", use_container_width=True):
                all_cols_less_40 = [col for col in self.df.columns if self.df[col].nunique() < 40]
                cols_to_show = st.multiselect("Select columns to show", all_cols_less_40, default=all_cols_less_40[0], key = 'key2')
                for col in cols_to_show:
                    st.write(col)
                    st.bar_chart(self.df[col].value_counts())

            # Dist Plots Against Target Variable
            # st.subheader("Bivariate Analysis (Distribution Plots against Target)")
            with st.popover("Bivariate Analysis (Distribution Plots against Target)", use_container_width=True):
                x_col = st.selectbox("Select x column", self.df.drop(target, axis = 1).columns, index = 0, key = 'key3')
                fig = px.histogram(self.df, x=x_col, color=target, marginal="violin", hover_data=self.df.columns, opacity=0.5)
                st.plotly_chart(fig)

            # Scatter Plots
            all_cols_more_40 = [col for col in self.df.columns if self.df[col].nunique() >= 40]
            if len(all_cols_more_40) > 1:
                # st.subheader("Bivariate Analysis (Scatter plot between two columns)")
                with st.popover("Bivariate Analysis (Scatter plot between two columns)", use_container_width=True):
                    x_col = st.selectbox("Select x column", all_cols_more_40, index=0, key = 'key4')
                    y_col = st.selectbox("Select y column", all_cols_more_40, index=1, key = 'key5')
                    fig = px.scatter(self.df, x=x_col, y=y_col, width=980, color_discrete_sequence=self.plot_colors[1:])
                    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                    st.plotly_chart(fig)