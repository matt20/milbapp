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
def load_dfcurr():
    URL2 = 'https://github.com/matt20/milbapp/blob/master/milbtoday.csv?raw=true'
    data2 = pd.read_csv(URL2, index_col = 'idlevelorg')
    return data2

dfcurr = load_dfcurr()

@st.cache(allow_output_mutation=True)
def load_df_recent():
    URL3 = 'https://github.com/matt20/milbapp/blob/master/milbrecent.csv?raw=true'
    data3 = pd.read_csv(URL3, index_col = 'idlevelorg')
    return data3

df_recent = load_df_recent()

@st.cache(allow_output_mutation=True)
def load_dfL7():
    URL7 = 'https://github.com/matt20/milbapp/blob/master/milb_l7.csv?raw=true'
    data7 = pd.read_csv(URL7, index_col = 'idlevelorg')
    return data7

df_L7 = load_dfL7()

@st.cache(allow_output_mutation=True)
def load_dfL14():
    URL14 = 'https://github.com/matt20/milbapp/blob/master/milb_l14.csv?raw=true'
    data14 = pd.read_csv(URL14, index_col = 'idlevelorg')
    return data14

df_L14 = load_dfL14()

#######################################################################

#st.header('MiLB Historical Offensive Comparison Tool')
#st.write('Use the sliders on the sidebar to filter 2022 Minor League Baseball statistics (updated as of yesterday, courtesy of FanGraphs.com)')

#### SIDEBAR ###########################################################
input_age = st.sidebar.slider('Max Age:', 16, 32, 20)
input_pa_curr = st.sidebar.slider('Min PA (2022):', 0, 150, 0)
input_kpct = st.sidebar.slider('Max K%:', .0, .400, .300)
input_iso = st.sidebar.slider('Min ISO:', .0, .400, .150)
input_bbpct = st.sidebar.slider('Min BB%:', .0, .25, .05)
input_wrcplus = st.sidebar.slider('Min wRC+:', 0, 200, 100)
input_buffer_iso = st.sidebar.slider('ISO Buffer:', .0, .100, .0)
input_buffer_kpct = st.sidebar.slider('K% Buffer:', .0, .100, .0)
input_buffer_bbpct = st.sidebar.slider('BB% Buffer:', .0, .100, .0)
input_pa_hist = st.sidebar.slider('Min PA (Hist):', 100, 400, 100)

levels = dfhist['level'].unique()
input_levels = st.sidebar.multiselect(
    "Levels:", levels, default=levels)

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
dfcurr['id'] = dfcurr.index
df_L7['id'] = df_L7.index
df_L14['id'] = df_L14.index
df_recent['id'] = df_recent.index

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
    'Pull%', 'Cent%', 'Oppo%', 'hmm', 'xPOPS', 'id', 'Name'
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

#######################################################################
#### --- TRANSFORM THE DATA  ------------------------------------ #####
dfhist['xSpect'] = (dfhist['iso']/(dfhist['kpct']+dfhist['swstrpct'])).round(3)
dfhist['Name/Org/Year'] = dfhist['name'] + ' - ' + dfhist['team'] + ' - ' + (dfhist['season']).astype(str)
dfhist['OPS'] = (dfhist['obp'] + dfhist['slg']).round(3)
dfhist = dfhist[cols_hist]
dfhist = dfhist[(dfhist['age'] <= input_age)]
dfhist = dfhist[(dfhist['pa'] >= input_pa_hist)]
dfhist = dfhist[dfhist['level'].isin(input_levels)]
dfhist['wrcplus'] = dfhist['wrcplus'].round(0)
dfhist2 = dfhist[(dfhist['iso'] >= input_iso) &
                 (dfhist['kpct'] <= input_kpct) &
                 (dfhist['bbpct'] >= input_bbpct) &
                 (dfhist['wrcplus'] >= input_wrcplus)]
