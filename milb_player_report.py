import pandas as pd
import streamlit as st
# import plotly.express as px
from st_aggrid import AgGrid,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_option_menu import option_menu
# import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype
from datetime import datetime, timedelta

#### SET UP THE ACTUAL PAGE ###########################################
st.set_page_config(
    page_title='MiLB Offensive Player Report', 
    layout="wide",
    initial_sidebar_state="expanded"
)

######################################################################################################
#### ---- LOAD DATAFRAMES ---- #######################################################################
with st.spinner('Loading data...'):
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
    df_hist['PlayerID'] = df_hist.index

    #######################################################################################################

    #st.dataframe(df_raw)

    df_raw['IndexSplit'] = df_raw.PlayerID.astype(str) + '-' + df_raw.Level + '-' + df_raw.Org
    df_raw['IndexSplit2'] = df_raw.PlayerID.astype(str) + '-' + df_raw.Level + '-' + df_raw.Org

    def get_df_filter(date):
        return df_raw.loc[(df_raw['Date'].astype(str) == date)].copy()
    
    def get_df_filter_days(days):
        return df_raw.loc[(df_raw['DaysBack'] == days)].copy()

    dates = df_raw['Date'].unique()
    dates2 = sorted(dates, 
                            key=lambda date: datetime.strptime(date, '%Y-%m-%d'), reverse=True)
    date_max = dates2[0]

    df_raw['DaysBack'] = ((df_raw.apply(lambda row: datetime.strptime(date_max, '%Y-%m-%d') - datetime.strptime(row['Date'], '%Y-%m-%d'), axis = 1)).dt.days).astype(int)

    def get_df_filter_days(days):
        return df_raw.loc[(df_raw['DaysBack'] == days)].copy()

################################################################################################
#### SET UP COLUMNS ############################################################################

cols_count = [
    'G','AB','PA','H','1B','2B','3B','HR','R',
    'RBI','BB','IBB','SO','HBP','SF','SH',
    'GDP','SB','CS','IndexSplit'
#   ,'Balls','Strikes','Pitches','wRC+']
]

cols_bio = [
    'Name','Org','Level','Age','IndexSplit',
    'IndexSplit2','PlayerID'
            ]

cols_split_display = [
    'Name','Org','Age','Level','PA',
    'xSpect','ISO','K%','BB%',
    'OPS','BABIP','AVG','OBP','SLG',
    'HR','XBH','SB','CS','IndexSplit2','PlayerID'
]

cols_xyz = [
    'Name','Age','Level','PA',
    'wRC+','ISO','K%','BB%','SwStr%',
    'OPS','BABIP','AVG','OBP','SLG',
    'HR', '2B', '3B','SB','CS',
    'FB%', 'LD%', 'GB%', 'HR/FB',
    'IndexSplit2'
]

cols_hist_clean = [
    'Name', 'Org', 'Level', 'Age', 'Season',
    'PA', 'HR', 'SB', 'CS', 'ISO', 'SwStr%',
    'K%','BB%','BABIP','AVG','OBP','SLG',
    'wRC+','HR/FB','FB%','LD%','GB%','Pull%',
    'Cent%','Oppo%','PlayerID'
]

cols_hist_num = [
    'ISO', 'SwStr%',
    'K%','BB%','BABIP','AVG','OBP','SLG',
    'HR/FB','FB%','LD%','GB%','Pull%',
    'Cent%','Oppo%',
]

cols_hist_display = [
    'Name','Org','Season','Age','Level','PA',
    'wRC+','ISO','K%','BB%','SwStr%',
    'OPS','BABIP','AVG','OBP','SLG',
    'HR','XBH','HR/FB','SB','CS','PlayerID'
]

cats_sel_display = [
    'PA','wRC+','ISO','K%','BB%','SwStr%',
    'OPS','BABIP','AVG','OBP','SLG',
    'HR','XBH','SB','CS',
    'FB%','LD%','GB%',
    'PlayerID'
]

df_hist.columns = cols_hist_clean

for col in cols_hist_num:
    df_hist[col] = pd.to_numeric(df_hist[col], errors='coerce').round(3)

df_hist['wRC+'] = df_hist['wRC+'].astype(int).round(0)
df_raw['wRC+'] = df_raw['wRC+'].astype(int).round(0)

df_hist_recent = df_hist[df_hist['Season'] > 2014]

levels = df_raw['Level'].unique()

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

## COLUMNS AND SEARCH ############################################################################
# col1, col2, col3 = st.columns(3)

# with col1:
#     date_start = st.selectbox(
#     'Choose a starting date',
#     (dates_choice_start))
    
#     date_start_dt = datetime.strptime(date_start, '%Y-%m-%d') #string to date

# with col2:
#     date_end = st.selectbox(
#     'Choose an ending date',
#     (dates_choice_end))

