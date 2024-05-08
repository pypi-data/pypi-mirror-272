# automlapp/fetchdir.py
import os

def fetch():
    # Fetch the directory of app.py
    dir_path = os.path.dirname(os.path.abspath(__file__))
    print(dir_path)

if __name__ == "__main__":
    fetch()