dfhist2.columns = cols_hist_display
dfhist2.sort_values(by='wRC+', ascending=False)
#######################################################################
#######################################################################
dfcurr['Name/Org'] = (dfcurr['Name'] + " - " + dfcurr['Org'])
dfcurr['XBH'] = dfcurr['2B'] + dfcurr['3B'] + dfcurr['HR']
dfcurr['idk'] = ((2*dfcurr['ISO'])+(dfcurr['BB%']/2))**(((3*dfcurr['K%'])+dfcurr['SwStr%'])**dfcurr['BABIP']).round(3)
dfcurr['xSpect'] = (dfcurr['ISO']/(dfcurr['K%']+dfcurr['SwStr%'])).round(3)
dfcurr2 = dfcurr.filter(cols_curr, axis=1)
dfcurr2 = dfcurr2[(dfcurr2['Age'] <= input_age)]
dfcurr2 = dfcurr2[(dfcurr2['PA'] >= input_pa_curr)]
dfcurr2 = dfcurr2.round(3)
dfcurr2['wRC+'] = dfcurr2['wRC+'].round(0)
dfcurr2 = dfcurr2[(dfcurr2['ISO'] >= input_iso) &
                 (dfcurr2['K%'] <= input_kpct) &
                 (dfcurr2['BB%'] >= input_bbpct) &
                 (dfcurr2['wRC+'] >= input_wrcplus)]
dfcurr2 = dfcurr2.sort_values(by='wRC+', ascending=False)
#dfcurr['xPOPS'] = (dfcurr['xSpect']*dfcurr['OPS']).round(3)
#dfcurr = dfcurr[dfcurr['Org'].isin(orgs_choice)]
#dfcurr2 = dfcurr2[dfcurr2['Level'].isin(input_levels)]
#######################################################################
#######################################################################
df_L7['Name/Org'] = (df_L7['Name'] + " - " + df_L7['Org'])
df_L7['idk'] = ((2*df_L7['ISO'])+(df_L7['BB%']/2))**(((3*df_L7['K%'])*2)**df_L7['BABIP']).round(3)
df_L7['xSpect'] = (df_L7['ISO']/(df_L7['K%']*2)).round(3)
df_L7 = df_L7.filter(cols_time, axis=1)
#df_L7 = df_L7[(df_L7['Age'] <= input_age)]
#df_L7 = df_L7[(df_L7['PA'] >= input_pa_curr)]
df_L7 = df_L7.round(3)
# df_L7 = df_L7[(df_L7['ISO'] >= input_iso) &
#                  (df_L7['K%'] <= input_kpct) &
#                  (df_L7['BB%'] >= input_bbpct)]
#df_L7 = df_L7.sort_values(by='OPS', ascending=False)
#df_L7['xPOPS'] = (df_L7['xSpect']*df_L7['OPS']).round(3)
#df_L7 = df_L7[df_L7['Org'].isin(orgs_choice)]
#df_L7 = df_L7[df_L7['Level'].isin(input_levels)]
#######################################################################
#######################################################################
df_L14['Name/Org'] = (df_L14['Name'] + " - " + df_L14['Org'])
df_L14['idk'] = ((2*df_L14['ISO'])+(df_L14['BB%']/2))**(((3*df_L14['K%'])*2)**df_L14['BABIP']).round(3)
df_L14['xSpect'] = (df_L14['ISO']/(df_L14['K%']*2)).round(3)
df_L14 = df_L14.filter(cols_time, axis=1)
#df_L14 = df_L14[(df_L14['Age'] <= input_age)]
#df_L14 = df_L14[(df_L14['PA'] >= input_pa_curr)]
df_L14 = df_L14.round(3)
# df_L14 = df_L14[(df_L14['ISO'] >= input_iso) &
#                  (df_L14['K%'] <= input_kpct) &
#                  (df_L14['BB%'] >= input_bbpct)]
#df_L14 = df_L14.sort_values(by='OPS', ascending=False)
#df_L14['xPOPS'] = (df_L14['xSpect']*df_L14['OPS']).round(3)
#df_L14 = df_L14[df_L14['Org'].isin(orgs_choice)]
#df_L14 = df_L14[df_L14['Level'].isin(input_levels)]
#######################################################################
#######################################################################
df_recent['Name/Org'] = (df_recent['Name'] + " - " + df_recent['Org'])
df_recent['idk'] = ((2*df_recent['ISO'])+(df_recent['BB%']/2))**(((3*df_recent['K%'])*2)**df_recent['BABIP']).round(3)
df_recent['xSpect'] = (df_recent['ISO']/(df_recent['K%']*2)).round(3)
df_recent = df_recent.filter(cols_time, axis=1)
#df_recent = df_recent[(df_recent['Age'] <= input_age)]
#df_recent = df_recent[(df_recent['PA'] >= input_pa_curr)]
df_recent = df_recent.round(3)
# df_recent = df_recent[(df_recent['ISO'] >= input_iso) &
#                  (df_recent['K%'] <= input_kpct) &
#                  (df_recent['BB%'] >= input_bbpct)]
#df_recent = df_recent.sort_values(by='OPS', ascending=False)
#df_recent['xPOPS'] = (df_recent['xSpect']*df_recent['OPS']).round(3)
#df_recent = df_recent[df_recent['Org'].isin(orgs_choice)]
#df_recent = df_recent[df_recent['Level'].isin(input_levels)]
#######################################################################


