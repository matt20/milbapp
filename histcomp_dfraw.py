import pandas as pd
import streamlit as st
import plotly.express as px
from st_aggrid import AgGrid,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype

#### SET UP THE ACTUAL PAGE ###########################################
st.set_page_config(
    page_title='MiLB Historical Comparison Tool', 
    layout="wide",
    initial_sidebar_state="expanded"
)

#######################################################################
#### ---- LOAD DATAFRAMES ---- ########################################
@st.cache(allow_output_mutation=True)
def load_dfhist():
    URL1 = 'https://github.com/matt20/milbapp/blob/master/milb0621off_70pa.csv?raw=true'
    data1 = pd.read_csv(URL1,index_col = 'playeriduniquecount')
    return data1

dfhist = load_dfhist()

@st.cache(allow_output_mutation=True)
def load_dfraw():
    URL2 = 'https://github.com/matt20/milbapp/blob/master/dfraw.csv?raw=true'
    data2 = pd.read_csv(URL2, index_col = 'playeridunique')
    return data2

dfraw = load_dfraw()

#### SIDEBAR ###########################################################
input_age = st.sidebar.slider('Max Age:', 16, 32, 20)
input_pa_curr = st.sidebar.slider('Min PA (2022):', 30, 100, 50)
input_kpct = st.sidebar.slider('Max K%:', .0, .400, .300)
input_iso = st.sidebar.slider('Min ISO:', .0, .400, .150)
input_bbpct = st.sidebar.slider('Min BB%:', .0, .25, .05)
input_wrcplus = st.sidebar.slider('Min wRC+:', 0, 200, 100)
input_buffer_iso = st.sidebar.slider('ISO Buffer:', .0, .100, .0)
input_buffer_kpct = st.sidebar.slider('K% Buffer:', .0, .100, .0)
input_buffer_bbpct = st.sidebar.slider('BB% Buffer:', .0, .100, .0)
input_pa_hist = st.sidebar.slider('Min PA (Hist):', 100, 400, 100)

#### ADD SOME VARIABLES #################################################
dfhist['level_code'] = dfhist['level'].map({
    "AAA": 8,
    "AA": 7,
    "A+": 6,
    "A": 5,
    "A-": 4,
    "CPX": 1,
    "R": 1,
    "DSL": 1,
})

dfhist['Name/Org'] = dfhist['name'] + dfhist['team']

#### COLUMNS #############################################################
cols_hist = [
    'Name/Org/Year', 'age', 'level', 'pa', 'wrcplus', 'iso', 'kpct', 
    'swstrpct', 'bbpct', 'xSpect', 'OPS', 'babip', 'avg', 'obp', 'slg',
    'hr', 'hrperfb', 'sb', 'cs', 'fbpct', 'ldpct', 'gbpct', 'pullpct',
    'centpct', 'oppopct', 'level_code'
    ]

cols_hist_display = [
    'Name/Org/Year', 'Age', 'Level', 'PA', 'wRC+', 'ISO', 'K%',
    'SwStr%', 'BB%', 'xSpect', 'OPS', 'BABIP', 'AVG', 'OBP', 'SLG', 
    'HR', 'HR/FB', 'SB', 'CS', 'FB%', 'LD%', 'GB%', 'Pull%', 'Cent%',
    'Oppo%', 'level_code'
    ]

cols_curr = [
    'Name/Org', 'Age', 'Level', 'PA', 'wRC+', 'ISO', 'K%',
    'SwStr%', 'BB%', 'xSpect', 'OPS', 'BABIP', 'AVG', 'OBP', 
    'SLG', 'XBH', 'HR', 'HR/FB', 'SB', 'CS', 'FB%', 'GB%', 'LD%',
    'Pull%', 'Cent%', 'Oppo%', 'hmm', 'xPOPS', 'id'
    ]

cols_time = [
    'Name/Org', 'Age', 'Level', 'PA', 'wRC+', 'ISO', 'K%',
    'SwStr%', 'BB%', 'xSpect', 'OPS', 'BABIP', 'AVG', 'OBP', 
    'SLG', 'XBH', 'HR', 'HR/FB', 'SB', 'CS', 'FB%', 'GB%', 'LD%',
    'Pull%', 'Cent%', 'Oppo%', 'hmm', 'xPOPS', 'id', 'Days'
    ]

cols_pct = [
    'K%', 'SwStr%', 'BB%', 'HR/FB', 'FB%', 'GB%', 'LD%',
    'Pull%', 'Cent%', 'Oppo%'
]

cols_slash = [
    'ISO', 'BABIP', 'AVG', 'OBP', 'SLG'
]

st.dataframe(dfraw)

