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

######################################################################################################
#### ---- LOAD DATAFRAMES ---- #######################################################################
@st.cache(allow_output_mutation=True)
def load_df_hist():
    URL1 = 'https://github.com/matt20/milbapp/blob/master/milb0621off_70pa.csv?raw=true'
    data1 = pd.read_csv(URL1,index_col = 'playeriduniquecount')
    return data1

df_hist = load_df_hist()

@st.cache(allow_output_mutation=True)
def load_df_raw():
    URL2 = 'https://github.com/matt20/milbapp/blob/master/dfraw.csv?raw=true'
    data2 = pd.read_csv(URL2, index_col = 'IndexNew')
    return data2

df_raw = load_df_raw()

#######################################################################################################

#st.dataframe(df_raw)

df_raw['IndexSplit'] = df_raw.PlayerID.astype(str) + '-' + df_raw.Level + '-' + df_raw.Org
df_raw['IndexSplit2'] = df_raw.PlayerID.astype(str) + '-' + df_raw.Level + '-' + df_raw.Org

def get_df_filter(date):
    return df_raw.loc[(df_raw['Date'].astype(str) == date)].copy()

dates = df_raw['Date'].unique()
dates2 = sorted(dates, 
                          key=lambda date: datetime.strptime(date, '%Y-%m-%d'), reverse=True)
date_max = dates2[0]

df_raw['DaysBack'] = ((df_raw.apply(lambda row: datetime.strptime(date_max, '%Y-%m-%d') - datetime.strptime(row['Date'], '%Y-%m-%d'), axis = 1)).dt.days).astype(int)

def get_df_filter_days(days):
    return df_raw.loc[(df_raw['DaysBack'] == days)].copy()

################################################################################################
#### SET UP COLUMNS ############################################################################

cols_count = ['G','AB','PA','H','1B','2B','3B','HR','R',
             'RBI','BB','IBB','SO','HBP','SF','SH','GDP',
             'SB','CS','IndexSplit'
             #,'Balls','Strikes','Pitches','wRC+']
]

cols_bio = ['Name','Org','Level','Age','IndexSplit','IndexSplit2','PlayerID'
            ]

cols_split_display = [
    'Name','Org','Age','Level','PA',
    'xSpect','ISO','K%','BB%',
    'OPS','BABIP','AVG','OBP','SLG',
    'HR','XBH','SB','CS','IndexSplit2','PlayerID'
]

cols_xyz = [
    'Name','Age','Level','PA',
    'wRC+','ISO','K%','BB%',
    'OPS','BABIP','AVG','OBP','SLG',
    'HR', '2B', '3B','SB','CS','IndexSplit2'
]

################################################################################################
#### USER INPUT FOR DATES ######################################################################

dates_choice_start = df_raw['Date'].unique()
dates_choice_start = sorted(dates_choice_start, 
                            key=lambda date: datetime.strptime(date, '%Y-%m-%d'))

dates_choice_end = df_raw['Date'].unique()
dates_choice_end = sorted(dates_choice_end, 
                          key=lambda date: datetime.strptime(date, '%Y-%m-%d'), reverse=True)

days_back_choice = df_raw['DaysBack'].unique()
days_back_choice = sorted(days_back_choice)

date_max = dates_choice_end[0]
df_date_max = get_df_filter(date_max)

date_min = dates_choice_start[0]
df_date_min = get_df_filter(date_min)

date_6 = dates_choice_end[6]
df_date_6 = get_df_filter(date_6)

date_12 = dates_choice_end[12]
df_date_12 = get_df_filter(date_12)

col1, col2, col3 = st.columns(3)

## COLUMNS AND SEARCH ############################################################################

with col1:
    date_start = st.selectbox(
    'Choose a starting date',
    (dates_choice_start))
    
    date_start_dt = datetime.strptime(date_start, '%Y-%m-%d') #string to date

with col2:
    date_end = st.selectbox(
    'Choose an ending date',
    (dates_choice_end))

    date_end_dt = datetime.strptime(date_end, '%Y-%m-%d') #string to date
    
with col3:
    days_back = st.selectbox(
        'How many days back?',
        (days_back_choice))
    days_submit = st.checkbox('Use days instead of date range')