# utilize the datediff variable in the jupyter notebook to set the X in the subheader
#st.write('Select a row from the 2022 stats to see all MiLB seasons with a higher ISO and walk rate, and lower strikeout rate since 2006 in the second table')
#st.caption('For the purposes of this app, season is defined as a stint with one Minor League team with at least 70 PA')

search_input = st.text_input(label='Search for a player')
search_submit = st.checkbox('Submit search')

#@st.cache(allow_output_mutation=True)
def player_search(search_input):
    if player_search != '':
        dfcurr3 = dfcurr[dfcurr['Name'].str.contains(search_input)]

if search_submit: 
    dfcurr3 = dfcurr[dfcurr['Name'].str.contains(search_input)]
    gdsearch = GridOptionsBuilder.from_dataframe(dfcurr3)
    gdsearch.configure_pagination(enabled=True)
    gdsearch.configure_default_column(editable=True, groupable=True)
    gdsearch.configure_selection(selection_mode='single', use_checkbox=True, pre_selected_rows=[0])
    gridoptionssearch = gdsearch.build()
    grid_table_search = AgGrid(dfcurr3, gridOptions=gridoptionssearch,
                        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                        allow_unsafe_jscode=True,
                        height = 150,
                        enable_enterprise_modules = True,
                        theme='blue')
    sel_row = grid_table_search["selected_rows"]


