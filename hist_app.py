import pandas as pd
import streamlit as st
import plotly.express as px
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(page_title='MiLB Historical Offensive Leaderboards', layout="wide")
st.header('MiLB Historical Offensive Leaderboards')

#######################################################################
#### ---- LOAD DATAFRAMES ---- ########################################
dfhist = pd.read_csv(r'C:/Users/mwpul/milbapp/milb0621off_100pa.csv', 
                     index_col ='playeriduniquecount')


#have user select parameters to filter data
age_input = st.sidebar.slider('Max Age:', 17, 40, 20)
pa_input = st.sidebar.slider('Min PA:', 100, 400, 100)

levels = dfhist['level'].unique()

levels_choice = st.sidebar.multiselect(
    "Levels:", levels, default=levels)


#######################################################################
#### --- ADJUSTING THE DATA   ----------------------------------- #####

dfhist['xSpect'] = dfhist['iso']/(dfhist['kpct']+dfhist['swstrpct'])
dfhist = dfhist[(dfhist['age'] <= age_input)]
dfhist = dfhist[(dfhist['pa'] >= pa_input)]
#dftotal2 = dftotal2.round(3)
# dftotal2 = dftotal2[(dftotal2['K%'] <= kpct_input)]
# dftotal2 = dftotal2[(dftotal2['ISO'] >= iso_input)]
# dftotal2 = dftotal2[(dftotal2['BB%'] >= bbpct_input)]
# dftotal2 = dftotal2[(dftotal2['HR'] >= hr_input)]
# dftotal2 = dftotal2[(dftotal2['SB'] >= sb_input)]
# dftotal2 = dftotal2[(dftotal2['BABIP'] >= babip_input)]
#dftotal2.columns = cols2
#dftotal2 = dftotal2[dftotal2['Level'].isin(levels_choice)]
#dftotal2.columns = cols2


#######################################################################
#### --- THE FIRST DATA TABLE ----------------------------------- #####
# utilize the datediff variable in the jupyter notebook to set the X in the subheader
st.subheader("Stats since 2006")

# configure grid options for Ag-Grid table
gb = GridOptionsBuilder.from_dataframe(dfhist)
#gb.configure_pagination()
#gb.configure_column('Name/Org', min_column_width = 25)
gb.configure_side_bar()
#gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_default_column(min_column_width = .1, groupable=True, value=True, enableRowGroup=True, aggFunc="mean", editable=True)
gridOptions = gb.build()

AgGrid(dfhist, gridOptions=gridOptions, enable_enterprise_modules=True, theme = "blue") #fit_columns_on_grid_load=True)
#st.dataframe(dfrecent2.describe())
#A