################################################################################################
#### SET UP THE DATA FRAME BASED ON USER INPUT #################################################
### EXPERIMENTAL FILTERS #######################################################################
def get_df_count(df):
    return df.filter(cols_count, axis=1)

def df_to_int(df):
    for col in cols_count:
        df[col] = df[col].astype('int')
        return pd.DataFrame(df)

if days_submit:
    df_start = get_df_filter_days(days_back)

    df_end = get_df_filter(date_max)
else:
    df_start = get_df_filter(date_start)

    df_end = get_df_filter(date_end)

days_back_var = str(df_start.DaysBack[0])

def get_df_diff(dfEnd, dfStart):
    df_count_start = get_df_count(dfStart)
    df_count_end = get_df_count(dfEnd)

    df_count_start.set_index('IndexSplit', inplace=True)
    df_count_end.set_index('IndexSplit', inplace=True)

    df_count_start = df_to_int(df_count_start)    
    df_count_end = df_to_int(df_count_end)   

    df_diff = df_count_end.subtract(df_count_start, fill_value=0).astype(int)
    return df_diff[df_diff['PA'] > 0]
 

df_diff_input = get_df_diff(df_end, df_start)

################################################################################################
#### SETTING UP THE BIO DF TO MERGE BACK IN WITH THE SPLITS DATA ###############################

df_bio = df_date_max.filter(cols_bio, axis=1)
df_bio.set_index('IndexSplit', inplace=True)

def merge_with_bio(df):
    return pd.merge(df_bio, df, left_index=True, right_index=True)

df_splits = merge_with_bio(df_diff_input)

df_splits.sort_values(by=['PA'])

# pa_mean = (df_splits['PA'].mean()).astype(int)

splits_pa_max = int(df_splits['PA'].max())
#splits_pa_max = splits_pa_max_0

#### SIDEBAR ###########################################################
input_age = st.sidebar.slider('Max Age:', 16, 32, 20)
input_pa_min = st.sidebar.slider('Min PA (Splits):', 1, splits_pa_max, 1)
input_pa_max = st.sidebar.slider('Max PA (Splits):', 50, splits_pa_max, splits_pa_max)
input_kpct = st.sidebar.slider('Max K%:', .0, .400, .300)
input_iso = st.sidebar.slider('Min ISO:', .0, .400, .150)
input_bbpct = st.sidebar.slider('Min BB%:', .0, .25, .0)
input_wrcplus = st.sidebar.slider('Min wRC+:', 0, 200, 100)
# input_buffer_iso = st.sidebar.slider('ISO Buffer:', .0, .100, .0)
# input_buffer_kpct = st.sidebar.slider('K% Buffer:', .0, .100, .0)
# input_buffer_bbpct = st.sidebar.slider('BB% Buffer:', .0, .100, .0)
# input_pa_hist = st.sidebar.slider('Min PA (Hist):', 100, 400, 100)

################################################################################################
#### CALCULATING THE SPLIT RATIO STATS #########################################################

def calc_split_stats(df):
    df['BABIP'] = ((df.H-df.HR)/(df.AB-df.SO-df.HR+df.SF+df.SH)).round(3)
    df['AVG'] = (df.H/df.AB).round(3)
    df['OBP'] = ((df.H+df.BB+df.HBP)/df.PA).round(3)
    df['SLG'] = (((df['1B'])+(2*df['2B'])+(3*df['3B'])+(4*df.HR))/df.AB).round(3)
    df['ISO'] = (df.SLG - df.AVG).round(3)
    df['XBH'] = (df['2B']+df['3B']+df.HR).astype(int)
    df['K%'] = (df.SO/df.PA).round(3)
    df['BB%'] = (df.BB/df.PA).round(3)
    df['xSpect'] = (df.ISO/(2*df['K%'])).round(3)
    df['OPS'] = (df.OBP + df.SLG).round(3)
    df = df.filter(cols_split_display, axis=1)
    return df

def filter_by_input(df):
    return df[(df['ISO'] >= input_iso) &
                        (df['K%'] <= input_kpct) &
                        (df['BB%'] >= input_bbpct) &
                        (df['Age'] <= input_age) &
                        (df['PA'] >= input_pa_min) &
                        (df['PA'] <= input_pa_max)
    ]