#     date_end_dt = datetime.strptime(date_end, '%Y-%m-%d') #string to date
    
# with col3:
#     days_back = st.selectbox(
#         'How many days back?',
#         (days_back_choice))
#     days_submit = st.checkbox('Use days instead of date range')

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

df_date_max_display = df_date_max.filter(cols_xyz, axis=1)
#st.dataframe(df_date_max_display)
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
#### SIDEBAR ###########################################################
input_age = st.sidebar.slider('Max Age:', 16, 32, 20)
input_pa_min = st.sidebar.slider('Min PA (Splits):', 1, splits_pa_max, 1)
input_pa_max = st.sidebar.slider('Max PA (Splits):', 50, splits_pa_max, splits_pa_max)
input_kpct = st.sidebar.slider('Max K%:', .0, .500, .500)
input_iso = st.sidebar.slider('Min ISO:', .0, .400, .0)
input_bbpct = st.sidebar.slider('Min BB%:', .0, .25, .0)
input_wrcplus = st.sidebar.slider('Min wRC+:', 0, 200, 100)
input_levels = st.sidebar.multiselect(
     'Levels',
     levels,
     levels)
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
                        (df['PA'] <= input_pa_max) &
                        (df['Level'].isin(input_levels))
    ]


df_splits_2 = calc_split_stats(df_splits)

df_splits_2 = filter_by_input(df_splits_2)

df_splits = df_splits.filter(cols_split_display, axis=1)
df_splits_2 = df_splits_2.filter(cols_split_display, axis=1)

# format_dict = {'K%': '{:.2%}', 'BB%': '{:.2%}'}
# df_splits_2.style.format(format_dict)



# st.dataframe(df_hist_recent)
# st.write(df_hist.columns)

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

def get_time_graph(yvar, df, ymin, ymax):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter("PA", yvar, data = df)
    ax.plot("PA", yvar, data = df)
    ax.set_xlabel('PA')
    ax.set_ylabel(yvar)
    plt.ylim([ymin, ymax])
    output = st.write(fig)
    return output

def get_time_graph_hrsb(df, ymin, ymax):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter("PA", "HR", data = df)
    ax.plot("PA", "HR", data = df)
    ax.scatter("PA", "SB", data = df)
    ax.plot("PA", "SB", data = df)
    ax.set_xlabel('PA')
    ax.set_ylabel('HR (Blue) | SB (Orange)')
    plt.ylim([ymin, ymax])
    output = st.write(fig)
    return output

def get_time_graph_bbkswstr(df):
    fig, ax = plt.subplots(figsize=(8, 5), label='Inline label')
    ax.scatter("PA", "BB%", data = df)
    ax.plot("PA", "BB%", data = df, label='_BB%')
    ax.scatter("PA", "K%", data = df)
    ax.plot("PA", "K%", data = df, label='_K%')
    ax.scatter("PA", "ISO", data = df)
    ax.plot("PA", "ISO", data = df, label='_ISO')
    ax.scatter("PA", "SwStr%", data = df)
    ax.plot("PA", "SwStr%", data = df, label='_SwStr%')
    ax.set_xlabel('PA')
    ax.legend(frameon=False, loc = 'best', ncol=2)
    plt.ylim([.0, .35])
    output = st.write(fig)
    return output

