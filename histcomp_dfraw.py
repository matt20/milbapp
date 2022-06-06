import pandas as pd
import streamlit as st
import plotly.express as px
from st_aggrid import AgGrid,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype
from datetime import datetime, timedelta

#### SET UP THE ACTUAL PAGE ###########################################
st.set_page_config(
    page_title='MiLB Splits Tool', 
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
def load_df_raw():
    URL2 = 'https://github.com/matt20/milbapp/blob/master/dfraw.csv?raw=true'
    data2 = pd.read_csv(URL2, index_col = 'IndexNew')
    return data2

df_raw = load_df_raw()

df_raw['IndexSplit'] = df_raw.PlayerID.astype(str) + '-' + df_raw.Level + '-' + df_raw.Org

################################################################################################
#### SET UP COLUMNS ############################################################################

# cols_clean = ['Name','Org','Level','Age','PlayerID',
#              'PlayerIDLevel','Date','PlayerIDUnique',
#              'G','AB','PA','H','1B','2B','3B','HR','R',
#              'RBI','BB','IBB','SO','HBP','SF','SH','GDP',
#              'SB','CS','Balls','Strikes','Pitches','BB%',
#              'K%','BB/K','AVG','OBP','SLG','OPS','ISO',
#              'BABIP','wSB','wRC','wRAA','wOBA','wRC+',
#              'GB/FB','LD%','GB%','FB%','IFFB%','HR/FB',
#              'Pull%','Cent%','Oppo%','SwStr%']

cols_count = ['G','AB','PA','H','1B','2B','3B','HR','R',
             'RBI','BB','IBB','SO','HBP','SF','SH','GDP',
             'SB','CS','IndexSplit'
             #,'Balls','Strikes','Pitches','wRC+']
]

cols_bio = ['Name','Org','Level','Age','IndexSplit'
            ]

cols_split_display = [
    'Name','Org','Age','Level','PA',
    'xSpect','ISO','K%','BB%',
    'OPS','BABIP','AVG','OBP','SLG',
    'HR','XBH','SB','CS'
]

################################################################################################
#### USER INPUT FOR DATES ######################################################################
dates_choice_start = df_raw['Date'].unique()
dates_choice_start = sorted(dates_choice_start, 
                            key=lambda date: datetime.strptime(date, '%Y-%m-%d'))

date_start = st.selectbox(
    'Choose a starting date',
    (dates_choice_start)
)

date_start_dt = datetime.strptime(date_start, '%Y-%m-%d') #string to date


dates_choice_end = df_raw['Date'].unique()
dates_choice_end = sorted(dates_choice_end, 
                          key=lambda date: datetime.strptime(date, '%Y-%m-%d'), reverse=True)

date_end = st.selectbox(
    'Choose an ending date',
    (dates_choice_end)
)

date_end_dt = datetime.strptime(date_end, '%Y-%m-%d') #string to date

date_diff = date_end_dt - date_start_dt
date_diff_str = str(date_diff.days)
st.write(date_diff_str)

################################################################################################
#### SET UP THE DATA FRAME BASED ON USER INPUT #################################################

# @st.cache(allow_output_mutation=True)
def get_df_filter(date):
    return df_raw.loc[(df_raw['Date'].astype(str) == date)].copy()

df_start = get_df_filter(date_start)

df_end = get_df_filter(date_end)

#st.dataframe(df_start)

# @st.cache(allow_output_mutation=True)
def get_df_count(df):
    return df.filter(cols_count, axis=1)

df_count_start = get_df_count(df_start)
df_count_end = get_df_count(df_end)

#st.dataframe(df_count_end)

df_count_start.set_index('IndexSplit', inplace=True)
df_count_end.set_index('IndexSplit', inplace=True)

# def get_df_diff(dfEnd, dfStart):
#     return dfEnd.subtract(dfStart, axis = 0, fill_value=0)

# df_diff = get_df_diff(df_count_end, df_count_start)

#st.dataframe(df_diff)

def df_to_int(df):
    for col in cols_count:
        df[col] = df[col].astype('int')
        return pd.DataFrame(df)
        
df_count_start = df_to_int(df_count_start)    
df_count_end = df_to_int(df_count_end)   

# st.dataframe(df_count_end)
# st.dataframe(df_count_start)
# st.dataframe(df_count_end.sort_values(by=['PA'], ascending=False))
# st.dataframe(df_count_end.sort_values(by=['PA'], ascending=False))
#st.dataframe(df_diff)
dfhmm2 = df_count_end.subtract(df_count_start, fill_value=0).astype(int)
dfhmm3 = dfhmm2[dfhmm2['PA'] > 0]
# pa_mean = dfhmm3['PA'].mean()
# dfhmm4 = dfhmm3[dfhmm3['PA'] < (2.5*pa_mean)]
# st.dataframe(dfhmm.sort_values(by='PA', ascending=False))

# hmmstart = pd.DataFrame(df_count_start, index = ['sa3004142-A+-TEX'])
# hmmstart2  = df_start[df_start['Name'].str.contains('Seise')]
# hmmraw  = df_raw[df_raw['Name'].str.contains('Seise')]
# hmmstart3  = df_start[(df_start['Org'].str.contains('TEX')) & (df_start['Level'] == "A+")]
# hmmend = pd.DataFrame(df_count_end, index = ['sa3004142-A+-TEX'])

# st.dataframe(hmmstart)
# st.dataframe(hmmraw)
# st.dataframe(hmmstart3)
# st.dataframe(hmmend)
# st.dataframe(dfhmm2.sort_values(by=['PA'], ascending=False))
# st.write(dfhmm2.shape)
# st.write(df_count_start.shape)
# st.write(df_count_end.shape)
#st.dataframe(dfhmm2.sort_values(by=['PA'], ascending=False))

################################################################################################
#### SETTING UP THE BIO DF TO MERGE BACK IN WITH THE SPLITS DATA ###############################

date_max = dates_choice_end[0]
df_recent = get_df_filter(date_max)

df_bio = df_recent.filter(cols_bio, axis=1)
df_bio.set_index('IndexSplit', inplace=True)

df_splits = pd.merge(df_bio, dfhmm3, left_index=True, right_index=True)

df_splits.sort_values(by=['PA'])

# pa_max = (df_splits['PA'].max()).astype(int)
# pa_mean = (df_splits['PA'].mean()).astype(int)

hmm = df_splits['PA'].max()
hmm2 = int(hmm)
pa_max = hmm2
pa_mean = 10

st.write(pa_mean)
#### SIDEBAR ###########################################################
input_age = st.sidebar.slider('Max Age:', 16, 32, 20)
input_pa_min = st.sidebar.slider('Min PA (Splits):', 1, pa_max, 1)
input_pa_max = st.sidebar.slider('Max PA (Splits):', 50, pa_max, pa_max)
input_kpct = st.sidebar.slider('Max K%:', .0, .400, .300)
input_iso = st.sidebar.slider('Min ISO:', .0, .400, .150)
input_bbpct = st.sidebar.slider('Min BB%:', .0, .25, .05)
input_wrcplus = st.sidebar.slider('Min wRC+:', 0, 200, 100)
# input_buffer_iso = st.sidebar.slider('ISO Buffer:', .0, .100, .0)
# input_buffer_kpct = st.sidebar.slider('K% Buffer:', .0, .100, .0)
# input_buffer_bbpct = st.sidebar.slider('BB% Buffer:', .0, .100, .0)
# input_pa_hist = st.sidebar.slider('Min PA (Hist):', 100, 400, 100)


################################################################################################
#### CALCULATING THE SPLIT RATIO STATS #########################################################

df_splits['BABIP'] = ((df_splits.H-df_splits.HR)/(df_splits.AB-df_splits.SO-df_splits.HR+df_splits.SF+df_splits.SH)).round(3)
df_splits['AVG'] = (df_splits.H/df_splits.AB).round(3)
df_splits['OBP'] = ((df_splits.H+df_splits.BB+df_splits.HBP)/df_splits.PA).round(3)
df_splits['SLG'] = (((df_splits['1B'])+(2*df_splits['2B'])+(3*df_splits['3B'])+(4*df_splits.HR))/df_splits.AB).round(3)
df_splits['ISO'] = (df_splits.SLG - df_splits.AVG).round(3)
df_splits['XBH'] = (df_splits['2B']+df_splits['3B']+df_splits.HR).astype(int)
df_splits['K%'] = (df_splits.SO/df_splits.PA).round(3)
df_splits['BB%'] = (df_splits.BB/df_splits.PA).round(3)
df_splits['xSpect'] = (df_splits.ISO/(2*df_splits['K%'])).round(3)
df_splits['OPS'] = (df_splits.OBP + df_splits.SLG).round(3)
#df_splits['days'] = pd.to_numeric(datediffstr)
df_splits = df_splits[(df_splits['ISO'] >= input_iso) &
                      (df_splits['K%'] <= input_kpct) &
                      (df_splits['BB%'] >= input_bbpct) &
                      (df_splits['Age'] <= input_age) &
                      (df_splits['PA'] >= input_pa_min) &
                      (df_splits['PA'] <= input_pa_max)
]



df_splits = df_splits.filter(cols_split_display, axis=1)
st.dataframe(df_splits.sort_values(by=['PA'], ascending = False))

search_input = st.text_input(label='Search for a player')
search_submit = st.checkbox('Submit search')

#@st.cache(allow_output_mutation=True)
def player_search(search_input):
    if player_search != '':
        df_splits3 = df_splits[df_splits['Name'].str.contains(search_input)]

if search_submit: 
    df_splits3 = df_splits[df_splits['Name'].str.contains(search_input)]
    gdsearch = GridOptionsBuilder.from_dataframe(df_splits3)
    gdsearch.configure_pagination(enabled=True)
    gdsearch.configure_default_column(editable=True, groupable=True)
    gdsearch.configure_selection(selection_mode='single', use_checkbox=True, pre_selected_rows=[0])
    gridoptionssearch = gdsearch.build()
    grid_table_search = AgGrid(df_splits3, gridOptions=gridoptionssearch,
                        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                        allow_unsafe_jscode=True,
                        height = 150,
                        enable_enterprise_modules = True,
                        theme='blue')
    sel_row = grid_table_search["selected_rows"]

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
# df_raw['Name/Org'] = (df_raw['Name'] + " - " + df_raw['Org'])
# df_raw['XBH'] = df_raw['2B'] + df_raw['3B'] + df_raw['HR']
# df_raw['idk'] = ((2*df_raw['ISO'])+(df_raw['BB%']/2))**(((3*df_raw['K%'])+df_raw['SwStr%'])**df_raw['BABIP']).round(3)
# df_raw['xSpect'] = (df_raw['ISO']/(df_raw['K%']+df_raw['SwStr%'])).round(3)
# df_raw2 = df_raw.filter(cols_curr, axis=1)
# df_raw2 = df_raw2[(df_raw2['Age'] <= input_age)]
# df_raw2 = df_raw2[(df_raw2['PA'] >= input_pa_curr)]
# df_raw2 = df_raw2.round(3)
# df_raw2['wRC+'] = df_raw2['wRC+'].round(0)
# df_raw2 = df_raw2[(df_raw2['ISO'] >= input_iso) &
#                  (df_raw2['K%'] <= input_kpct) &
#                  (df_raw2['BB%'] >= input_bbpct) &
#                  (df_raw2['wRC+'] >= input_wrcplus)]
# df_raw2 = df_raw2.sort_values(by='wRC+', ascending=False)
# #######################################################################

# #######################################################################
# #### --- THE FIRST DATA TABLE ----------------------------------- #####
# # configure grid options for Ag-Grid table
# gd = GridOptionsBuilder.from_dataframe(df_raw2)
# gd.configure_pagination(enabled=True)
# gd.configure_default_column(editable=True, groupable=True)
# gd.configure_selection(selection_mode='single', use_checkbox=True, pre_selected_rows=[0])
# gridoptions1 = gd.build()
# grid_table = AgGrid(df_raw2, gridOptions=gridoptions1,
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
#     # #df_sel_curr = df_raw2.loc[[sel_id]]
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
