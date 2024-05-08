from utils.streamlit_utils import st
import os, io
import pandas as pd
import zipfile

class DataInput:
    def __init__(_self, uploaded_file, key_suffix = None):
        _self.uploaded_file = uploaded_file
        _self.key_suffix = key_suffix

    def upload_dataset(_self):
        st.write("**Filename:**", _self.uploaded_file.name)
        st.write("**Type:**", _self.uploaded_file.type)

        has_header = st.toggle('Does the dataset have a header?', value = True, key=f'header_toggle_{_self.key_suffix}')
        header_param = 0 if has_header else None

        file_extension = os.path.splitext(_self.uploaded_file.name)[1]

        if file_extension == '.csv':
            df = pd.read_csv(_self.uploaded_file, header = header_param)
        elif file_extension == '.tsv':
            df = pd.read_csv(_self.uploaded_file, sep = '\t', header = header_param)
        elif file_extension == '.txt':
            df = pd.read_csv(_self.uploaded_file, sep = ' ', header = header_param)
        elif file_extension == '.xlsx':
            df = pd.read_excel(_self.uploaded_file, header = header_param)
        elif file_extension == '.zip':
            with zipfile.ZipFile(_self.uploaded_file, 'r') as z:
                # Assuming there's only one file in the zip archive, and it's a csv file
                try:
                    with z.open(z.namelist()[0]) as f:
                        df = pd.read_csv(f, header = header_param)
                except:
                    st.error("Please upload a zip file containing a single CSV file")
    
        if not has_header:
            df = df.drop(0, axis = 0)
        st.dataframe(df, hide_index = True, use_container_width = True)
        st.write(f"Number of Samples: :red[{df.shape[0]}]")
        st.write(f"Number of Features: :red[{df.shape[1]}]")
        
        # st.subheader("Dataset Info")
        # with st.container(border = True):
        with st.popover("Dataset Info"):
            buffer = io.StringIO()

            # Pass the buffer to df.info()
            df.info(buf=buffer, memory_usage="deep")

            # Get the dataframe info as a string from the buffer
            df_info = buffer.getvalue()

            # Split the string into lines and remove the first line
            lines = df_info.split('\n')
            df_info = '\n'.join(lines[1:])

            # Display the dataframe info in the Streamlit app
            st.text(df_info)
        return df