df_splits_2 = calc_split_stats(df_splits)

df_splits_2 = filter_by_input(df_splits_2)

df_splits = df_splits.filter(cols_split_display, axis=1)
df_splits_2 = df_splits_2.filter(cols_split_display, axis=1)

# format_dict = {'K%': '{:.2%}', 'BB%': '{:.2%}'}
# df_splits_2.style.format(format_dict)

st.write('Last ' + days_back_var + ' days')

#######################################################################
#### --- THE FIRST DATA TABLE ----------------------------------- #####
# configure grid options for Ag-Grid table
gd = GridOptionsBuilder.from_dataframe(df_splits_2)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True, groupable=True)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gridoptions1 = gd.build()
grid_table = AgGrid(df_splits_2, gridOptions=gridoptions1,
                    update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                    height=435,
                    allow_unsafe_jscode=True,
                    enable_enterprise_modules=True,
                    theme='blue')

#### SETTING UP THE SELECTION ###########################################
sel_row = grid_table["selected_rows"]

if sel_row:
    df_sel = pd.DataFrame(sel_row)
    st.subheader("Selected player: " + df_sel['Name'].iloc[0] + ' - ' + df_sel['Org'].iloc[0] + ' | Level: ' + df_sel['Level'].iloc[0])
    #st.table(df_sel)

    sel_iso = df_sel['ISO'].iloc[0]
    sel_kpct = df_sel['K%'].iloc[0]
    sel_bbpct = df_sel['BB%'].iloc[0]
    sel_age = df_sel['Age'].iloc[0].astype(int)
    sel_level = df_sel['Level'].iloc[0]
    
    # sel_buff_iso = (sel_iso - input_buffer_iso).round(3)
    # sel_buff_kpct = (sel_kpct + input_buffer_kpct).round(3)
    # sel_buff_bbpct = (sel_bbpct - input_buffer_bbpct).round(3)
    #sel_buff_age = sel_age + 1
    #sel_buff_level = sel_level + 1
    #sel_buff_swstrpct = sel_swstrpct - input_buffer_other
    #sel_days = df_sel['Days'].iloc[0]
    #st.subheader("Last " + sel_days + " days")
    sel_id = df_sel.IndexSplit2[0]
    sel_pid = df_sel.PlayerID[0]
    
    sel_id_max = sel_id + '-' + date_max
    df_sel_date_max = df_date_max.loc[[sel_id_max]]
    df_sel_date_max_2 = df_sel_date_max.filter(cols_xyz, axis=1)
    st.dataframe(df_sel_date_max_2)
    frames = []
            
    sel_id_6 = sel_id + '-' + date_6
    if (sel_id in df_date_6['IndexSplit2'].values):
        df_sel_date_6 = df_date_6.loc[[sel_id_6]]
        df_sel_date_6_split = get_df_diff(df_sel_date_max, df_sel_date_6)
        df_sel_date_6_split = calc_split_stats(df_sel_date_6_split)
        frames = [df_sel_date_6_split]
    sel_id_12 = sel_id + '-' + date_12
    if (sel_id in df_date_12['IndexSplit2'].values):
        df_sel_date_12 = df_date_12.loc[[sel_id_12]]
        df_sel_date_12_split = get_df_diff(df_sel_date_max, df_sel_date_12)
        df_sel_date_12_split = calc_split_stats(df_sel_date_12_split)
        frames = [df_sel_date_6_split, df_sel_date_12_split]
    df_sel_all_dates = df_raw[df_raw['PlayerID'].str.contains(sel_pid)]
    df_sel_all_dates = df_sel_all_dates.sort_values(by=['G'],ascending=False)
    # df_sel_all_dates = df_sel_all_dates.loc[:,~df_sel_all_dates.columns.duplicated()]
    df_sel_all_dates_2 = df_sel_all_dates.filter(cols_xyz, axis=1)
    #st.dataframe(df_sel_all_dates_2)
    # fig = plt.figure()
    
    # plt.scatter(df_sel_all_dates, y = df_sel_all_dates['wRC+'], x = df_sel_all_dates['Date'])
    # st.write(fig)
    #fig = plt.figure()
    # sns.scatterplot(df_sel_all_dates, y = df_sel_all_dates.ISO) 
    # st.pyplot(fig)   
    # df_sel_date_12['Days'] = df_date_12.Days[0]
    # df_sel_date_12.set_index('Days', inplace=True)
    # df_sel_date_max['Days'] = df_date_max.Days[0]
    # df_sel_date_max.set_index('Days', inplace=True)
    # #df_sel_curr = df_raw2.loc[[sel_id]]
    # frames = [df_sel_date_6_split, df_sel_date_12_split] #df_sel_date_max]
    
    if len(frames) > 0: 
        result = pd.concat(frames)
        st.table(result)
    
    st.dataframe(df_sel_all_dates_2)