# #######################################################################
# #### --- TRANSFORM THE DATA  ------------------------------------ #####
# dfhist['xSpect'] = (dfhist['iso']/(dfhist['kpct']+dfhist['swstrpct'])).round(3)
# dfhist['Name/Org/Year'] = dfhist['name'] + ' - ' + dfhist['team'] + ' - ' + (dfhist['season']).astype(str)
# dfhist['OPS'] = (dfhist['obp'] + dfhist['slg']).round(3)
# dfhist = dfhist[cols_hist]
# dfhist = dfhist[(dfhist['age'] <= input_age)]
# dfhist = dfhist[(dfhist['pa'] >= input_pa_hist)]
# #dfhist = dfhist[dfhist['level'].isin(input_levels)]
# dfhist['wrcplus'] = dfhist['wrcplus'].round(0)
# dfhist2 = dfhist[(dfhist['iso'] >= input_iso) &
#                  (dfhist['kpct'] <= input_kpct) &
#                  (dfhist['bbpct'] >= input_bbpct) &
#                  (dfhist['wrcplus'] >= input_wrcplus)]
# dfhist2.columns = cols_hist_display
# dfhist2.sort_values(by='wRC+', ascending=False)
# #######################################################################
# #######################################################################
# dfraw['Name/Org'] = (dfraw['Name'] + " - " + dfraw['Org'])
# dfraw['XBH'] = dfraw['2B'] + dfraw['3B'] + dfraw['HR']
# dfraw['idk'] = ((2*dfraw['ISO'])+(dfraw['BB%']/2))**(((3*dfraw['K%'])+dfraw['SwStr%'])**dfraw['BABIP']).round(3)
# dfraw['xSpect'] = (dfraw['ISO']/(dfraw['K%']+dfraw['SwStr%'])).round(3)
# dfraw2 = dfraw.filter(cols_curr, axis=1)
# dfraw2 = dfraw2[(dfraw2['Age'] <= input_age)]
# dfraw2 = dfraw2[(dfraw2['PA'] >= input_pa_curr)]
# dfraw2 = dfraw2.round(3)
# dfraw2['wRC+'] = dfraw2['wRC+'].round(0)
# dfraw2 = dfraw2[(dfraw2['ISO'] >= input_iso) &
#                  (dfraw2['K%'] <= input_kpct) &
#                  (dfraw2['BB%'] >= input_bbpct) &
#                  (dfraw2['wRC+'] >= input_wrcplus)]
# dfraw2 = dfraw2.sort_values(by='wRC+', ascending=False)
# #######################################################################

# #######################################################################
# #### --- THE FIRST DATA TABLE ----------------------------------- #####
# # configure grid options for Ag-Grid table
# gd = GridOptionsBuilder.from_dataframe(dfraw2)
# gd.configure_pagination(enabled=True)
# gd.configure_default_column(editable=True, groupable=True)
# gd.configure_selection(selection_mode='single', use_checkbox=True, pre_selected_rows=[0])
# gridoptions1 = gd.build()
# grid_table = AgGrid(dfraw2, gridOptions=gridoptions1,
#                     update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
#                     height=530,
#                     allow_unsafe_jscode=True,
#                     enable_enterprise_modules = True,
#                     theme='blue')

# #### SETTING UP THE SELECTION ###########################################
# sel_row = grid_table["selected_rows"]

# if sel_row != "":
#     #st.write(sel_row)
#     df_sel = pd.DataFrame(sel_row)
#     st.subheader("Selected player: " + df_sel['Name/Org'].iloc[0] + ' | Level: ' + df_sel['Level'].iloc[0])
#     #st.table(df_sel)

#     sel_iso = df_sel['ISO'].iloc[0]
#     sel_kpct = df_sel['K%'].iloc[0]
#     sel_bbpct = df_sel['BB%'].iloc[0]
#     sel_wrcplus = df_sel['wRC+'].iloc[0]
#     sel_age = df_sel['Age'].iloc[0].astype(int)
#     sel_level = df_sel['Level'].iloc[0]
#     sel_swstrpct = df_sel['SwStr%'].iloc[0]
    
#     sel_buff_iso = (sel_iso - input_buffer_iso).round(3)
#     sel_buff_kpct = (sel_kpct + input_buffer_kpct).round(3)
#     sel_buff_bbpct = (sel_bbpct - input_buffer_bbpct).round(3)
#     #sel_buff_age = sel_age + 1
#     #sel_buff_level = sel_level + 1
#     #sel_buff_swstrpct = sel_swstrpct - input_buffer_other
#     #sel_days = df_sel['Days'].iloc[0]
#     #st.subheader("Last " + sel_days + " days")
#     # sel_id = df_sel.id[0]
#     # df_sel_recent = df_recent.loc[[sel_id]]
#     # df_sel_L7 = df_L7.loc[[sel_id]]
#     # df_sel_L7['Days'] = df_L7.Days[0]
#     # df_sel_L7.set_index('Days', inplace=True)
#     # df_sel_L14 = df_L14.loc[[sel_id]]
#     # df_sel_L14['Days'] = df_L14.Days[0]
#     # df_sel_L14.set_index('Days', inplace=True)
#     # df_sel_recent['Days'] = df_recent.Days[0]
#     # df_sel_recent.set_index('Days', inplace=True)
#     # #df_sel_curr = dfraw2.loc[[sel_id]]
#     # frames = [df_sel_L7, df_sel_L14, df_sel_recent]
#     # result = pd.concat(frames)
#     # st.write('Last 7')
#     # st.table(df_sel_L7)
#     # st.write('Last 14')
#     # st.table(df_sel_L14)
#     # st.write('Last ' + str(df_recent.Days[0]))
#     #st.table(result)
    
