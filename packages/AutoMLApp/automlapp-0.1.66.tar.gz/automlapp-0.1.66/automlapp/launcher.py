import sys
from streamlit.web import cli as stcli

# def launch_streamlit():
#     # Determine the path to the app.py within the installed package
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     app_path = os.path.join(dir_path, 'app.py')  # Full path to app.py
    
#     # Change the working directory
#     os.chdir(dir_path)
    
#     # Run the streamlit command
#     subprocess.run(["streamlit", "run", app_path])

if __name__ == "__main__":
    #launch_streamlit()
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())