#### SEARCH FUNCTION ###################################################

search_input = st.text_input(label='Search for a player')
search_submit = st.checkbox('Submit search')

#@st.cache(allow_output_mutation=True)
def player_search(search_input):
    if player_search != '':
        df_splits_search = df_splits[df_splits['Name'].str.contains(search_input)]
        df_total_search = df_date_max[df_date_max['Name'].str.contains(search_input)]
        df_total_search = df_total_search.filter(cols_split_display, axis=1)

if search_submit:
    st.write('Search results time split:')
    df_splits_search = df_splits[df_splits['Name'].str.contains(search_input)]
    gdsearch = GridOptionsBuilder.from_dataframe(df_splits_search)
    gdsearch.configure_pagination(enabled=True)
    gdsearch.configure_default_column(editable=True, groupable=True)
    #gdsearch.configure_selection(selection_mode='single', use_checkbox=True, pre_selected_rows=[0])
    gridoptions_search = gdsearch.build()
    grid_table_search = AgGrid(df_splits_search, gridOptions=gridoptions_search,
                        #update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                        allow_unsafe_jscode=True,
                        height = 150,
                        enable_enterprise_modules = True,
                        theme='blue')
    #sel_row = grid_table_search["selected_rows"]
    
    st.write('Search results season totals:')
    df_total_search = df_date_max[df_date_max['Name'].str.contains(search_input)]
    df_total_search = df_total_search.filter(cols_split_display, axis=1)
    gdsearch_total = GridOptionsBuilder.from_dataframe(df_total_search)
    gdsearch_total.configure_pagination(enabled=True)
    gdsearch_total.configure_default_column(editable=True, groupable=True)
    #gdsearch_total.configure_selection(selection_mode='single', use_checkbox=True, pre_selected_rows=[0])
    gridoptions_search_total = gdsearch_total.build()
    grid_table_search = AgGrid(df_total_search, gridOptions=gridoptions_search_total,
                        #update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                        allow_unsafe_jscode=True,
                        height = 150,
                        enable_enterprise_modules = True,
                        theme='blue')
    #sel_row = grid_table_search["selected_rows"]

#### ADD SOME VARIABLES #################################################
df_hist['level_code'] = df_hist['level'].map({
    "AAA": 8,
    "AA": 7,
    "A+": 6,
    "A": 5,
    "A-": 4,
    "CPX": 1,
    "R": 1,
    "DSL": 1,
})

df_hist['Name/Org'] = df_hist['name'] + '-' + df_hist['team']

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
# df_hist['xSpect'] = (df_hist['iso']/(df_hist['kpct']+df_hist['swstrpct'])).round(3)
# df_hist['Name/Org/Year'] = df_hist['name'] + ' - ' + df_hist['team'] + ' - ' + (df_hist['season']).astype(str)
# df_hist['OPS'] = (df_hist['obp'] + df_hist['slg']).round(3)
# df_hist = df_hist[cols_hist]
# df_hist = df_hist[(df_hist['age'] <= input_age)]
# df_hist = df_hist[(df_hist['pa'] >= input_pa_hist)]
# #df_hist = df_hist[df_hist['level'].isin(input_levels)]
# df_hist['wrcplus'] = df_hist['wrcplus'].round(0)
# df_hist2 = df_hist[(df_hist['iso'] >= input_iso) &
#                  (df_hist['kpct'] <= input_kpct) &
#                  (df_hist['bbpct'] >= input_bbpct) &
#                  (df_hist['wrcplus'] >= input_wrcplus)]
# df_hist2.columns = cols_hist_display
# df_hist2.sort_values(by='wRC+', ascending=False)
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
#     # df_sel_date_max = df_date_max.loc[[sel_id]]
#     # df_sel_date_6 = df_date_6.loc[[sel_id]]
#     # df_sel_date_6['Days'] = df_date_6.Days[0]
#     # df_sel_date_6.set_index('Days', inplace=True)
#     # df_sel_date_12 = df_date_12.loc[[sel_id]]
#     # df_sel_date_12['Days'] = df_date_12.Days[0]
#     # df_sel_date_12.set_index('Days', inplace=True)
#     # df_sel_date_max['Days'] = df_date_max.Days[0]
#     # df_sel_date_max.set_index('Days', inplace=True)
#     # #df_sel_curr = df_raw2.loc[[sel_id]]
#     # frames = [df_sel_date_6, df_sel_date_12, df_sel_date_max]
#     # result = pd.concat(frames)
#     # st.write('Last 7')
#     # st.table(df_sel_date_6)
#     # st.write('Last 14')
#     # st.table(df_sel_date_12)
#     # st.write('Last ' + str(df_date_max.Days[0]))
#     #st.table(result)
    
