import pickle
from pathlib import Path
import streamlit_authenticator as stauth 

names = ["Kshitij Sharma","AmbalaDist","GurgaonDist","KarnalDist"]
usernames = ["ksharma","Ambala","Gurgaon","Karnal"]
passwords = ['abc123','ambala123','gurgaon123','karnal123']

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)