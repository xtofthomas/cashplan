import pandas as pd
import streamlit as st

#DATA SOURCES
#------------
revenues = pd.read_csv("../data/forecast_euros.csv")
expenses = pd.read_csv("../data/forecast_expenses.csv")


#DATA CLEANING
#-------------
revenues = revenues.rename(columns={"date.utc": "datetime"})
expenses = expenses.rename(columns={"date.utc": "datetime"})
#modifier la colonne en valeur de type datetime
revenues["datetime"] = pd.to_datetime(revenues['datetime'])
expenses["datetime"] = pd.to_datetime(expenses['datetime'])
# permet d'utlliser les fonctions de date
max_revenue = revenues["datetime"].max()
# ajouter une colonne qui ne reprend que le mois
revenues["month"] = revenues["datetime"].dt.month
expenses["month"] = expenses["datetime"].dt.month

#Template
#---------

st.title("The Cash App")
st.divider()
#INPUT DATA
#----------
st.markdown("Here start the journey, how many cash do you have ?")

solde = st.number_input('Cash status',key='solde',value=50000,step=1000)
#solde = 50000 

st.divider()
st.header("Enter your estimations")
st.markdown("You can change, add or remove lines")

#MODELLING
#---------
group_revenues = revenues.groupby(revenues["datetime"].dt.month)["value"].sum()
group_expenses = expenses.groupby(expenses["datetime"].dt.month)["value"].sum()

col1, col2 = st.columns([3, 3])
col1.subheader("Revenues")
col2.subheader("Expenses")

edited_revenues = col1.data_editor(group_revenues,num_rows="dynamic",height=500)
edited_expenses = col2.data_editor(group_expenses,num_rows="dynamic",height=500)

marge = edited_revenues - edited_expenses

st.divider()
st.subheader('Visualise a threshold')
steady = st.number_input('Threshold',key='Threshold',step=1000,value=5000)

cash = []
cash_value = solde
for elements in marge :
    cash_value = cash_value + elements
    cash.append(cash_value)

#st.write(cash) 

# RESULTS
#--------

chartData = pd.DataFrame({
    'revenues' : edited_revenues,
    'expenses' : edited_expenses,
    'threshold' : steady,
    'cash': cash
})

st.divider()

st.header('Results')
st.line_chart(chartData,color = ['#32a852','#cc2929', '#cc8829','#2954cc'])

#TEMPLATE
#--------
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 