#     # st.write('Level Total')
#     # st.table(df_sel_curr)


#     sel_id = df_sel.id[0]


# # if sel_id in df_L7.index.values:
# #     df_sel_L7 = df_L7.loc[[sel_id]]
# #     df_sel_L7['Days'] = df_L7['Days'][0]
# #     df_sel_L7['Days'] = 'Last ' + df_sel_L7['Days'].astype(str)
# #     df_sel_L7.set_index('Days', inplace=True)
# # else: 
# #     df_sel_L7 = pd.DataFrame({}, columns=df_L7.columns, index = ['Days'])

# # if sel_id in df_L14.index.values:
# #     df_sel_L14 = df_L14.loc[[sel_id]]
# #     df_sel_L14['Days'] = df_L14['Days'][0]
# #     df_sel_L14['Days'] = 'Last ' + df_sel_L14['Days'].astype(str)
# #     df_sel_L14.set_index('Days', inplace=True)
# # else:
# #     df_sel_L14 = pd.DataFrame({}, columns=df_L14.columns, index = ['Days'])

# # if sel_id in df_recent.index.values:
# #     df_sel_recent = df_recent.loc[[sel_id]]
# #     df_sel_recent['Days'] = df_recent['Days'][0]
# #     df_sel_recent['Days'] = 'Last ' + df_sel_recent['Days'].astype(str)
# #     df_sel_recent.set_index('Days', inplace=True)
# # else:
# #     df_sel_recent = pd.DataFrame({}, columns=df_recent.columns, index = ['Days'])

# # if sel_id in allidx:
# #     frames = [
# #         df_sel_L7,
# #         df_sel_L14,
# #         df_sel_recent
# #         ]
# #     result = pd.concat(frames)
# #     result2 = result.drop(columns=['Name/Org', 'Age', 'Level', 'id'])
# #     result2['Split'] = result2.index
# #     # shift column 'Name' to first position
# #     first_column = result2.pop('Split')
    
# #     # insert column using insert(position,column_name,
# #     # first_column) function
# #     result2.insert(0, 'Split', first_column)
# #     # CONFIGURE GRID OPTIONS ###############################################
# #     gb2 = GridOptionsBuilder.from_dataframe(result2)
# #     gb2.configure_default_column(min_column_width = .1)
# #     gridoptions3 = gb2.build()

# #     AgGrid(
# #         result2,
# #         gridOptions=gridoptions3,
# #         height=100,
# #         enable_enterprise_modules=True,
# #         theme = "blue"
# #     )

# # else:
# #     st.write('This player has not played during this period')
    


# ## FILTER THE HISTORIC TABLE BASED ON THE SELECTED PLAYER #############
# ## THIS WORKS WITHOUT THE BUFFERS #####################################
# #dfhist3 = dfhist2[(dfhist2['iso'] >= sel_iso) & (dfhist2['kpct'] <= sel_kpct) & (dfhist2['bbpct'] >= sel_bbpct)]
# #either above code or below code depending on whether or not the buffers are working -_- #

# ## FILTER THE HISTORIC TABLE BASED ON THE SELECTED PLAYER #############
# ## WITH BUFFERS #######################################################
# dfhist3 = dfhist2[
#     (dfhist2['ISO'] >= sel_buff_iso) &
#     (dfhist2['K%'] <= sel_buff_kpct) &
#     (dfhist2['BB%'] >= sel_buff_bbpct) &
#     (dfhist2['Age'] <= sel_age)
# ]
          
# dfhist3 = dfhist3.sort_values(by='level_code', ascending=False)

# # CONFIGURE GRID OPTIONS ###############################################
# gb = GridOptionsBuilder.from_dataframe(dfhist3)
# gb.configure_pagination(enabled=True)
# gb.configure_side_bar()

# gb.configure_default_column(min_column_width = .1, groupable=True, value=True, enableRowGroup=True, aggFunc="mean", editable=True)
# gridoptions2 = gb.build()

# AgGrid(
#     dfhist3,
#     gridOptions=gridoptions2,
#     height=530,
#     enable_enterprise_modules=True,
#     theme = "blue"
# )
