import streamlit as st
import pandas as pd
from sklearn import linear_model
import csv
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import matplotlib.pyplot as plt
import numpy as np



st.set_page_config(page_title="Analysis")


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

    st.title("Analysis")
    pos = ["Forwards", "Midfielder", "Defender"]

    position = st.sidebar.selectbox("Position", pos)

    if position == "Forwards":

        def getForwardNames():
            with open("forwards.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    forwardNameList.append(row[0])

        def getForwardCode(playerNameInput):
            with open('forwards.csv', 'r') as file:
                    reader = csv.DictReader(
                        file, fieldnames=['Name', 'code'])
                    for row in reader:
                        if row['Name'] == playerNameInput :
                            return row['code']



        forwardNameList = []

        getForwardNames()

        forwardNameInput = st.sidebar.selectbox("Players",forwardNameList)
        forwardSeasonInput = st.sidebar.selectbox('Seasons', list(reversed(range(2019,2023))))



        #https://fbref.com/en/players/8d78e732/matchlogs/2022-2023/c12/Robert-Lewandowski-Match-Logs
        url = "https://fbref.com/en/players/"+str(getForwardCode(forwardNameInput))+"/matchlogs/"+str(forwardSeasonInput)+"-"+str(forwardSeasonInput+1)+"/"+str(forwardNameInput)+"-Match-Logs"
        html = pd.read_html(url, header=1)
        df = html[0]
        df.drop(columns=df.columns[:11],inplace=True)
        df.drop(columns=df.columns[1:4],inplace=True)
        df.drop(columns=df.columns[4:15],inplace=True)
        df.drop(columns=df.columns[3:8],inplace=True)
        df.drop(columns=df.columns[4:],inplace=True)
        df.drop(df.index[26:], axis=0 , inplace=True)
        dropIndex = df[df["Sh"]=="On matchday squad, but did not play"].index
        df.drop(dropIndex, inplace=True)
        df = df.dropna()

        reg = linear_model.LinearRegression()

        reg.fit(df[["Sh", "SoT", "PrgC"]], df.Gls)

        shotsInput = st.number_input("Shots", min_value = 0)
        shotsOnTargetInput = st.number_input("Shots on Target(<=Shots)", min_value=0, max_value=shotsInput)
        progCarriers = st.number_input("Progressive Carriers", min_value=0)
        potenGoals = reg.predict([[shotsInput,shotsOnTargetInput,progCarriers]])

        if potenGoals[0]>0 :

            st.write("Potential Goals: ", str(potenGoals[0]))

            if st.button(label="Pie Chart"):
                labels = 'Shots', 'Shots on Target', 'Progressive Carriers', 'Potential Goals'
                sizes = [shotsInput, shotsOnTargetInput, progCarriers, potenGoals[0]]
                explode = (0, 0, 0, 0.1) 

                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')

                st.pyplot(fig1)

            if st.button(label="Bar Chart"):
                xp = np.array([shotsInput, shotsOnTargetInput, progCarriers, potenGoals[0]])
                chart_data = pd.DataFrame(xp, index=['Shots', 'Shots on Target', 'Progressive Carriers', 'Potential Goals'])

                st.bar_chart(chart_data, use_container_width=True)
        else:
            st.warning("Please select different set values.")


    elif position == "Midfielder":

        def getMidfielderNames():
            with open("midfielders.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    midfielderNameList.append(row[0])

        def getMidfielderCode(playerNameInput):
            with open('midfielders.csv', 'r') as file:
                    reader = csv.DictReader(
                        file, fieldnames=['Name', 'code'])
                    for row in reader:
                        if row['Name'] == playerNameInput :
                            return row['code']



        midfielderNameList = []
        getMidfielderNames()

        MidfielderNameInput = st.sidebar.selectbox("Players",midfielderNameList)
        MidfielderSeasonInput = st.sidebar.selectbox('Seasons', list(reversed(range(2019,2023))))

        # "https://fbref.com/en/players/e46012d4/matchlogs/2022-2023/Kevin-De-Bruyne-Match-Logs"
        url= "https://fbref.com/en/players/"+str(getMidfielderCode(MidfielderNameInput))+"/matchlogs/"+str(MidfielderSeasonInput)+"-"+str(MidfielderSeasonInput+1)+"/"+str(MidfielderNameInput)+"-Match-Logs"
        html1 = pd.read_html(url, header=1)
        df1 = html1[0]
        df1.drop(columns=df1.columns[:28],inplace=True)
        df1.drop(columns=df1.columns[2:3],inplace=True)
        df1.drop(columns=df1.columns[4:],inplace=True)
        df1.drop(df1.index[30:], axis=0 , inplace=True)
        dropIndex = df1[df1["Cmp"]=="On matchday squad, but did not play"].index
        df1.drop(dropIndex, inplace=True)
        df1 = df1.dropna()

        reg1 = linear_model.LinearRegression()
        reg1.fit(df1[["Att", "PrgP", "Carries"]], df1.Cmp)

        attInput = st.number_input("Passes Attempted")
        progPassInput = st.number_input("Progressive Passes")
        carries = st.number_input("Progressive Carriers")
        potenCompPasses = reg1.predict([[attInput,progPassInput,carries]])
          

        if potenCompPasses[0] > 0:
            st.write("Potential Passes Completed: ", str(int(potenCompPasses[0])))

            if st.button(label="Pie Chart"):
                labels = 'Passes Attempted', 'Progressive Passes', 'Progressive Carriers', 'Potential Passes Completed'
                sizes = [attInput, progPassInput, carries, potenCompPasses[0]]
                explode = (0, 0, 0, 0.1) 

                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')

                st.pyplot(fig1)

            if st.button(label="Bar Chart"):
                xp = np.array([attInput, progPassInput, carries, potenCompPasses[0]])
                chart_data = pd.DataFrame(xp, index=['Passes Attempted', 'Progressive Passes', 'Progressive Carriers', 'Potential Passes Completed'])

                st.bar_chart(chart_data, use_container_width=True)
        else:
            st.warning("Please select different set values.")


    else:
        # print("Defender")

        def getDefenderNames():
            with open("defenders.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    defenderNameList.append(row[0])

        def getDefenderCode(playerNameInput):
            with open('defenders.csv', 'r') as file:
                    reader = csv.DictReader(
                        file, fieldnames=['Name', 'code'])
                    for row in reader:
                        if row['Name'] == playerNameInput :
                            return row['code']



        defenderNameList = []
        getDefenderNames()

        defenderNameInput = st.sidebar.selectbox("Players",defenderNameList)
        defenderSeasonInput = st.sidebar.selectbox('Seasons', list(reversed(range(2019,2023))))

        # "https://fbref.com/en/players/08511d65/matchlogs/2022-2023/Sergio-Ramos-Match-Logs"
        url= "https://fbref.com/en/players/"+str(getDefenderCode(defenderNameInput))+"/matchlogs/"+str(defenderSeasonInput)+"-"+str(defenderSeasonInput+1)+"/"+str(defenderNameInput)+"-Match-Logs"
        html1 = pd.read_html(url, header=1)
        df1 = html1[0]
        df1.drop(columns=df1.columns[:20],inplace=True)
        df1.drop(columns=df1.columns[3:],inplace=True)
        df1.drop(df1.index[30:], axis=0 , inplace=True)
        dropIndex = df1[df1["Tkl"]=="On matchday squad, but did not play"].index
        df1.drop(dropIndex, inplace=True)
        df1 = df1.dropna()

        reg1 = linear_model.LinearRegression()
        reg1.fit(df1[["Int", "Blocks"]], df1.Tkl)

        interceptionsInput = st.number_input("Interceptions")
        blocksInput = st.number_input("Blocks")
        potenTackles = reg1.predict([[interceptionsInput,blocksInput]])

        if potenTackles[0] > 0:

            st.write("Potential Tackles: ", str(potenTackles[0]))

            if st.button(label="Pie Chart"):
                labels = 'Interceptions', 'Blocks', 'Potential Tackles'
                sizes = [interceptionsInput, blocksInput, potenTackles[0]]
                explode = (0, 0, 0.1) 

                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')

                st.pyplot(fig1)

            if st.button(label="Bar Chart"):
                xp = np.array([interceptionsInput, blocksInput, potenTackles[0]])
                chart_data = pd.DataFrame(xp, index=['Interceptions', 'Blocks', 'Potential Tackles'])

                st.bar_chart(chart_data, use_container_width=True)

        else:
            st.warning("Please select different set values.")
