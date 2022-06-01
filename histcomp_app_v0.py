import pandas as pd
import streamlit as st
import plotly.express as px
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(page_title='MiLB Historical Offensive Comparison Tool', layout="wide")
st.header('MiLB Historical Offensive Comparison Tool')

#######################################################################
#### ---- LOAD DATAFRAMES ---- ########################################
dfhist = pd.read_csv(r'C:/Users/mwpul/milbapp/milb0621off_100pa.csv', index_col ='playeriduniquecount')

dfcurr = pd.read_csv(r'C:/Users/mwpul/milbapp/milbtoday.csv', index_col ='idlevelorg')

#have user select parameters to filter data
input_age = st.sidebar.slider('Max Age:', 16, 32, 20)
input_pa_hist = st.sidebar.slider('Min PA (Hist):', 100, 400, 100)
input_pa_curr = st.sidebar.slider('Min PA (2022):', 30, 100, 50)
input_kpct = st.sidebar.slider('Max K%:', .0, .400, .300)
input_iso = st.sidebar.slider('Min ISO:', .0, .400, .150)
input_bbpct = st.sidebar.slider('Min BB%:', .0, .25, .05)
input_wrcplus = st.sidebar.slider('Min wRC+:', 0, 200, 100)


levels = dfhist['level'].unique()

levels_choice = st.sidebar.multiselect(
    "Levels:", levels, default=levels)

cols2 = ['Name/Org', 'Age', 'Level', 'hmm', 'PA', 'wRC+', 'K%', 'SwStr%', 'ISO', 
         #'xPOPS', 'xSpect', 
        'OPS', 'BB%', 'BABIP', 'AVG', 'OBP', 'SLG', 'XBH', 'HR', 'HR/FB', 'SB', 'CS', 'FB%', 'GB%', 'LD%']

#######################################################################
#### --- ADJUSTING THE DATA   ----------------------------------- #####

dfhist['xSpect'] = dfhist['iso']/(dfhist['kpct']+dfhist['swstrpct'])
dfhist = dfhist[(dfhist['age'] <= input_age)]
dfhist = dfhist[(dfhist['pa'] >= input_pa_hist)]
dfhist = dfhist[dfhist['level'].isin(levels_choice)]
dfhist['wrcplus'] = dfhist['wrcplus'].round(0)
dfhist2 = dfhist[(dfhist['iso'] >= input_iso) &
                 (dfhist['kpct'] <= input_kpct) &
                 (dfhist['bbpct'] >= input_bbpct) &
                 (dfhist['wrcplus'] >= input_wrcplus)]
dfhist = dfhist[dfhist['level'].isin(levels_choice)]
#######################################################################
dfcurr['Name/Org'] = (dfcurr['Name'] + " - " + dfcurr['Org'])
#dfcurr = dfcurr[dfcurr['Org'].isin(orgs_choice)]
dfcurr['XBH'] = dfcurr['2B'] + dfcurr['3B'] + dfcurr['HR']
dfcurr['hmm'] = ((dfcurr['ISO']+dfcurr['BB%'])**((dfcurr['K%']**dfcurr['BABIP']))).round(3)
#dfcurr['xSpect'] = dfcurr['ISO']/(dfcurr['K%']+dfcurr['SwStr%'])
#dfcurr['xPOPS'] = (dfcurr['xSpect']*dfcurr['OPS']).round(3)
dfcurr2 = dfcurr.filter(cols2, axis=1)
dfcurr2 = dfcurr2[(dfcurr2['Age'] <= input_age)]
dfcurr2 = dfcurr2[(dfcurr2['PA'] >= input_pa_curr)]
dfcurr2 = dfcurr2.round(3)
dfcurr2['wRC+'] = dfcurr2['wRC+'].round(0)
#dfcurr2 = dfcurr2[dfcurr2['Level'].isin(levels_choice)]
#dfcurr2.columns = cols2
#######################################################################


#######################################################################
#### --- THE FIRST DATA TABLE ----------------------------------- #####
# utilize the datediff variable in the jupyter notebook to set the X in the subheader
st.subheader("Stats since 2006")

# configure grid options for Ag-Grid table
gb = GridOptionsBuilder.from_dataframe(dfhist2)
#gb.configure_pagination()
#gb.configure_column('Name/Org', min_column_width = 25)
gb.configure_side_bar()
#gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_default_column(min_column_width = .1, groupable=True, value=True, enableRowGroup=True, aggFunc="mean", editable=True)
gridOptions = gb.build()

agree_hist = st.checkbox('Show historical data')

if agree_hist:
     AgGrid(dfhist2, gridOptions=gridOptions, enable_enterprise_modules=True, theme = "blue")

# configure grid options for Ag-Grid table
gb2 = GridOptionsBuilder.from_dataframe(dfcurr2)
#gb2.configure_pagination()
gb2.configure_side_bar()
#gb2.configure_selection(selection_mode="multiple", use_checkbox=True)
gb2.configure_default_column(min_column_width = 1, groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions2 = gb2.build()



agree_curr = st.checkbox('Show 2022 data')

if agree_curr:
     AgGrid(dfcurr2, gridOptions=gridOptions2, enable_enterprise_modules=True, theme='blue')