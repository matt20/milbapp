import pandas as pd
import streamlit as st
import plotly.express as px
from st_aggrid import AgGrid,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype


st.set_page_config(page_title='MiLB Historical Offensive Comparison Tool', layout="wide")
st.header('MiLB Historical Offensive Comparison Tool')
st.write('Use the sliders on the sidebar to filter 2022 Minor League Baseball statistics (updated as of yesterday, courtesy of FanGraphs.com)')


#######################################################################
#### ---- LOAD DATAFRAMES ---- ########################################
dfhist = pd.read_csv(r'C:/Users/mwpul/milbapp/milb0621off_70pa.csv', index_col ='playeriduniquecount')

dfcurr = pd.read_csv(r'C:/Users/mwpul/milbapp/milbtoday.csv', index_col ='idlevelorg')

#have user select parameters to filter data
# enable_selection=st.sidebar.checkbox("Enable row selection", value=True)
# if enable_selection:
#     st.sidebar.subheader("Selection options")
#     selection_mode = st.sidebar.radio("Selection Mode", ['single','multiple'], index=1)
    
#     use_checkbox = st.sidebar.checkbox("Use check box for selection", value=True)
#     if use_checkbox:
#         groupSelectsChildren = st.sidebar.checkbox("Group checkbox select children", value=True)
#         groupSelectsFiltered = st.sidebar.checkbox("Group checkbox includes filtered", value=True)

#     if ((selection_mode == 'multiple') & (not use_checkbox)):
#         rowMultiSelectWithClick = st.sidebar.checkbox("Multiselect with click (instead of holding CTRL)", value=False)
#         if not rowMultiSelectWithClick:
#             suppressRowDeselection = st.sidebar.checkbox("Suppress deselection (while holding CTRL)", value=False)
#         else:
#             suppressRowDeselection=False
#     st.sidebar.text("___")

input_age = st.sidebar.slider('Max Age:', 16, 32, 20)
input_pa_curr = st.sidebar.slider('Min PA (2022):', 30, 100, 50)
input_kpct = st.sidebar.slider('Max K%:', .0, .400, .300)
input_iso = st.sidebar.slider('Min ISO:', .0, .400, .150)
input_bbpct = st.sidebar.slider('Min BB%:', .0, .25, .05)
input_wrcplus = st.sidebar.slider('Min wRC+:', 0, 200, 100)
input_buffer_iso = st.sidebar.slider('ISO Buffer:', .0, .100, .025)
input_buffer_kpct = st.sidebar.slider('K% Buffer:', .0, .100, .025)
input_buffer_bbpct = st.sidebar.slider('BB% Buffer:', .0, .100, .025)
input_pa_hist = st.sidebar.slider('Min PA (Hist):', 100, 400, 100)



#lev_type = CategoricalDtype(categories=['DSL','Rk','CPX','A-','A','A+','AA','AAA'], ordered=True)
#level_cats = ['AAA','AA','A+','A','A-','R','CPX','DSL']
#level_cats = CategoricalDtype(categories=['AAA','AA','A+','A','A-','R','CPX','DSL'], ordered=True)
#dfhist['level'] = dfhist['level'].astype(level_cats)
#dfhist['level'] = dfhist['level'].cat.reorder_categories(cat, ordered=True)
#CategoricalIndex.reorder_categories(dfhist['level'], ordered=True)

# dfhist['level'] = pd.Categorical(dfhist['level'], categories=['AAA','AA','A+','A','A-','R','CPX','DSL'],ordered=True)

#['AAA', 'R', 'A', 'A+', 'AA', 'A-', 'CPX', 'DSL']
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

levels = dfhist['level'].unique()
input_levels = st.sidebar.multiselect(
    "Levels:", levels, default=levels)

cols_hist = ['Name/Org', 'age', 'level', 'season', 'pa', 'wrcplus','iso','kpct','swstrpct','bbpct', 'xSpect',
             'OPS', 'babip', 'avg', 'obp', 'slg', 'hr', 'hrperfb', 'sb', 'cs', 'fbpct', 'ldpct', 'gbpct', 'pullpct', 'centpct', 'oppopct', 'level_code']

cols_hist_display = ['Name/Org', 'Age', 'Level', 'Season', 'PA', 'wRC+', 'ISO', 'K%', 'SwStr%', 'BB%', 'xSpect', 
                     'OPS', 'BABIP', 'AVG', 'OBP', 'SLG', 'HR', 'HR/FB', 'SB', 'CS', 'FB%', 'LD%', 'GB%', 'Pull%', 'Cent%', 'Oppo%', 'level_code']


cols_curr = ['Name/Org', 'Age', 'Level', 'xSpect', 'PA', 'wRC+', 'ISO', 'K%', 'SwStr%', 'BB%', 'hmm', 
         #'xPOPS', 
        'OPS', 'BABIP', 'AVG', 'OBP', 'SLG', 'XBH', 'HR', 'HR/FB', 'SB', 'CS', 'FB%', 'GB%', 'LD%']

#######################################################################
#### --- ADJUSTING THE DATA   ----------------------------------- #####

