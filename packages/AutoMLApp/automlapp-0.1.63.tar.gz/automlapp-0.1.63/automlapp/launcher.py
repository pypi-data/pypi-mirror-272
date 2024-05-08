# automlapp/launcher.py
import subprocess
import os

def launch_streamlit():
    # Assuming app.py is in the same directory as launcher.py
    app_path = os.path.join(os.path.dirname(__file__), 'app.py')
    subprocess.run(["streamlit", "run", app_path])

if __name__ == "__main__":
    launch_streamlit()
