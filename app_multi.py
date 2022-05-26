import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(page_title='MiLB Offensive Leaderboards', layout="wide")
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
age_input = st.sidebar.slider('Max Age:', 17, 40, 25)
pa_input = st.sidebar.slider('Min PA:', 10, 30, 10)
# Create a page dropdown 
page = st.sidebar.selectbox("Select level:", ["All", "AAA", "AA", "A+", "A"]) 
if page == "Page 1":
    # Display details of page 1
elif page == "Page 2":
    # Display details of page 2
elif page == "Page 3":
    # Display details of page 3
elif page == "Page 4":
    # Display details of page 3
elif page == "Page ":
    # Display details of page 3    

# kpct_input = st.sidebar.slider('Max K%:', .40, .10, .25)
# iso_input = st.sidebar.slider('Min ISO:', .000, .400, .200)
# bbpct_input = st.sidebar.slider('Min BB%:', .000, .15, .05)
# hr_input = st.sidebar.slider('Min HR:', 0, 30, 0)
# sb_input = st.sidebar.slider('Min SB:', 0, 30, 0)
# babip_input = st.sidebar.slider('Min BABIP:', .000, .400, .000)

#have user select levels to filter data
levels = ['A','A+','AA','AAA']

levels_choice = st.sidebar.multiselect(
    "Levels:", levels, default=levels)

#have user select columns to filter data?
cols =  ['Name/Org', 'Age', 'Level', 'PA', 'xPOPS', 'xSpect', 'K%', 'ISO', 'OPS', 'BB%',
        'BABIP', 'AVG', 'OBP', 'SLG', 'XBH', 'HR', 'SB', 'CS', 'eFB%',
        'eGB%', 'eLD%']

colsdefault =  ['Name/Org', 'Age', 'Level', 'PA', 'xPOPS', 'xSpect', 'K%', 'ISO', 'OPS', 'BB%',
        'BABIP', 'AVG', 'OBP', 'SLG', 'XBH', 'HR', 'SB', 'CS']

# ['Name', 'Org', 'Age', 'Level', 'PA', 'wRC+', 'K%', 'ISO', 'SwStr%',
#        'BB%', 'OPS', 'BABIP', 'AVG', 'OBP', 'SLG', 'HR/FB', 'HR', '2B', '3B',
#        'SB', 'CS', 'FB%', 'GB%', 'LD%', 'Date']

orgs = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'LAA', 'LAD','MIA', 
        'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SEA', 'SFG', 'STL', 'TBR', 'TEX', 'TOR', 'WSN']

orgs_choice = st.sidebar.multiselect(
    "Organizations:", orgs, default=orgs)

cols2 = ['Name/Org', 'Age', 'Level', 'PA', 'wRC+', 'K%', 'SwStr%', 'ISO', 
         #'xPOPS', 'xSpect', 
        'OPS', 'BB%',
        'BABIP', 'AVG', 'OBP', 'SLG', 'XBH', 'HR', 'HR/FB', 'SB', 'CS', 'FB%',
        'GB%', 'LD%']

cols_choice = st.sidebar.multiselect(
    "Categories:", cols, default=colsdefault)



### --- LOAD DATAFRAMES
dfrecent = pd.read_csv(r'C:/Users/mwpul/milbapp/milbrecent.csv', 
                 index_col ='idlevel')

dftotal = pd.read_csv(r'C:/Users/mwpul/milbapp/milbtoday.csv', 
                 index_col ='idlevel')

### --- FILTER DATAFRAMES BASED ON USER INPUT
#dfrecent['Name/Org/Age/Lvl'] = dfrecent['Name'] + "-" + dfrecent['Org'] + "-" + dfrecent['Age'].astype(str) + "-" + dfrecent['Level']
dfrecent['Name/Org'] = (dfrecent['Name'] + "-" + dfrecent['Org'])
dfrecent['xPOPS'] = (dfrecent['xSpect']*dfrecent['OPS']).round(3)
dfrecent2 = dfrecent[(dfrecent['Age'] <= age_input)]
dfrecent2 = dfrecent2[(dfrecent2['PA'] >= pa_input)]
dfrecent2 = dfrecent2[dfrecent2['Level'].isin(levels_choice)]
dfrecent2 = dfrecent2[dfrecent2['Org'].isin(orgs_choice)]
dfrecent2 = dfrecent2.filter(cols_choice, axis=1)

days = dfrecent['Days'].values[0]
lastdate = dfrecent['Date'].values[0]


# utilize the datediff variable in the jupyter notebook to set the X in the subheader
st.subheader("Stats from the last " + days.astype(str) + " days.")

# configure grid options for Ag-Grid table
gb = GridOptionsBuilder.from_dataframe(dfrecent2)
#gb.configure_pagination()
gb.configure_column('Name/Org', min_column_width = 25)
gb.configure_side_bar()
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_default_column(min_column_width = .1, groupable=True, value=True, enableRowGroup=True, aggFunc="mean", editable=True)
gridOptions = gb.build()

AgGrid(dfrecent2, gridOptions=gridOptions, enable_enterprise_modules=True, theme = "blue") #fit_columns_on_grid_load=True)
#st.dataframe(dfrecent2.describe())
#AgGrid(dfrecent2.describe(), gridOptions=gridOptions, enable_enterprise_modules=True, theme = "blue") #fit_columns_on_grid_load=True))

# should make the subheader date dynamic
st.subheader('Totals through ' + lastdate)
patot_input = st.slider('Min PA:', 10, 70, 30)

dftotal['Name/Org'] = (dftotal['Name'] + "-" + dftotal['Org'])
dftotal = dftotal[dftotal['Org'].isin(orgs_choice)]
dftotal['XBH'] = dftotal['2B'] + dftotal['3B'] + dftotal['HR']
#dftotal['xSpect'] = dftotal['ISO']/(dftotal['K%']+dftotal['SwStr%'])
#dftotal['xPOPS'] = (dftotal['xSpect']*dftotal['OPS']).round(3)
dftotal2 = dftotal.filter(cols2, axis=1)
dftotal2 = dftotal2[(dftotal2['Age'] <= age_input)]
dftotal2 = dftotal2[(dftotal2['PA'] >= patot_input)]
# dftotal2 = dftotal2[(dftotal2['K%'] <= kpct_input)]
# dftotal2 = dftotal2[(dftotal2['ISO'] >= iso_input)]
# dftotal2 = dftotal2[(dftotal2['BB%'] >= bbpct_input)]
# dftotal2 = dftotal2[(dftotal2['HR'] >= hr_input)]
# dftotal2 = dftotal2[(dftotal2['SB'] >= sb_input)]
# dftotal2 = dftotal2[(dftotal2['BABIP'] >= babip_input)]
#dftotal2.columns = cols2
dftotal2 = dftotal2[dftotal2['Level'].isin(levels_choice)]
#dftotal2.columns = cols2


# configure grid options for Ag-Grid table
gb2 = GridOptionsBuilder.from_dataframe(dftotal2)
#gb2.configure_pagination()
gb2.configure_side_bar()
gb2.configure_selection(selection_mode="multiple", use_checkbox=True)
gb2.configure_default_column(min_column_width = 1, groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions2 = gb2.build()

AgGrid(dftotal2, gridOptions=gridOptions2, enable_enterprise_modules=True, theme='blue')

# scatter = px.scatter(dftotal2, x=dftotal['K%'], y=dftotal.ISO, 
#                      color=dftotal.Age, hover_name=dftotal.Name)


### new code from the fcpython.com tutorial
# st.plotly_chart(scatter)
