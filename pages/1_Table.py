import streamlit as st
import pandas as pd
import base64
import csv
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="Table")


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

    
    def getTeam():
            with open('Teams.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    teamName.append(row[1])

    teamName = []
    getTeam()

    seasonInput = st.sidebar.selectbox('Seasons', list(reversed(range(2010,2023))))
    teamInput = st.sidebar.selectbox('Teams', list(teamName))



    def loadCode(teamInput):
        with open('Teams.csv', 'r') as file:
            reader = csv.DictReader(
                file, fieldnames=['id','Team', 'code'])
            for row in reader:
                if row['Team'] == teamInput :
                    return row['code']

    #https://fbref.com/en/squads/206d90db/2021-2022/Barcelona-Stats

    st.title(teamInput + " Stats "+ str(seasonInput-2000)+ "/" + str(seasonInput-1999))



    def loadStats(year):
        url = "https://fbref.com/en/squads/"+str(loadCode(teamInput))+"/"+ str(year)+"-"+str(year+1)+"/"+str(teamInput)+"-Stats"
        html = pd.read_html(url, header=1)
        df = html[0]
        df.rename(columns={'Gls':'Goals', 'CrdY':'Yellow Cards', 'CrdR':'Red Cards'}, inplace=True)
        raw = df.drop('Nation', axis=1)
        raw.drop(columns=df.columns[16:],inplace=True)
        raw.drop(columns=df.columns[3:8], inplace=True)
        raw = raw.dropna()
        return raw

    new_data = loadStats(seasonInput)

    st.write(new_data)
    def download_link(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  
        href = f'<a href="data:file/csv;base64,{b64}" download = "TeamData.csv">Download csv file</a>'
        return href

    st.markdown(download_link(new_data), unsafe_allow_html= True)














