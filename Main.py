import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns 
from UI import *
import altair as alt
from matplotlib import pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer
import streamlit.components.v1 as stc
import time
import pickle
from pathlib import Path
from tables import render_table_editor
from Pro import ProPage
from analysis import HomePage
import streamlit_authenticator as stauth
from data import load_and_merge_data
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Home", page_icon="🌎", layout="wide")

# Load CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar Navigation
def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=[ "Home","Database", "Projects"],
            icons=["house", "key", "eye"],
            menu_icon="cast",
            default_index=0,
        )
    return selected

# Sidebar Date Filters
# Sidebar Date Filters
with st.sidebar:
    st.sidebar.image("images/kcm.jpg")
    st.title("Select Date Range")
    start_date = st.date_input(
        label="Start Date",
        value=pd.to_datetime("01-01-2025")
    )
    end_date = st.date_input(
        label="End Date",
        value=pd.to_datetime("10-12-2025")
    )


    

   



# PROGRESS PAGE FUNCTION
def ProgressBar():
    st.subheader("🕸 PM Database", divider="rainbow")

    selected_table = st.selectbox("Choose Table", ["Projects", "Tasks", "Financials", "Departments"])

    if selected_table == "Projects":
        render_table_editor(
            file_path="projects.csv",
            key_prefix="projects",
            id_column="Project_ID",
            date_columns=["Start_Date", "End_Date"]
        )

    elif selected_table == "Tasks":
        render_table_editor(
            file_path="tasks.csv",
            key_prefix="tasks",
            id_column="Task_ID",
            date_columns=["Est_Start", "Est_End", "Act_Start", "Act_End", "Last_Updated"]
        )

    elif selected_table == "Financials":
        render_table_editor(
            file_path="costs.csv",
            key_prefix="costs",
            id_column="Cost_ID"  # Adjust based on your actual ID column
        )

    elif selected_table == "Departments":
        render_table_editor(
            file_path="Departments.csv",
            key_prefix="departments",
            id_column="Department_ID"  # Adjust based on your actual ID column
        )


    # Progress Bar
    st.markdown(
        """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",
        unsafe_allow_html=True,
    )

    target = 3000000000
    percent = round((target * 100) / target)  # Just for demo

    my_bar = st.progress(0)
    if percent > 100:
        st.subheader("Target 100% Completed")
    else:
        st.write("You have", percent, "% of", format(target, ',d'), "TZS")
        for percent_complete in range(percent):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text="Target percentage")







# Call correct page
selected = sideBar()



if selected == "Database":
    ProgressBar()

elif selected == "Home":
   HomePage()    

elif selected == "Projects":
    ProPage()      

# Bottom error message
st.error(f"Business Metrics between [{start_date}] and [{end_date}]")