dfhist['xSpect'] = (dfhist['iso']/(dfhist['kpct']+dfhist['swstrpct'])).round(3)
dfhist['Name/Org'] = dfhist['name'] + ' - ' + dfhist['team']
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
dfcurr['Name/Org'] = (dfcurr['Name'] + " - " + dfcurr['Org'])
#dfcurr = dfcurr[dfcurr['Org'].isin(orgs_choice)]
dfcurr['XBH'] = dfcurr['2B'] + dfcurr['3B'] + dfcurr['HR']
dfcurr['hmm'] = ((2*dfcurr['ISO'])+(dfcurr['BB%']/2))**(((3*dfcurr['K%'])+dfcurr['SwStr%'])**dfcurr['BABIP']).round(3)
dfcurr['xSpect'] = (dfcurr['ISO']/(dfcurr['K%']+dfcurr['SwStr%'])).round(3)
#dfcurr['xPOPS'] = (dfcurr['xSpect']*dfcurr['OPS']).round(3)
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
#dfcurr2 = dfcurr2[dfcurr2['Level'].isin(input_levels)]
#dfcurr2.columns = cols_curr
#######################################################################


#######################################################################
#### --- THE FIRST DATA TABLE ----------------------------------- #####
# utilize the datediff variable in the jupyter notebook to set the X in the subheader
st.write('Select a row from the 2022 stats to see all MiLB seasons with a higher ISO and walk rate, and lower strikeout rate since 2006 in the second table')
st.caption('Season is defined as a stint at one level with one team of at least 100 PA')
# configure grid options for Ag-Grid table
gd = GridOptionsBuilder.from_dataframe(dfcurr2)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True, groupable=True)
#sel_mode = st.radio('Selection Type', options=['single'])
gd.configure_selection(selection_mode='single', use_checkbox=True, pre_selected_rows=[0])
gridoptions = gd.build()
grid_table = AgGrid(dfcurr2, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                    height=500,
                    allow_unsafe_jscode=True,
                    enable_enterprise_modules = True,
                    theme='blue')

sel_row = grid_table["selected_rows"]


if sel_row != "":
    #st.write(sel_row)

    df_sel = pd.DataFrame(sel_row)
    st.subheader("Selected player: " + df_sel['Name/Org'].iloc[0])
    st.table(df_sel)

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
#################################################
#FILTER THE HIST DATA ON THE NEW SELECTED JAWNS

# st.write(sel_buff_iso.dtypes)

#dfhist2['age'] = dfhist2['age'].astype(int)
#dfhist3 = dfhist2[(dfhist2['iso'] >= sel_iso) & (dfhist2['kpct'] <= sel_kpct) & (dfhist2['bbpct'] >= sel_bbpct)]
#either above code or below code depending on whether or not the buffers are working -_- #
dfhist3 = dfhist2[(dfhist2['ISO'] >= sel_buff_iso) &
                  (dfhist2['K%'] <= sel_buff_kpct) &
                  (dfhist2['BB%'] >= sel_buff_bbpct) &
                  (dfhist2['Age'] <= sel_age)]
                  

dfhist3 = dfhist3.sort_values(by='level_code', ascending=False)
# selection_iso = df_selected['ISO']
# selection_kpct = df_selected['K%']
# selection_bbpct = df_selected['BB%']
# selection_wrcplus = df_selected['wRC+']
# selection_swstrpct = df_selected['SwStr%']

# st.write(selection_iso)

# gb2 = GridOptionsBuilder.from_dataframe(dfcurr2)
# gb2.configure_pagination()
# gb2.configure_side_bar()
# gb2.configure_selection(selection_mode="single", use_checkbox=True)
# gb2.configure_default_column(min_column_width = 1, groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
# if enable_selection:
#     gb2.configure_selection(selection_mode)
#     if use_checkbox:
#         gb2.configure_selection(selection_mode, use_checkbox=True, groupSelectsChildren=groupSelectsChildren, groupSelectsFiltered=groupSelectsFiltered)
#     # if ((selection_mode == 'multiple') & (not use_checkbox)):
#     #     gb2.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=rowMultiSelectWithClick, suppressRowDeselection=suppressRowDeselection)
# gridOptions2 = gb2.build()
# grid_response = AgGrid(dfcurr2, gridOptions=gridOptions2, enable_enterprise_modules=True, theme='blue')

# selected = grid_response['selected_rows']
# selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')
# st.write(grid_response['selected_rows'])
# st.table(data=selected_df)
#print
# agree_curr = st.checkbox('Show 2022 data')

# if agree_curr:
#      AgGrid(dfcurr2, gridOptions=gridOptions2, enable_enterprise_modules=True, theme='blue')

# configure grid options for Ag-Grid table
gb = GridOptionsBuilder.from_dataframe(dfhist3)
#gb.configure_pagination()
#gb.configure_column('Name/Org', min_column_width = 25)
gb.configure_side_bar()
#gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_default_column(min_column_width = .1, groupable=True, value=True, enableRowGroup=True, aggFunc="mean", editable=True)
gridOptions = gb.build()

AgGrid(dfhist3, gridOptions=gridOptions, enable_enterprise_modules=True, theme = "blue")
# agree_hist = st.checkbox('Show historical data')


# if agree_hist:
#      AgGrid(dfhist3, gridOptions=gridOptions, enable_enterprise_modules=True, theme = "blue")

##################################################
#adding in some graphs and things of that nature
##################################################

