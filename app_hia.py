import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(page_title='A+ Offensive Leaderboards', layout="wide")
st.header('A+ Offensive Leaderboards')

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
age_input = st.sidebar.slider('Max Age:', 17, 40, 23)

#have user select levels to filter data
#levels = ['A','A+','AA','AAA']

# levels_choice = st.sidebar.multiselect(
#     "Levels:", levels, default=levels)

#have user select columns to filter data?
cols =  ['Name/Org', 'Age', 'Level', 'PA', 'xPOPS', 'xSpect', 'K%', 'ISO', 'OPS', 'BB%',
        'BABIP', 'AVG', 'OBP', 'SLG', 'XBH', 'HR', 'SB', 'CS', 'eFB%',
        'eGB%', 'eLD%']

# ['Name', 'Org', 'Age', 'Level', 'PA', 'wRC+', 'K%', 'ISO', 'SwStr%',
#        'BB%', 'OPS', 'BABIP', 'AVG', 'OBP', 'SLG', 'HR/FB', 'HR', '2B', '3B',
#        'SB', 'CS', 'FB%', 'GB%', 'LD%', 'Date']


cols2 = ['Name/Org', 'Age', 'Level', 'PA', 'wRC+', 'K%', 'SwStr%', 'ISO', 
         #'xPOPS', 'xSpect', 
        'OPS', 'BB%',
        'BABIP', 'AVG', 'OBP', 'SLG', 'XBH', 'HR', 'HR/FB', 'SB', 'CS', 'FB%',
        'GB%', 'LD%']

cols_choice = st.sidebar.multiselect(
    "Categories:", cols, default=cols)

orgs = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'LAA', 'LAD','MIA', 
        'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'STL', 'TBR', 'TEX', 'TOR', 'WSN']

orgs_choice = st.sidebar.multiselect(
    "Organizations:", orgs, default=orgs)

### --- LOAD DATAFRAMES
dfrecent = pd.read_csv(r'C:/Users/mwpul/milbapp/hiarecent.csv', 
                 index_col ='idlevel')

dftotal = pd.read_csv(r'C:/Users/mwpul/milbapp/dfhia.csv', 
                 index_col ='idlevel')

### --- FILTER DATAFRAMES BASED ON USER INPUT
#dfrecent['Name/Org/Age/Lvl'] = dfrecent['Name'] + "-" + dfrecent['Org'] + "-" + dfrecent['Age'].astype(str) + "-" + dfrecent['Level']
dfrecent['Name/Org'] = (dfrecent['Name'] + "-" + dfrecent['Org'])
dfrecent['xPOPS'] = (dfrecent['xSpect']*dfrecent['OPS']).round(3)
dfrecent2 = dfrecent[(dfrecent['Age'] <= age_input)]
#dfrecent2 = dfrecent2[dfrecent2['Level'].isin(levels_choice)]
dfrecent2 = dfrecent2.filter(cols_choice, axis=1)

days = dfrecent['Days'].values[0]
lastdate = dfrecent['Date'].values[0]


# utilize the datediff variable in the jupyter notebook to set the X in the subheader
st.subheader("Stats from the last " + days.astype(str) + " days.")

# configure grid options for Ag-Grid table
gb = GridOptionsBuilder.from_dataframe(dfrecent2)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_default_column(min_column_width = 1, groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions = gb.build()

AgGrid(dfrecent2, gridOptions=gridOptions, enable_enterprise_modules=True)


# should make the subheader date dynamic
st.subheader('Totals through ' + lastdate)
dftotal['Name/Org'] = (dftotal['Name'] + "-" + dftotal['Org'])
dftotal['XBH'] = dftotal['2B'] + dftotal['3B'] + dftotal['HR']
#dftotal['xSpect'] = dftotal['ISO'].astype(float)/(dftotal['K%']+dftotal['SwStr%']).astype(float)
#dftotal['xPOPS'] = (dftotal['xSpect']*dftotal['OPS']).round(3)
dftotal2 = dftotal.filter(cols2, axis=1)
dftotal2.columns = cols2

# configure grid options for Ag-Grid table
gb2 = GridOptionsBuilder.from_dataframe(dftotal)
gb2.configure_pagination()
gb2.configure_side_bar()
gb2.configure_selection(selection_mode="multiple", use_checkbox=True)
gb2.configure_default_column(min_column_width = 1, groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions2 = gb2.build()

AgGrid(dftotal, gridOptions=gridOptions2, enable_enterprise_modules=True)

# scatter = px.scatter(dftotal, x=dftotal['K%'], y=dftotal.ISO, 
#                      color=dftotal.Age, hover_name=dftotal.Name)


# ### new code from the fcpython.com tutorial
# st.plotly_chart(scatter)


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
