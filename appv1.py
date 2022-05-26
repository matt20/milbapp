import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from st_aggrid import AgGrid

st.set_page_config(page_title='MiLB Offensive Leaderboards')
st.header('MiLB Offensive Leaderboards')

# my_page = st.sidebar.radio('Page Navigation', ['A', 'A+', 'AA', 'AAA'])

# if my_page == 'A':
#     st.title('here is a page')
#     button = st.button('a button')
#     if button:
#         st.write('clicked')
# if my_page == 'A+':
#     st.title('here is a page')
#     button = st.button('a button')
#     if button:
#         st.write('clicked')
# if my_page == 'AA':
#     st.title('here is a page')
#     button = st.button('a button')
#     if button:
#         st.write('clicked')
# if my_page == 'AAA':
#     st.title('here is a page')
#     button = st.button('a button')
#     if button:
#         st.write('clicked')
# else:
#     st.title('this is a different page')
#     slide = st.slider('this is a slider')
#     slide

# age_input = st.number_input(
#     'Maximum age:', min_value=17, max_value=40, value = 24, step = 1
# )

#have user select maximum age to filter data
age_input = st.sidebar.slider('Max Age:', 17, 40, 21)

#have user select levels to filter data
levels = ['A','A+','AA','AAA']

levels_choice = st.sidebar.multiselect(
    "Levels:", levels, default=levels)

#have user select columns to filter data
cols =  ['Name/Org/Age/Lvl', 'xSpect', 'K%', 'ISO', 'OPS', 'BB%',
        'PA', 'BABIP', 'AVG', 'OBP', 'SLG', 'XBH', 'HR', 'SB', 'CS', 'eFB%',
        'eGB%', 'eLD%']

cols_choice = st.sidebar.multiselect(
    "Categories:", cols, default=cols)


### --- LOAD DATAFRAMES
dfrecent = pd.read_csv(r'C:/Users/mwpul/milbapp/milbrecent.csv', 
                 index_col ='idlevel')

dftotal = pd.read_csv(r'C:/Users/mwpul/milbapp/milbtoday.csv', 
                 index_col ='idlevel')

### --- FILTER DATAFRAMES BASED ON USER INPUT
dfrecent['Name/Org/Age/Lvl'] = dfrecent['Name'] + "-" + dfrecent['Org'] + "-" + dfrecent['Age'].astype(str) + "-" + dfrecent['Level']
dfrecent2 = dfrecent[(dfrecent['Age'] <= age_input)]
dfrecent2 = dfrecent2[dfrecent2['Level'].isin(levels_choice)]
dfrecent2 = dfrecent2.filter(cols_choice, axis=1)

days = dfrecent['Days'].values[0]





# utilize the datediff variable in the jupyter notebook to set the X in the subheader
st.subheader("Stats from the last " + days.astype(str) + " days.")
AgGrid(dfrecent2)

# should make the subheader date dynamic
st.subheader('Totals through 5/21/22')
st.dataframe(dftotal)

scatter = px.scatter(dftotal, x=dftotal.kpct, y=dftotal.iso, 
                     color=dftotal.age, hover_name=dftotal.name)


### new code from the fcpython.com tutorial
st.plotly_chart(scatter)


df2cols = dfrecent2.columns
#This is our header
st.markdown(print(df2cols))
 #This is our plot
st.vega_lite_chart(dfrecent2, {
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'K%', 'type': 'quantitative'},
         'y': {'field': 'ISO', 'type': 'quantitative'},
         'color': {'field': 'OPS', 'type': 'quantitative'},
         'tooltip': [{"field": 'Name', 'type': 'nominal'}, {'field': 'Org', 'type': 'nominal'}, {'field': 'Age', 'type': 'quantitative'}],
     },
     'width': 700,
     'height': 400,
})