def get_time_graph_fbldgb(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter("PA", "FB%", data = df)
    ax.plot("PA", "FB%", data = df, label='_FB%')
    ax.scatter("PA", "LD%", data = df)
    ax.plot("PA", "LD%", data = df, label='_LD%')
    ax.scatter("PA", "GB%", data = df)
    ax.plot("PA", "GB%", data = df, label='_GB%')
    ax.set_xlabel('PA')
    ax.legend(frameon=False, loc = 'best')
    plt.ylim([.10,.60])
    output = st.write(fig)
    return output

def get_time_graph_hrfb(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter("PA", "ISO", data = df)
    ax.plot("PA", "ISO", data = df, label='_ISO')
    ax.scatter("PA", "FB%", data = df)
    ax.plot("PA", "FB%", data = df, label='_FB%')
    ax.scatter("PA", "HR/FB", data = df)
    ax.plot("PA", "HR/FB", data = df, label='_HR/FB')
    ax.set_xlabel('PA')
    ax.legend(frameon=False, loc = 'best')
    plt.ylim([.10, .50])
    output = st.write(fig)
    return output

def get_time_graph_wrcbabip(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter("PA", "K%", data = df)
    ax.plot("PA", "K%", data = df, label='_wRC+')
    ax.scatter("PA", "BABIP", data = df)
    ax.plot("PA", "BABIP", data = df, label='_BABIP')
    ax.scatter("PA", "HR/FB", data = df)
    ax.plot("PA", "HR/FB", data = df, label='_HR/FB')
    ax.set_xlabel('PA')
    ax.legend(frameon=False, loc = 'best')
    plt.ylim([.10, .450])
    output = st.write(fig)
    return output

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
    #st.dataframe(df_sel_date_max_2)
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
    df_sel_all_dates_2 = df_sel_all_dates_2.reset_index()
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
    
    df_sel_all_dates = df_raw[df_raw['PlayerID'].str.contains(sel_pid)]
    df_sel_all_dates = df_sel_all_dates.sort_values(by=['G'],ascending=False)
    # df_sel_all_dates = df_sel_all_dates.loc[:,~df_sel_all_dates.columns.duplicated()]
    df_sel_all_dates_2 = df_sel_all_dates.filter(cols_xyz, axis=1)
    df_sel_all_dates_2 = df_sel_all_dates_2.dropna()
    df_sel_all_dates_2 = df_sel_all_dates_2.reset_index()
    
    #st.dataframe(df_sel_all_dates_2)

    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        get_time_graph_bbkswstr(df_sel_all_dates_2)
        get_time_graph_hrfb(df_sel_all_dates_2)
        # get_time_graph('wRC+', df_sel_all_dates_2, 100, 200)
        # get_time_graph('ISO', df_sel_all_dates_2, .100, .400)
        # get_time_graph('BABIP', df_sel_all_dates_2, .250, .500)
        # get_time_graph('OPS', df_sel_all_dates_2, .700, 1.100)


    with col5:
        # get_time_graph('K%', df_sel_all_dates_2, .10, .40)
        # get_time_graph('SwStr%', df_sel_all_dates_2, .05, .25)
        # get_time_graph('BB%', df_sel_all_dates_2, .0, .250)
        # #get_time_graph('SB', df_sel_all_dates_2, 0, 30)
        get_time_graph_hrsb(df_sel_all_dates_2, 0, 30)
        
        fig, axes = plt.subplots(2,2)
        # just plot things on each individual axes
        x = df_sel_all_dates_2['PA']
        y1 = df_sel_all_dates_2['wRC+']
        y2 = df_sel_all_dates_2['ISO']
        y3 = df_sel_all_dates_2['BABIP']
        y4 = df_sel_all_dates_2['K%']
        # one plot on each subplot
        axes[0][0].scatter(x,y1)
        axes[0][0].plot(x,y1)
        axes[0][0].set_ylim([100, 200])
        axes[0][0].legend(['wRC+'])
        axes[0][1].scatter(x,y2)
        axes[0][1].plot(x,y2)
        axes[0][1].set_ylim([.100, .400])
        axes[0][1].legend(['ISO'])
        axes[1][0].scatter(x,y3)
        axes[1][0].plot(x,y3)
        axes[1][0].set_ylim([.100, .400])
        axes[1][0].legend(['BABIP'])
        axes[1][1].scatter(x,y4)
        axes[1][1].plot(x,y4)
        axes[1][1].legend(['K%'])
        axes[1][1].set_ylim([.100, .400])
        st.write(fig)

        
    with col6:
        get_time_graph_fbldgb(df_sel_all_dates_2)
        # get_time_graph('FB%', df_sel_all_dates_2, .2, .6)
        # get_time_graph('LD%', df_sel_all_dates_2, .100, .400)
        # get_time_graph('GB%', df_sel_all_dates_2, .200, .600)
        get_time_graph_wrcbabip(df_sel_all_dates_2)
          
    # with col5:
    #     fig = plt.figure()
    #     plt.scatter('PA','wRC+', data= df_sel_all_dates_2)
    #     st.write(fig) 
    #     # fig = plt.figure()
    #     # plt.plot(x = df_sel_all_dates_2['PA'], y=df_sel_all_dates_2['ISO'])
    #     # st.write(fig)     
        
    #     # fig = plt.figure()
    #     # plt.plot(x = df_sel_all_dates_2['PA'], y=df_sel_all_dates_2['BB%'])
    #     # st.write(fig)         
        
    # with col6:
    #     fig = plt.figure()
    #     plt.scatter(x = df_sel_all_dates_2['PA'], y=df_sel_all_dates_2['K%'])
    #     st.write(fig)
        
    #     fig = plt.figure()
    #     plt.scatter(x = df_sel_all_dates_2['PA'], y=df_sel_all_dates_2['SwStr%'])
    #     st.write(fig)          
    
    df_sel_hist = df_hist_recent[df_hist_recent['PlayerID'].str.contains(sel_pid)]
    df_sel_hist = df_sel_hist.filter(cols_hist_display, axis=1)
    df_sel_hist = df_sel_hist.sort_values(by=['Season'],ascending=False)
    st.dataframe(df_sel_hist)


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

