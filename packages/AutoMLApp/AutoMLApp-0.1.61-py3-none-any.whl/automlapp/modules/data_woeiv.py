from ..utils.streamlit_utils import st
import pandas as pd
import numpy as np
import scorecardpy as sc
import io

class DataWOEIV:
    def __init__(_self, df):
        _self.df = df

    #@st.cache_data
    def iv_woe(_self, data, target):
        newDF = pd.DataFrame()
        woeDF = pd.DataFrame()
        cols = data.columns

        for ivars in cols[~cols.isin([target])]:
            if data[ivars].dtype.kind in 'bifc':
                # Attempt auto binning, skip if errors occur
                try:
                    binned_x = sc.woebin(data[ivars], data[target])
                    d0 = pd.DataFrame({'x': binned_x, 'y': data[target]})
                except:
                    d0 = pd.DataFrame({'x': data[ivars], 'y': data[target]})
            else:
                d0 = pd.DataFrame({'x': data[ivars], 'y': data[target]})

            d = d0.groupby("x", as_index=False, dropna=False).agg({"y": ["count", "sum"]})
            d.columns = ['Cutoff', 'N', 'Events']
            d['% of Events'] = np.maximum(d['Events'], 0.5) / d['Events'].sum()
            d['Non-Events'] = d['N'] - d['Events']
            d['% of Non-Events'] = np.maximum(d['Non-Events'], 0.5) / d['Non-Events'].sum()
            d['WoE'] = np.log(d['% of Non-Events'] / d['% of Events'])
            d['IV'] = d['WoE'] * (d['% of Non-Events'] - d['% of Events'])
            d.insert(loc=0, column='Variable', value=ivars)

            temp = pd.DataFrame({"Variable": [ivars], "IV": [d['IV'].sum()]}, columns=["Variable", "IV"])
            newDF, woeDF = pd.concat([newDF, temp], axis=0), pd.concat([woeDF, d], axis=0)

        return newDF, woeDF

    def apply_woe_iv(_self):
        if _self.df is not None:
            target = st.session_state.target
            iv, woe = _self.iv_woe(_self.df, target)
            # Create a BytesIO object to store the excel file in memory
            output = io.BytesIO()

            # Create an ExcelWriter object to write the dataframes to different sheets
            writer = pd.ExcelWriter(output)

            # Write the dataframes to the excel file with the specified sheet names and formats
            woe.to_excel(writer, sheet_name='WOE', float_format='%.2f')
            iv.to_excel(writer, sheet_name='IV', float_format='%.2f')

            # Save and close the ExcelWriter object
            writer.close()

            # Seek to the beginning of the BytesIO object
            output.seek(0)

            # Create a download button for the excel file
            st.download_button(
                label='Download Excel file', data=output, file_name='WOE and IV Analysis.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            st.dataframe(iv)
    
    @st.cache_resource
    def display_chart(_self):
        st.subheader("IV Values Interpretation")
        st.write("If the IV value is:")
        df = pd.DataFrame({"Value": ["Less than 0.02", "0.02 to 0.1", "0.1 to 0.3", "0.3 to 0.5", "> 0.5"],
            "Interpretation": ["The predictor is not useful for modeling (separating the Goods from the Bads)",
                                "The predictor has only a weak relationship to the Goods/Bads odds ratio",
                                "The predictor has a medium strength relationship to the Goods/Bads odds ratio",
                                "The predictor has a strong relationship to the Goods/Bads odds ratio",
                                "suspicious relationship (Check once)"]})
        st.dataframe(df, hide_index=True)