#######################################################################
#### --- THE FIRST DATA TABLE ----------------------------------- #####
# configure grid options for Ag-Grid table
if search_submit:
    st.write('Uncheck "Submit search" to clear search results')
    gd = GridOptionsBuilder.from_dataframe(dfcurr2)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True, groupable=True)
    gd.configure_selection(selection_mode='single', use_checkbox=True, pre_selected_rows=[0])
    gridoptions1 = gd.build()
    grid_table = AgGrid(dfcurr2, gridOptions=gridoptions1,
                        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                        height=530,
                        allow_unsafe_jscode=True,
                        enable_enterprise_modules = True,
                        theme='blue')
    sel_row = grid_table["selected_rows"]
    if sel_row == "":
        st.spinner('Select a player')
    else:
        df_sel = pd.DataFrame(sel_row)
        st.subheader("Selected player: " + df_sel['Name/Org'].iloc[0] + ' | Level: ' + df_sel['Level'].iloc[0])
        #st.table(df_sel)

        sel_iso = df_sel['ISO'].iloc[0]
        sel_kpct = df_sel['K%'].iloc[0]
        sel_bbpct = df_sel['BB%'].iloc[0]
        sel_wrcplus = df_sel['wRC+'].iloc[0]
        sel_age = df_sel['Age'].iloc[0].astype(int)
        sel_level = df_sel['Level'].iloc[0]
        sel_swstrpct = df_sel['SwStr%'].iloc[0]
        
        sel_buff_iso = (sel_iso - input_buffer_iso).round(3)
        sel_buff_kpct = (sel_kpct + input_buffer_kpct).round(3)
        sel_buff_bbpct = (sel_bbpct - input_buffer_bbpct).round(3)
        #sel_buff_age = sel_age + 1
        #sel_buff_level = sel_level + 1
        #sel_buff_swstrpct = sel_swstrpct - input_buffer_other
        #sel_days = df_sel['Days'].iloc[0]
        #st.subheader("Last " + sel_days + " days")
        # sel_id = df_sel.id[0]
        # df_sel_recent = df_recent.loc[[sel_id]]
        # df_sel_L7 = df_L7.loc[[sel_id]]
        # df_sel_L7['Days'] = df_L7.Days[0]
        # df_sel_L7.set_index('Days', inplace=True)
        # df_sel_L14 = df_L14.loc[[sel_id]]
        # df_sel_L14['Days'] = df_L14.Days[0]
        # df_sel_L14.set_index('Days', inplace=True)
        # df_sel_recent['Days'] = df_recent.Days[0]
        # df_sel_recent.set_index('Days', inplace=True)
        # #df_sel_curr = dfcurr2.loc[[sel_id]]
        # frames = [df_sel_L7, df_sel_L14, df_sel_recent]
        # result = pd.concat(frames)
        # st.write('Last 7')
        # st.table(df_sel_L7)
        # st.write('Last 14')
        # st.table(df_sel_L14)
        # st.write('Last ' + str(df_recent.Days[0]))
        #st.table(result)
        
        # st.write('Level Total')
        # st.table(df_sel_curr)

        sel_id = df_sel.id[0]

        l7idx = df_L7.index.values.tolist()
        l14idx = df_L14.index.values.tolist()
        recentidx = df_recent.index.values.tolist()
        allidx = l7idx + l14idx + recentidx

        if sel_id in df_L7.index.values:
            df_sel_L7 = df_L7.loc[[sel_id]]
            df_sel_L7['Days'] = df_L7['Days'][0]
            df_sel_L7['Days'] = 'Last ' + df_sel_L7['Days'].astype(str)
            df_sel_L7.set_index('Days', inplace=True)
        else: 
            df_sel_L7 = pd.DataFrame({}, columns=df_L7.columns, index = ['Days'])

        if sel_id in df_L14.index.values:
            df_sel_L14 = df_L14.loc[[sel_id]]
            df_sel_L14['Days'] = df_L14['Days'][0]
            df_sel_L14['Days'] = 'Last ' + df_sel_L14['Days'].astype(str)
            df_sel_L14.set_index('Days', inplace=True)
        else:
            df_sel_L14 = pd.DataFrame({}, columns=df_L14.columns, index = ['Days'])

        if sel_id in df_recent.index.values:
            df_sel_recent = df_recent.loc[[sel_id]]
            df_sel_recent['Days'] = df_recent['Days'][0]
            df_sel_recent['Days'] = 'Last ' + df_sel_recent['Days'].astype(str)
            df_sel_recent.set_index('Days', inplace=True)
        else:
            df_sel_recent = pd.DataFrame({}, columns=df_recent.columns, index = ['Days'])

        if sel_id in allidx:
            frames = [
                df_sel_L7,
                df_sel_L14,
                df_sel_recent
                ]
            result = pd.concat(frames)
            result2 = result.drop(columns=['Name/Org', 'Age', 'Level', 'id'])
            result2['Split'] = result2.index
            # shift column 'Name' to first position
            first_column = result2.pop('Split')
            
            # insert column using insert(position,column_name,
            # first_column) function
            result2.insert(0, 'Split', first_column)
            # CONFIGURE GRID OPTIONS ###############################################
            gb2 = GridOptionsBuilder.from_dataframe(result2)
            gb2.configure_default_column(min_column_width = .1)
            gridoptions3 = gb2.build()

            AgGrid(
                result2,
                gridOptions=gridoptions3,
                height=100,
                enable_enterprise_modules=True,
                theme = "blue"
            )
            dfhist3 = dfhist2[
                (dfhist2['ISO'] >= sel_buff_iso) &
                (dfhist2['K%'] <= sel_buff_kpct) &
                (dfhist2['BB%'] >= sel_buff_bbpct) &
                (dfhist2['Age'] <= sel_age)
            ]       
            dfhist3 = dfhist3.sort_values(by='level_code', ascending=False)
            # CONFIGURE GRID OPTIONS ###############################################
            gb = GridOptionsBuilder.from_dataframe(dfhist3)
            gb.configure_pagination(enabled=True)
            gb.configure_side_bar()
            gb.configure_default_column(min_column_width = .1, groupable=True, value=True, enableRowGroup=True, aggFunc="mean", editable=True)
            gridoptions2 = gb.build()
            AgGrid(
                dfhist3,
                gridOptions=gridoptions2,
                height=530,
                enable_enterprise_modules=True,
                theme = "blue"
        )   
        else:
            st.write('This player has not played during this period')

