import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="main")

with open('./config.yaml') as file:
    config = yaml.load(file, Loader = SafeLoader) 



with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

hashedPass = stauth.Hasher(["abc", "def"]).generate()


authenticator = stauth.Authenticate(config['credentials'],cookie_name='app_dashboard',
                                    key='abcdef', cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False :
    st.error("Your Username / Password is incorrect. Please try again.")
if authentication_status == None:
    st.warning("Please enter your credentials")
if authentication_status:


    
    st.title("Welcome "+str(name))

    st.header("This is Football Performance Analyser⚽")
    st.header("You can explore this website with the help of Navigation on the sidebar👈")

    
    authenticator.logout("Logout", "sidebar")