#     # st.write('Level Total')
#     # st.table(df_sel_curr)


#     sel_id = df_sel.id[0]


# # if sel_id in df_date_6.index.values:
# #     df_sel_date_6 = df_date_6.loc[[sel_id]]
# #     df_sel_date_6['Days'] = df_date_6['Days'][0]
# #     df_sel_date_6['Days'] = 'Last ' + df_sel_date_6['Days'].astype(str)
# #     df_sel_date_6.set_index('Days', inplace=True)
# # else: 
# #     df_sel_date_6 = pd.DataFrame({}, columns=df_date_6.columns, index = ['Days'])

# # if sel_id in df_date_12.index.values:
# #     df_sel_date_12 = df_date_12.loc[[sel_id]]
# #     df_sel_date_12['Days'] = df_date_12['Days'][0]
# #     df_sel_date_12['Days'] = 'Last ' + df_sel_date_12['Days'].astype(str)
# #     df_sel_date_12.set_index('Days', inplace=True)
# # else:
# #     df_sel_date_12 = pd.DataFrame({}, columns=df_date_12.columns, index = ['Days'])

# # if sel_id in df_date_max.index.values:
# #     df_sel_date_max = df_date_max.loc[[sel_id]]
# #     df_sel_date_max['Days'] = df_date_max['Days'][0]
# #     df_sel_date_max['Days'] = 'Last ' + df_sel_date_max['Days'].astype(str)
# #     df_sel_date_max.set_index('Days', inplace=True)
# # else:
# #     df_sel_date_max = pd.DataFrame({}, columns=df_date_max.columns, index = ['Days'])

# # if sel_id in allidx:
# #     frames = [
# #         df_sel_date_6,
# #         df_sel_date_12,
# #         df_sel_date_max
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
# #df_hist3 = df_hist2[(df_hist2['iso'] >= sel_iso) & (df_hist2['kpct'] <= sel_kpct) & (df_hist2['bbpct'] >= sel_bbpct)]
# #either above code or below code depending on whether or not the buffers are working -_- #

# ## FILTER THE HISTORIC TABLE BASED ON THE SELECTED PLAYER #############
# ## WITH BUFFERS #######################################################
# df_hist3 = df_hist2[
#     (df_hist2['ISO'] >= sel_buff_iso) &
#     (df_hist2['K%'] <= sel_buff_kpct) &
#     (df_hist2['BB%'] >= sel_buff_bbpct) &
#     (df_hist2['Age'] <= sel_age)
# ]
          
# df_hist3 = df_hist3.sort_values(by='level_code', ascending=False)

# # CONFIGURE GRID OPTIONS ###############################################
# gb = GridOptionsBuilder.from_dataframe(df_hist3)
# gb.configure_pagination(enabled=True)
# gb.configure_side_bar()

# gb.configure_default_column(min_column_width = .1, groupable=True, value=True, enableRowGroup=True, aggFunc="mean", editable=True)
# gridoptions2 = gb.build()

# AgGrid(
#     df_hist3,
#     gridOptions=gridoptions2,
#     height=530,
#     enable_enterprise_modules=True,
#     theme = "blue"
# )