#### SETTING UP THE SELECTION ###########################################
# if sel_row == "":
#     st.spinner('Select a player')
# else:
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
#     # #df_sel_curr = dfcurr2.loc[[sel_id]]
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

#     l7idx = df_L7.index.values.tolist()
#     l14idx = df_L14.index.values.tolist()
#     recentidx = df_recent.index.values.tolist()
#     allidx = l7idx + l14idx + recentidx


#     if sel_id in df_L7.index.values:
#         df_sel_L7 = df_L7.loc[[sel_id]]
#         df_sel_L7['Days'] = df_L7['Days'][0]
#         df_sel_L7['Days'] = 'Last ' + df_sel_L7['Days'].astype(str)
#         df_sel_L7.set_index('Days', inplace=True)
#     else: 
#         df_sel_L7 = pd.DataFrame({}, columns=df_L7.columns, index = ['Days'])

#     if sel_id in df_L14.index.values:
#         df_sel_L14 = df_L14.loc[[sel_id]]
#         df_sel_L14['Days'] = df_L14['Days'][0]
#         df_sel_L14['Days'] = 'Last ' + df_sel_L14['Days'].astype(str)
#         df_sel_L14.set_index('Days', inplace=True)
#     else:
#         df_sel_L14 = pd.DataFrame({}, columns=df_L14.columns, index = ['Days'])

#     if sel_id in df_recent.index.values:
#         df_sel_recent = df_recent.loc[[sel_id]]
#         df_sel_recent['Days'] = df_recent['Days'][0]
#         df_sel_recent['Days'] = 'Last ' + df_sel_recent['Days'].astype(str)
#         df_sel_recent.set_index('Days', inplace=True)
#     else:
#         df_sel_recent = pd.DataFrame({}, columns=df_recent.columns, index = ['Days'])

#     if sel_id in allidx:
#         frames = [
#             df_sel_L7,
#             df_sel_L14,
#             df_sel_recent
#             ]
#         result = pd.concat(frames)
#         result2 = result.drop(columns=['Name/Org', 'Age', 'Level', 'id'])
#         result2['Split'] = result2.index
#         # shift column 'Name' to first position
#         first_column = result2.pop('Split')
        
#         # insert column using insert(position,column_name,
#         # first_column) function
#         result2.insert(0, 'Split', first_column)
#         # CONFIGURE GRID OPTIONS ###############################################
#         gb2 = GridOptionsBuilder.from_dataframe(result2)
#         gb2.configure_default_column(min_column_width = .1)
#         gridoptions3 = gb2.build()

#         AgGrid(
#             result2,
#             gridOptions=gridoptions3,
#             height=100,
#             enable_enterprise_modules=True,
#             theme = "blue"
#         )

#     else:
#         st.write('This player has not played during this period')


## FILTER THE HISTORIC TABLE BASED ON THE SELECTED PLAYER #############
## THIS WORKS WITHOUT THE BUFFERS #####################################
#dfhist3 = dfhist2[(dfhist2['iso'] >= sel_iso) & (dfhist2['kpct'] <= sel_kpct) & (dfhist2['bbpct'] >= sel_bbpct)]
#either above code or below code depending on whether or not the buffers are working -_- #

## FILTER THE HISTORIC TABLE BASED ON THE SELECTED PLAYER #############
## WITH BUFFERS #######################################################
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



# agree_hist = st.checkbox('Show historical data')

# if agree_hist:
#      AgGrid(dfhist3, gridOptions=gridOptions, enable_enterprise_modules=True, theme = "blue")

##################################################
#adding in some graphs and things of that nature
##################################################

#fig = plt.figure(figsize=(10, 4))
#sns.scatterplot(data = df, x = "Economy (GDP per Capita)", y = "Happiness Score")

#st.pyplot(fig)

#sns.scatterplot(data = dfhist3)