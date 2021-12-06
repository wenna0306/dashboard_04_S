import openpyxl
import pandas as pd
import plotly.graph_objects as go
import matplotlib
import numpy as np
import streamlit as st
from matplotlib.backends.backend_agg import RendererAgg
matplotlib.use('agg')
from st_btn_select import st_btn_select

_lock = RendererAgg.lock

# -----------------------------------------set page layout-------------------------------------------------------------
st.set_page_config(page_title='iSMM Dashboard',
                   page_icon = ':chart_with_upwards_trend:',
                   layout='wide',
                   initial_sidebar_state='collapsed')


page = st_btn_select(('Faults', 'Inventories'),
                     nav=True,
                     format_func=lambda name: name.capitalize(),
                     )
if page =='Faults':
    html_card_title="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; padding-top: 5px; width: 600px;
       height: 50px;">
        <h1 class="card-title" style=color:#116a8c; font-family:Georgia; text-align: left; padding: 0px 0;">FAULT DASHBOARD Nov 2021</h1>
      </div>
    </div>
    """

    st.markdown(html_card_title, unsafe_allow_html=True)
    st.markdown('##')
    st.markdown('##')
    st.markdown(
        'Welcome to this Analysis App, get more detail from :point_right: [iSMM](https://ismm.sg/ce/login)')
    st.markdown('##')

    def fetch_file(filename):
        cols = ['Fault Number', 'Building Trade', 'Trade Category',
                'Type of Fault', 'Impact', 'Location', 'Cancel Status', 'Reported Date',
                'Fault Acknowledged Date', 'Responded on Site Date', 'RA Conducted Date',
                'Work Started Date', 'Work Completed Date',
                'Other Trades Required Date', 'Cost Cap Exceed Date',
                'Assistance Requested Date', 'Fault Reference',
                'End User Priority', 'Incident Report', 'Remarks']
        parse_dates = ['Reported Date',
                       'Fault Acknowledged Date', 'Responded on Site Date', 'RA Conducted Date',
                       'Work Started Date', 'Work Completed Date',
                       'Other Trades Required Date', 'Cost Cap Exceed Date',
                       'Assistance Requested Date']
        return pd.read_excel(filename, header=1, index_col='Fault Number', usecols=cols, parse_dates=parse_dates)


    df = fetch_file('Fault 2021-12-05 211557.xlsx')
    df.columns = df.columns.str.replace(' ', '_')
    df['Time_Acknowledged_mins'] = (df.Fault_Acknowledged_Date - df.Reported_Date)/pd.Timedelta(minutes=1)
    df['Time_Site_Reached_mins'] = (df.Responded_on_Site_Date - df.Reported_Date)/pd.Timedelta(minutes=1)
    df['Time_Work_Started_mins'] = (df.Work_Started_Date - df.Reported_Date)/pd.Timedelta(minutes=1)
    df['Time_Work_Recovered_mins'] = (df.Work_Completed_Date - df.Reported_Date)/pd.Timedelta(minutes=1)

    df1 = df.Location.str.split(pat=' > ', expand=True, n=3).rename(columns={0:'Site', 1:'Building', 2:'Level'})
    df2 = pd.concat([df, df1], axis=1)

    # ----------------------------------------Sidebar---------------------------------------------------------------------
    st.sidebar.header('Please Filter Here:')

    Building_Trade = st.sidebar.multiselect(
        'Select the Building Trade:',
        options=df2['Building_Trade'].unique(),
        default=df2['Building_Trade'].unique()
    )

    Trade_Category = st.sidebar.multiselect(
        'Select the Trade Category:',
        options=df2['Trade_Category'].unique(),
        default=df2['Trade_Category'].unique()
    )

    df2 = df2.query(
        'Building_Trade ==@Building_Trade & Trade_Category==@Trade_Category'
    )


    # ----------------------------------------------Main Page---------------------------------------------------------------
    html_card_subheader_outstanding = """
        <div class="card">
          <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #116a8c; padding-top: 5px; width: 350px;
           height: 50px;">
            <h3 class="card-title" style="background-color:#116a8c; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">Outstanding Fault</h3>
          </div>
        </div>
        """
    html_card_subheader_daily="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #116a8c; padding-top: 5px; width: 350px;
       height: 50px;">
        <h3 class="card-title" style="background-color:#116a8c; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">Daily Fault Cases</h3>
      </div>
    </div>
    """
    html_card_subheader_KPI_Responded="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #116a8c; padding-top: 5px; width: 450px;
       height: 50px;">
        <h3 class="card-title" style="background-color:#116a8c; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">KPI Monitoring-Responded</h3>
      </div>
    </div>
    """
    html_card_subheader_KPI_Recovered="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #116a8c; padding-top: 5px; width: 450px;
       height: 50px;">
        <h3 class="card-title" style="background-color:#116a8c; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">KPI Monitoring-Recovered</h3>
      </div>
    </div>
    """
    html_card_subheader_Tier1="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #116a8c; padding-top: 5px; width: 500px;
       height: 50px;">
        <h3 class="card-title" style="background-color:#116a8c; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">Recovered Fault vs Building Trade</h3>
      </div>
    </div>
    """
    html_card_subheader_Tier2="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #116a8c; padding-top: 5px; width: 500px;
       height: 50px;">
        <h3 class="card-title" style="background-color:#116a8c; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">Recovered Fault vs Trade Category</h3>
      </div>
    </div>
    """
    html_card_subheader_Tier3="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #116a8c; padding-top: 5px; width: 500px;
       height: 50px;">
        <h3 class="card-title" style="background-color:#116a8c; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">Recovered Fault vs Type of Fault</h3>
      </div>
    </div>
    """
    html_card_subheader_location="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px; background: #116a8c; padding-top: 5px; width: 450px;
       height: 50px;">
        <h3 class="card-title" style="background-color:#116a8c; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">Recovered Fault vs Location</h3>
      </div>
    </div>
    """

    # -----------------------------------------------------Fault-----------------------------------------------------------
    total_fault = df2.shape[0]
    fault_cancelled = int(df2['Cancel_Status'].notna().sum())
    fault_not_recovered = df2.loc[(df2['Cancel_Status'].isna()) & (df2['Work_Completed_Date'].isna()),:].shape[0]
    fault_recovered = df2.loc[(df2['Cancel_Status'].isna()) & (df2['Work_Completed_Date'].notna()),:].shape[0]
    fault_incident = int(df2['Incident_Report'].sum())


    column01_fault, column02_fault, column03_fault, column04_fault, column05_fault = st.columns(5)
    with column01_fault, _lock:
        st.markdown('**Total**')
        st.markdown(f"<h2 style='text-align: left; color: #703bef;'>{total_fault}</h2>", unsafe_allow_html=True)

    with column02_fault, _lock:
        st.markdown('Cancelled')
        st.markdown(f"<h2 style='text-align: left; color: #3c9992;'>{fault_cancelled}</h2>", unsafe_allow_html=True)

    with column03_fault, _lock:
        st.markdown('Outstanding')
        st.markdown(f"<h2 style='text-align: left; color: red;'>{fault_not_recovered}</h2>", unsafe_allow_html=True)

    with column04_fault, _lock:
        st.markdown('Recovered')
        st.markdown(f"<h2 style='text-align: left; color: #4da409;'>{fault_recovered}</h2>", unsafe_allow_html=True)

    with column05_fault, _lock:
        st.markdown('Incident Report')
        st.markdown(f"<h2 style='text-align: left; color: #fec615;'>{fault_incident}</h2>", unsafe_allow_html=True)

    st.markdown('##')
    st.markdown('##')
    st.markdown(html_card_subheader_outstanding, unsafe_allow_html=True)
    st.markdown('##')

    df_outstanding = df2.loc[(df2['Cancel_Status'].isna()) & (df2['Work_Completed_Date'].isna()),:]

    ser_outstanding_building = df_outstanding.groupby(['Building_Trade'])['Type_of_Fault'].count().sort_values(ascending=False)
    ser_outstanding_category = df_outstanding.groupby(['Trade_Category'])['Type_of_Fault'].count().sort_values(ascending=False)

    x_outstanding_building = ser_outstanding_building.index
    y_outstanding_building = ser_outstanding_building.values
    x_outstanding_category = ser_outstanding_category.index
    y_outstanding_category = ser_outstanding_category.values

    fig_outstanding_building, fig_outstanding_category = st.columns([1, 2])

    with fig_outstanding_building, _lock:
        fig_outstanding_building = go.Figure(data=[go.Pie(labels=x_outstanding_building, values=y_outstanding_building, hoverinfo='all', textinfo='label+percent+value', textfont_size=15, textfont_color='white', textposition='inside', showlegend=False, hole=.4)])
        fig_outstanding_building.update_layout(title='Number of Fault vs Building Trade', annotations=[dict(text='Outstanding', x=0.5, y=0.5, font_size=18, showarrow=False)])
        st.plotly_chart(fig_outstanding_building, use_container_width=True)

    with fig_outstanding_category, _lock:
        fig_outstanding_category = go.Figure(data=[go.Bar(x=x_outstanding_category, y=y_outstanding_category, orientation='v', text=y_outstanding_category,
                                                          textfont=dict(family='sana serif', size=14, color='#c4fff7'),
                                                          textposition='auto', textangle=-45)
                                                   ])
        fig_outstanding_category.update_xaxes(title_text="Trade Category", tickangle=-45, title_font_color='#4c9085', showgrid=False,
                           showline=True, linewidth=1, linecolor='#59656d')
        fig_outstanding_category.update_yaxes(title_text='Number of Fault', title_font_color='#4c9085', showgrid=True, gridwidth=0.1,
                           gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
        fig_outstanding_category.update_traces(marker_color='#4c9085', marker_line_color='#4c9085', marker_line_width=1)
        fig_outstanding_category.update_layout(title='Number of Fault vs Trade Category', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_outstanding_category, use_container_width=True)

    st.markdown(html_card_subheader_daily, unsafe_allow_html=True)
    df_daily = df2.loc[(df2['Cancel_Status'].isna()) & (df2['Work_Completed_Date'].notna()),:]
    x_daily = df_daily['Reported_Date'].dt.day.value_counts().sort_index().index
    y_daily = df_daily['Reported_Date'].dt.day.value_counts().sort_index().values
    y_mean = df_daily['Reported_Date'].dt.day.value_counts().sort_index().mean()

    fig_daily = go.Figure(data=go.Scatter(x=x_daily, y=y_daily, mode='lines+markers+text', line=dict(color='#13bbaf', width=3),
                                          text=y_daily, textfont=dict(family='sana serif', size=14, color='#c4fff7'), textposition='top center'))
    fig_daily.add_hline(y=y_mean, line_dash='dot', line_color='#96ae8d', line_width=2, annotation_text='Average Line',
                              annotation_position='bottom right', annotation_font_size=18, annotation_font_color='green')
    fig_daily.update_xaxes(title_text='Date', tickangle=-45, title_font_color='#74a662', tickmode='linear', range=[1, 31],
                                       showgrid=False, showline=True, linewidth=1, linecolor='#59656d')
    fig_daily.update_yaxes(title_text='Number of Fault', title_font_color='#74a662', tickmode='linear', showgrid=False,
                                       gridwidth=0.1, gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
    fig_daily.update_layout(title = 'Number of Fault vs Date', plot_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig_daily, use_container_width=True)


    df3 = df2.loc[(df2['Cancel_Status'].isna()) & (df2['Work_Completed_Date'].notna()),:]
    cols_drop = ['Impact', 'Cancel_Status', 'Other_Trades_Required_Date', 'Cost_Cap_Exceed_Date', 'Assistance_Requested_Date',
                 'Fault_Reference', 'End_User_Priority', 'Incident_Report', 'Location', 'Reported_Date', 'Fault_Acknowledged_Date',
                 'Responded_on_Site_Date', 'RA_Conducted_Date', 'Work_Started_Date', 'Work_Completed_Date']
    df3.drop(columns=cols_drop, inplace=True)
    df3 = df3[['Site', 'Building', 'Level', 'Building_Trade', 'Trade_Category', 'Type_of_Fault', 'Time_Acknowledged_mins',
               'Time_Site_Reached_mins', 'Time_Work_Started_mins', 'Time_Work_Recovered_mins']]

    bin_responded = [0, 10, 30, 60, np.inf]
    label_responded = ['0-10mins', '10-30mins', '30-60mins', '60-np.inf']

    bin_recovered = [0, 60, 240, 480, np.inf]
    label_recovered = ['0-1hr', '1-4hrs', '4-8hrs', '8-np.inf']

    df3['KPI_For_Responded'] = pd.cut(df3.Time_Site_Reached_mins, bins=bin_responded, labels=label_responded, include_lowest=True)
    df3['KPI_For_Recovered'] = pd.cut(df3.Time_Work_Recovered_mins, bins=bin_recovered, labels=label_recovered, include_lowest=True)

    st.markdown(html_card_subheader_KPI_Responded, unsafe_allow_html=True)
    st.markdown('##')
    st.markdown('Response Time refers to the time the fault or emergency was reported to the time the Contractor arrived on-site with evidence')
    st.markdown('##')

    space01, dataframe01, space02, dataframe02, space03 = st.columns((.1, 1, .1, 2, .1))
    with dataframe01, _lock:
        st.markdown('KPI (Responded) vs Building Trade')
        st.dataframe(df3.groupby(by='KPI_For_Responded').Building_Trade.value_counts().unstack(level=-1).fillna(0).astype(int).style.highlight_max(
            axis=0, props='color:#f0833a; font-weight:bold; background-color:dark;'))

    with dataframe02, _lock:
        st.markdown('KPI(Responded) vs Trade Category')
        st.dataframe(df3.groupby(by='KPI_For_Responded').Trade_Category.value_counts().unstack(level=0).T.fillna(0).astype(int).style.highlight_max(
            axis=0, props='color:#f0833a; font-weight:bold; background-color:dark;'))

    x_KPI_building_010_Responded = df3.groupby(by='KPI_For_Responded').Building_Trade.value_counts().loc['0-10mins'].index
    x_KPI_building_1030_Responded = df3.groupby(by='KPI_For_Responded').Building_Trade.value_counts().loc['10-30mins'].index
    x_KPI_building_3060_Responded = df3.groupby(by='KPI_For_Responded').Building_Trade.value_counts().loc['30-60mins'].index
    x_KPI_building_60inf_Responded = df3.groupby(by='KPI_For_Responded').Building_Trade.value_counts().loc['60-np.inf'].index

    y_KPI_building_010_Responded = df3.groupby(by='KPI_For_Responded').Building_Trade.value_counts().loc['0-10mins'].values
    y_KPI_building_1030_Responded = df3.groupby(by='KPI_For_Responded').Building_Trade.value_counts().loc['10-30mins'].values
    y_KPI_building_3060_Responded = df3.groupby(by='KPI_For_Responded').Building_Trade.value_counts().loc['30-60mins'].values
    y_KPI_building_60inf_Responded = df3.groupby(by='KPI_For_Responded').Building_Trade.value_counts().loc['60-np.inf'].values

    x_KPI_category_010_Responded = df3.groupby(by='KPI_For_Responded').Trade_Category.value_counts().loc['0-10mins'].index
    x_KPI_category_1030_Responded = df3.groupby(by='KPI_For_Responded').Trade_Category.value_counts().loc['10-30mins'].index
    x_KPI_category_3060_Responded = df3.groupby(by='KPI_For_Responded').Trade_Category.value_counts().loc['30-60mins'].index
    x_KPI_category_60inf_Responded = df3.groupby(by='KPI_For_Responded').Trade_Category.value_counts().loc['60-np.inf'].index

    y_KPI_category_010_Responded = df3.groupby(by='KPI_For_Responded').Trade_Category.value_counts().loc['0-10mins'].values
    y_KPI_category_1030_Responded = df3.groupby(by='KPI_For_Responded').Trade_Category.value_counts().loc['10-30mins'].values
    y_KPI_category_3060_Responded = df3.groupby(by='KPI_For_Responded').Trade_Category.value_counts().loc['30-60mins'].values
    y_KPI_category_60inf_Responded = df3.groupby(by='KPI_For_Responded').Trade_Category.value_counts().loc['60-np.inf'].values

    fig_responded_building, fig_responded_category = st.columns([1, 2])
    with fig_responded_building, _lock:
        fig_responded_building = go.Figure(data=[
            go.Bar(name='0-10mins', x=x_KPI_building_010_Responded, y=y_KPI_building_010_Responded),
            go.Bar(name='10-30mins', x=x_KPI_building_1030_Responded, y=y_KPI_building_1030_Responded),
            go.Bar(name='30-60mins', x=x_KPI_building_3060_Responded, y=y_KPI_building_3060_Responded),
            go.Bar(name='60-np.inf', x=x_KPI_building_60inf_Responded, y=y_KPI_building_60inf_Responded)
        ])
        fig_responded_building.update_xaxes(title_text="Building Trade", tickangle=-45, title_font_color='#a2bffe', showgrid=False, showline=True, linewidth=1, linecolor='#59656d')
        fig_responded_building.update_yaxes(title_text='Number of Fault', title_font_color='#a2bffe', showgrid=True, gridwidth=0.1, gridcolor='#1f3b4d',
                           showline=True, linewidth=1, linecolor='#59656d')
        fig_responded_building.update_layout(barmode='stack', title='KPI Monitoring(Responded) vs Building Trade', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_responded_building, use_container_width=True)

    with fig_responded_category, _lock:
        fig_responded_category = go.Figure(data=[
            go.Bar(name='0-10mins', x=x_KPI_category_010_Responded, y=y_KPI_category_010_Responded),
            go.Bar(name='10-30mins', x=x_KPI_category_1030_Responded, y=y_KPI_category_1030_Responded),
            go.Bar(name='30-60mins', x=x_KPI_category_3060_Responded, y=y_KPI_category_3060_Responded),
            go.Bar(name='60-np.inf', x=x_KPI_category_60inf_Responded, y=y_KPI_category_60inf_Responded),
        ])
        fig_responded_category.update_xaxes(title_text="Trade Category", tickangle=-45, title_font_color='#a2bffe',
                                            showgrid=False, showline=True, linewidth=1, linecolor='#59656d')
        fig_responded_category.update_yaxes(title_text='Number of Fault', title_font_color='#a2bffe', showgrid=True,
                                            gridwidth=0.1, gridcolor='#1f3b4d',
                                            showline=True, linewidth=1, linecolor='#59656d')
        fig_responded_category.update_layout(barmode='stack', title='KPI Monitoring(Responded) vs Trade Category',
                                             plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_responded_category, use_container_width=True)

    st.markdown('##')
    st.markdown('##')
    st.markdown(html_card_subheader_KPI_Recovered, unsafe_allow_html=True)
    st.markdown('##')
    st.markdown('Recovery Time refers to the time the fault or emergency was reported to the time the Contractor completed the work with evidence')
    st.markdown('##')
    space04, dataframe03, space05, dataframe04, space06 = st.columns((.1, 1, .1, 2, .1))
    with dataframe03, _lock:
        st.markdown('KPI(Recovered) vs Building Trade')
        st.dataframe(df3.groupby(by='KPI_For_Recovered').Building_Trade.value_counts().unstack(level=-1).fillna(0).astype(int).style.highlight_max(
            axis=0, props='color:#f0833a; font-weight:bold; background-color:dark;'))

    with dataframe04, _lock:
        st.markdown('KPI(Recovered) vs Trade Category')
        st.dataframe(df3.groupby(by='KPI_For_Recovered').Trade_Category.value_counts().unstack(level=0).T.fillna(0).astype(int).style.highlight_max(
            axis=0, props='color:#f0833a; font-weight:bold; background-color:dark;'))

    x_KPI_building_010_recovered = df3.groupby(by='KPI_For_Recovered').Building_Trade.value_counts().loc['0-1hr'].index
    x_KPI_building_1030_recovered = df3.groupby(by='KPI_For_Recovered').Building_Trade.value_counts().loc['1-4hrs'].index
    x_KPI_building_3060_recovered = df3.groupby(by='KPI_For_Recovered').Building_Trade.value_counts().loc['4-8hrs'].index
    x_KPI_building_60inf_recovered = df3.groupby(by='KPI_For_Recovered').Building_Trade.value_counts().loc['8-np.inf'].index

    y_KPI_building_010_recovered = df3.groupby(by='KPI_For_Recovered').Building_Trade.value_counts().loc['0-1hr'].values
    y_KPI_building_1030_recovered = df3.groupby(by='KPI_For_Recovered').Building_Trade.value_counts().loc['1-4hrs'].values
    y_KPI_building_3060_recovered = df3.groupby(by='KPI_For_Recovered').Building_Trade.value_counts().loc['4-8hrs'].values
    y_KPI_building_60inf_recovered = df3.groupby(by='KPI_For_Recovered').Building_Trade.value_counts().loc['8-np.inf'].values

    x_KPI_category_010_recovered = df3.groupby(by='KPI_For_Recovered').Trade_Category.value_counts().loc['0-1hr'].index
    x_KPI_category_1030_recovered = df3.groupby(by='KPI_For_Recovered').Trade_Category.value_counts().loc['1-4hrs'].index
    x_KPI_category_3060_recovered = df3.groupby(by='KPI_For_Recovered').Trade_Category.value_counts().loc['4-8hrs'].index
    x_KPI_category_60inf_recovered = df3.groupby(by='KPI_For_Recovered').Trade_Category.value_counts().loc['8-np.inf'].index

    y_KPI_category_010_recovered = df3.groupby(by='KPI_For_Recovered').Trade_Category.value_counts().loc['0-1hr'].values
    y_KPI_category_1030_recovered = df3.groupby(by='KPI_For_Recovered').Trade_Category.value_counts().loc['1-4hrs'].values
    y_KPI_category_3060_recovered = df3.groupby(by='KPI_For_Recovered').Trade_Category.value_counts().loc['4-8hrs'].values
    y_KPI_category_60inf_recovered = df3.groupby(by='KPI_For_Recovered').Trade_Category.value_counts().loc['8-np.inf'].values

    fig_recovered_building, fig_recovered_category = st.columns([1, 2])
    with fig_recovered_building, _lock:
        fig_recovered_building = go.Figure(data=[
            go.Bar(name='0-1hr', x=x_KPI_building_010_recovered, y=y_KPI_building_010_recovered),
            go.Bar(name='1-4hrs', x=x_KPI_building_1030_recovered, y=y_KPI_building_1030_recovered),
            go.Bar(name='4-8hrs', x=x_KPI_building_3060_recovered, y=y_KPI_building_3060_recovered),
            go.Bar(name='8-np.inf', x=x_KPI_building_60inf_recovered, y=y_KPI_building_60inf_recovered)
        ])
        fig_recovered_building.update_xaxes(title_text="Building Trade", tickangle=-45, title_font_color='#a2bffe', showgrid=False, showline=True, linewidth=1, linecolor='#59656d')
        fig_recovered_building.update_yaxes(title_text='Number of Fault', title_font_color='#a2bffe', showgrid=True, gridwidth=0.1, gridcolor='#1f3b4d',
                           showline=True, linewidth=1, linecolor='#59656d')
        fig_recovered_building.update_layout(barmode='stack', title='KPI Monitoring(Recovered) vs Building Trade', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_recovered_building, use_container_width=True)

    with fig_recovered_category, _lock:
        fig_recovered_category = go.Figure(data=[
            go.Bar(name='0-1hr', x=x_KPI_category_010_recovered, y=y_KPI_category_010_recovered),
            go.Bar(name='1-4hrs', x=x_KPI_category_1030_recovered, y=y_KPI_category_1030_recovered),
            go.Bar(name='4-8hrs', x=x_KPI_category_3060_recovered, y=y_KPI_category_3060_recovered),
            go.Bar(name='8-np.inf', x=x_KPI_category_60inf_recovered, y=y_KPI_category_60inf_recovered)
        ])
        fig_recovered_category.update_xaxes(title_text="Trade Category", tickangle=-45, title_font_color='#a2bffe', showgrid=False, showline=True, linewidth=1, linecolor='#59656d')
        fig_recovered_category.update_yaxes(title_text='Number of Fault', title_font_color='#a2bffe', showgrid=True, gridwidth=0.1, gridcolor='#1f3b4d',
                           showline=True, linewidth=1, linecolor='#59656d')
        fig_recovered_category.update_layout(barmode='stack', title='KPI Monitoring(Recovered) vs Trade Category', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_recovered_category, use_container_width=True)

    st.markdown('##')
    st.markdown('##')
    st.markdown(html_card_subheader_Tier1, unsafe_allow_html=True)
    st.markdown('##')

    df3['Time_Acknowledged_hrs'] = df3.Time_Acknowledged_mins/60
    df3['Time_Site_Reached_hrs'] = df3.Time_Site_Reached_mins/60
    df3['Time_Work_Started_hrs'] = df3.Time_Work_Started_mins/60
    df3['Time_Work_Recovered_hrs'] = df3.Time_Work_Recovered_mins/60

    df4 = df3.loc[:, ['Site', 'Building', 'Level', 'Building_Trade', 'Trade_Category', 'Type_of_Fault', 'KPI_For_Responded',
                     'KPI_For_Recovered', 'Time_Acknowledged_hrs', 'Time_Site_Reached_hrs', 'Time_Work_Started_hrs',
                     'Time_Work_Recovered_hrs']]
    df4= df4[['Site', 'Building', 'Level', 'Building_Trade', 'Trade_Category', 'Type_of_Fault', 'Time_Acknowledged_hrs',
              'Time_Site_Reached_hrs', 'Time_Work_Started_hrs', 'Time_Work_Recovered_hrs']]

    df5 = df4.groupby(by=['Building_Trade']).agg(['count', 'max', 'min', 'mean', 'sum']).sort_values((     'Time_Acknowledged_hrs', 'count'), ascending=False)
    cols_name = ['Fault_Acknowledged_count', 'Fault_Acknowledged_max(hrs)', 'Fault_Acknowledged_min(hrs)', 'Fault_Acknowledged_mean(hrs)',
                   'Fault_Acknowledged_sum(hrs)', 'Fault_Site_Reached_count', 'Fault_Site_Reached_max(hrs)', 'Fault_Site_Reached_min(hrs)',
                   'Fault_Site_Reached_mean(hrs)', 'Fault_Site_Reached_sum(hrs)', 'Fault_Work_Started_count', 'Fault_Work_Started_max(hrs)',
                   'Fault_Work_Started_min(hrs)', 'Fault_Work_Started_mean(hrs)', 'Fault_Work_Started_sum(hrs)', 'Fault_Recovered_count',
                   'Fault_Recovered_max(hrs)', 'Fault_Recovered_min(hrs)', 'Fault_Recovered_mean(hrs)', 'Fault_Recovered_sum(hrs)']
    df5.columns = cols_name
    df6 = df5.loc[:, ['Fault_Site_Reached_count', 'Fault_Site_Reached_mean(hrs)', 'Fault_Site_Reached_sum(hrs)',
                  'Fault_Recovered_count', 'Fault_Recovered_mean(hrs)', 'Fault_Recovered_sum(hrs)']]
    df6.reset_index(inplace=True)

    x = df6['Building_Trade']
    y4 = df6.Fault_Recovered_count
    y5 = df6['Fault_Recovered_mean(hrs)']
    y6 = df6['Fault_Recovered_sum(hrs)']

    fig04, fig05, fig06 = st.columns(3)
    with fig04, _lock:
        fig04 = go.Figure(data=[go.Pie(values=y4, labels=x, hoverinfo='all', textinfo='label+percent+value', textfont_size=15, textfont_color='white', textposition='inside', showlegend=False, hole=.4)])
        fig04.update_layout(title='Proportions of Building Trade(Recovered)', annotations=[dict(text='Recovered', x=0.5, y=0.5, font_size=18, showarrow=False)])
        st.plotly_chart(fig04, use_container_width=True)

    with fig05, _lock:
        fig05 = go.Figure(data=[go.Bar(x=x, y=y5, orientation='v', text=y5,
                                textfont = dict(family='sana serif', size=14, color='#c4fff7'),
                                textposition = 'auto', textangle = -45, texttemplate = '%{text:.2f}')
                            ])
        fig05.update_xaxes(title_text="Building Trade", tickangle=-45, title_font_color='#06c2ac', showgrid=False, showline=True, linewidth=1, linecolor='#59656d')
        fig05.update_yaxes(title_text='Mean Time Spent', title_font_color='#06c2ac', showgrid=True, gridwidth=0.1, gridcolor='#1f3b4d',
                           showline=True, linewidth=1, linecolor='#59656d')
        fig05.update_traces(marker_color='#06c2ac', marker_line_color='#06c2ac', marker_line_width=1)
        fig05.update_layout(title='Mean Time Spent to Recovered(hrs)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig05, use_container_width=True)

    with fig06, _lock:
        fig06 = go.Figure(data=[go.Bar(x=x, y=y6, orientation='v', text=y6,
                                textfont = dict(family='sana serif', size=14, color='#c4fff7'),
                                textposition = 'auto', textangle = -45, texttemplate = '%{text:.2f}')
                              ])
        fig06.update_xaxes(title_text="Building Trade", tickangle=-45, title_font_color='#137e6d', showgrid=False, showline=True, linewidth=1, linecolor='#59656d')
        fig06.update_yaxes(title_text='Total Time Spent', title_font_color='#137e6d', showgrid=True, gridwidth=0.1, gridcolor='#1f3b4d',
                           showline=True, linewidth=1, linecolor='#59656d')
        fig06.update_traces(marker_color='#137e6d', marker_line_color='#137e6d', marker_line_width=1)
        fig06.update_layout(title='Total Time Spent to Recovered(hrs)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig06, use_container_width=True)

    st.markdown('##')
    st.markdown('##')
    st.markdown(html_card_subheader_Tier2, unsafe_allow_html=True)
    st.markdown('##')

    df7 = df4.groupby(by=['Trade_Category']).agg(['count', 'max', 'min', 'mean', 'sum']).sort_values((     'Time_Acknowledged_hrs', 'count'), ascending=False)
    cols_name01 = ['Fault_Acknowledged_count', 'Fault_Acknowledged_max(hrs)', 'Fault_Acknowledged_min(hrs)', 'Fault_Acknowledged_mean(hrs)',
                   'Fault_Acknowledged_sum(hrs)', 'Fault_Site_Reached_count', 'Fault_Site_Reached_max(hrs)', 'Fault_Site_Reached_min(hrs)',
                   'Fault_Site_Reached_mean(hrs)', 'Fault_Site_Reached_sum(hrs)', 'Fault_Work_Started_count', 'Fault_Work_Started_max(hrs)',
                   'Fault_Work_Started_min(hrs)', 'Fault_Work_Started_mean(hrs)', 'Fault_Work_Started_sum(hrs)', 'Fault_Recovered_count',
                   'Fault_Recovered_max(hrs)', 'Fault_Recovered_min(hrs)', 'Fault_Recovered_mean(hrs)', 'Fault_Recovered_sum(hrs)']
    df7.columns = cols_name01
    df8 = df7.loc[:, ['Fault_Site_Reached_count', 'Fault_Site_Reached_mean(hrs)', 'Fault_Site_Reached_sum(hrs)',
                 'Fault_Recovered_count', 'Fault_Recovered_mean(hrs)', 'Fault_Recovered_sum(hrs)']]
    df8.reset_index(inplace=True)

    df_fig10 = df8.loc[:, ['Trade_Category', 'Fault_Recovered_count']].sort_values('Fault_Recovered_count', ascending=False).head(10)
    df_fig11 = df8.loc[:, ['Trade_Category', 'Fault_Recovered_mean(hrs)']].sort_values('Fault_Recovered_mean(hrs)', ascending=False).head(10)
    df_fig12 = df8.loc[:, ['Trade_Category', 'Fault_Recovered_sum(hrs)']].sort_values('Fault_Recovered_sum(hrs)', ascending=False).head(10)

    x_fig10 = df_fig10.Trade_Category
    y_fig10 = df_fig10['Fault_Recovered_count']
    x_fig11 = df_fig11.Trade_Category
    y_fig11 = df_fig11['Fault_Recovered_mean(hrs)']
    x_fig12 = df_fig12.Trade_Category
    y_fig12 = df_fig12['Fault_Recovered_sum(hrs)']

    fig10, fig11, fig12 = st.columns(3)
    with fig10, _lock:
        fig10 = go.Figure(data=[go.Bar(x=x_fig10, y=y_fig10, orientation='v', text=y_fig10,
                               textfont=dict(family='sana serif', size=14, color='#c4fff7'),
                               textposition='auto', textangle=-45)
                                ])
        fig10.update_xaxes(title_text="Trade Category", tickangle=-45, title_font_color='#50a747', showgrid=False,
                               showline=True, linewidth=1, linecolor='#59656d')
        fig10.update_yaxes(title_text='Count(Recovered)', title_font_color='#50a747', showgrid=True, gridwidth=0.1,
                               gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
        fig10.update_traces(marker_color='#50a747', marker_line_color='#50a747', marker_line_width=1)
        fig10.update_layout(title='Count(Recovered)-Top 10', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig10, use_container_width=True)

    with fig11, _lock:
        fig11 = go.Figure(data=[go.Bar(x=x_fig11, y=y_fig11, orientation='v', text=y_fig11,
                                textfont=dict(family='sana serif', size=14, color='#c4fff7'),
                                textposition='auto', textangle=-45, texttemplate='%{text:.2f}')
                                ])
        fig11.update_xaxes(title_text="Trade Category", tickangle=-45, title_font_color='#929901', showgrid=False,
                               showline=True, linewidth=1, linecolor='#59656d')
        fig11.update_yaxes(title_text='Mean Time Spent', title_font_color='#929901', showgrid=True, gridwidth=0.1,
                               gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
        fig11.update_traces(marker_color='#929901', marker_line_color='#929901', marker_line_width=1)
        fig11.update_layout(title='Mean Time Spent to Recovered(hrs)-Top 10', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig11, use_container_width=True)

    with fig12, _lock:
        fig12 = go.Figure(data=[go.Bar(x=x_fig12, y=y_fig12, orientation='v', text=y_fig12,
                               textfont=dict(family='sana serif', size=14, color='#c4fff7'),
                               textposition='auto', textangle=-45, texttemplate='%{text:.2f}')
                                ])
        fig12.update_xaxes(title_text="Trade Category", tickangle=-45, title_font_color='#ff9408', showgrid=False,
                               showline=True, linewidth=1, linecolor='#59656d')
        fig12.update_yaxes(title_text='Total Time Spent', title_font_color='#ff9408', showgrid=True, gridwidth=0.1,
                               gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
        fig12.update_traces(marker_color='#ff9408', marker_line_color='#ff9408', marker_line_width=1)
        fig12.update_layout(title='Total Time Spent to Recovered(hrs)-Top 10', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig12, use_container_width=True)

    st.markdown('##')
    st.markdown('##')
    st.markdown(html_card_subheader_Tier3, unsafe_allow_html=True)
    st.markdown('##')

    df9 = df4.groupby(by=['Type_of_Fault']).agg(['count', 'max', 'min', 'mean', 'sum']).sort_values((     'Time_Acknowledged_hrs', 'count'), ascending=False)
    cols_name02 = ['Fault_Acknowledged_count', 'Fault_Acknowledged_max(hrs)', 'Fault_Acknowledged_min(hrs)', 'Fault_Acknowledged_mean(hrs)',
                   'Fault_Acknowledged_sum(hrs)', 'Fault_Site_Reached_count', 'Fault_Site_Reached_max(hrs)', 'Fault_Site_Reached_min(hrs)',
                   'Fault_Site_Reached_mean(hrs)', 'Fault_Site_Reached_sum(hrs)', 'Fault_Work_Started_count', 'Fault_Work_Started_max(hrs)',
                   'Fault_Work_Started_min(hrs)', 'Fault_Work_Started_mean(hrs)', 'Fault_Work_Started_sum(hrs)', 'Fault_Recovered_count',
                   'Fault_Recovered_max(hrs)', 'Fault_Recovered_min(hrs)', 'Fault_Recovered_mean(hrs)', 'Fault_Recovered_sum(hrs)']
    df9.columns = cols_name02
    df10 = df9.loc[:, ['Fault_Site_Reached_count', 'Fault_Site_Reached_mean(hrs)', 'Fault_Site_Reached_sum(hrs)',
                 'Fault_Recovered_count', 'Fault_Recovered_mean(hrs)', 'Fault_Recovered_sum(hrs)']]
    df10.reset_index(inplace=True)

    df_fig16 = df10.loc[:, ['Type_of_Fault', 'Fault_Recovered_count']].sort_values('Fault_Recovered_count', ascending=False).head(10)
    df_fig17 = df10.loc[:, ['Type_of_Fault', 'Fault_Recovered_mean(hrs)']].sort_values('Fault_Recovered_mean(hrs)', ascending=False).head(10)
    df_fig18 = df10.loc[:, ['Type_of_Fault', 'Fault_Recovered_sum(hrs)']].sort_values('Fault_Recovered_sum(hrs)', ascending=False).head(10)


    x_fig16 = df_fig16.Type_of_Fault
    y_fig16 = df_fig16['Fault_Recovered_count']
    x_fig17 = df_fig17.Type_of_Fault
    y_fig17 = df_fig17['Fault_Recovered_mean(hrs)']
    x_fig18 = df_fig18.Type_of_Fault
    y_fig18 = df_fig18['Fault_Recovered_sum(hrs)']

    fig16, fig17, fig18 = st.columns(3)
    with fig16, _lock:
        fig16 = go.Figure(data=[go.Bar(x=x_fig16, y=y_fig16, orientation='v', text=y_fig16,
                             textfont=dict(family='sana serif', size=14, color='#c4fff7'),
                             textposition='auto', textangle=-45)
                                ])
        fig16.update_xaxes(title_text="Type of Fault", tickangle=-45, title_font_color='#d58a94', showgrid=False,
                           showline=True, linewidth=1, linecolor='#59656d')
        fig16.update_yaxes(title_text='Count(Recovered)', title_font_color='#d58a94', showgrid=True, gridwidth=0.1,
                           gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
        fig16.update_traces(marker_color='#d58a94', marker_line_color='#d58a94', marker_line_width=1)
        fig16.update_layout(title='Count(Recovered)-Top 10', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig16, use_container_width=True)

    with fig17, _lock:
        fig17 = go.Figure(data=[go.Bar(x=x_fig17, y=y_fig17, orientation='v', text=y_fig17,
                             textfont=dict(family='sana serif', size=14, color='#c4fff7'),
                             textposition='auto', textangle=-45, texttemplate='%{text:.2f}')
                                ])
        fig17.update_xaxes(title_text="Type of Fault", tickangle=-45, title_font_color='#ff796c', showgrid=False,
                           showline=True, linewidth=1, linecolor='#59656d')
        fig17.update_yaxes(title_text='Mean Time Spent', title_font_color='#ff796c', showgrid=True, gridwidth=0.1,
                           gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
        fig17.update_traces(marker_color='#ff796c', marker_line_color='#ff796c', marker_line_width=1)
        fig17.update_layout(title='Mean Time Spent to Recovered(hrs)-Top 10', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig17, use_container_width=True)

    with fig18, _lock:
        fig18 = go.Figure(data=[go.Bar(x=x_fig18, y=y_fig18, orientation='v', text=y_fig18,
                             textfont=dict(family='sana serif', size=14, color='#c4fff7'),
                             textposition='auto', textangle=-45, texttemplate='%{text:.2f}')
                                ])
        fig18.update_xaxes(title_text="Type of Fault", tickangle=-45, title_font_color='#ba6873', showgrid=False,
                           showline=True, linewidth=1, linecolor='#59656d')
        fig18.update_yaxes(title_text='Total Time Spent', title_font_color='#ba6873', showgrid=True, gridwidth=0.1,
                           gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
        fig18.update_traces(marker_color='#ba6873', marker_line_color='#ba6873', marker_line_width=1)
        fig18.update_layout(title='Total Time Spent to Recovered(hrs)-Top 10', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig18, use_container_width=True)

    st.markdown('##')
    st.markdown('##')
    st.markdown(html_card_subheader_location, unsafe_allow_html=True)
    st.markdown('##')

    df11 = df4.groupby(by=['Building']).agg(['count', 'max', 'min', 'mean', 'sum'])
    cols_name_location = ['Fault_Acknowledged_count', 'Fault_Acknowledged_max(hrs)', 'Fault_Acknowledged_min(hrs)', 'Fault_Acknowledged_mean(hrs)',
                   'Fault_Acknowledged_sum(hrs)', 'Fault_Site_Reached_count', 'Fault_Site_Reached_max(hrs)', 'Fault_Site_Reached_min(hrs)',
                   'Fault_Site_Reached_mean(hrs)', 'Fault_Site_Reached_sum(hrs)', 'Fault_Work_Started_count', 'Fault_Work_Started_max(hrs)',
                   'Fault_Work_Started_min(hrs)', 'Fault_Work_Started_mean(hrs)', 'Fault_Work_Started_sum(hrs)', 'Fault_Recovered_count',
                   'Fault_Recovered_max(hrs)', 'Fault_Recovered_min(hrs)', 'Fault_Recovered_mean(hrs)', 'Fault_Recovered_sum(hrs)']
    df11.columns = cols_name_location
    df12 = df11.loc[:, ['Fault_Recovered_count', 'Fault_Recovered_sum(hrs)']]

    x_fig19 = df12['Fault_Recovered_count'].sort_values().index
    y_fig19 = df12['Fault_Recovered_count'].sort_values().values

    x_fig20 = df12['Fault_Recovered_sum(hrs)'].sort_values().index
    y_fig20 = df12['Fault_Recovered_sum(hrs)'].sort_values().values


    fig19, fig20 = st.columns(2)
    with fig19, _lock:
        fig19 = go.Figure(data=[go.Bar(x=y_fig19, y=x_fig19, orientation='h', text=y_fig19,
                             textfont=dict(family='sana serif', size=14, color='#c4fff7'),
                             textposition='auto', textangle=0)
                                ])
        fig19.update_xaxes(title_text="Number of Fault", title_font_color='#728f02', showgrid=True,
                           gridwidth=0.1, gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
        fig19.update_yaxes(title_text='Building', title_font_color='#728f02', showgrid=False, showline=True, linewidth=1, linecolor='#59656d', tickmode='linear')
        fig19.update_traces(marker_color='#728f02', marker_line_color='#728f02', marker_line_width=1)
        fig19.update_layout(title='Number of Fault vs Building', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig19, use_container_width=True)

    with fig20, _lock:
        fig20 = go.Figure(data=[go.Bar(x=y_fig20, y=x_fig20, orientation='h', text=y_fig20,
                               textfont=dict(family='sana serif', size=14, color='#c4fff7'),
                               textposition='auto', textangle=0, texttemplate='%{text:.2f}')
                                ])
        fig20.update_xaxes(title_text="Total Time Spent", title_font_color='#516572', showgrid=True, gridwidth=0.1,
                           gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
        fig20.update_yaxes(title_text='Building', title_font_color='#516572', showgrid=False, showline=True, linewidth=1, tickmode='linear')
        fig20.update_traces(marker_color='#516572', marker_line_color='#516572', marker_line_width=1)
        fig20.update_layout(title='Total Time Spent(hrs) vs Building', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig20, use_container_width=True)







# --------------------------------------Inventories----------------------------------------------------------------------
# if page =='Inventories':
#     use_cols =['Description', 'Category', 'Subcategory', 'Ref. ID', 'Reference Location', 'Quantity', 'Request to draw or add',
#            'Reference number', 'Created date']
#     date=['Created date']
#     dfALH = pd.read_excel('Transaction 2021-12-05 212104(ALH).xlsx', header=1, usecols=use_cols, parse_dates=date)
#     dfALH['Created day'] = dfALH['Created date'].dt.day
#
#     dfECH4 = pd.read_excel('Transaction 2021-12-05 212104(EC-H4).xlsx', header=1, usecols=use_cols, parse_dates=date)
#     dfECH4['Created day'] = dfECH4['Created date'].dt.day
#
#     serALH_daily = dfALH.groupby(by=['Created day'])['Request to draw or add'].sum()
#     serALHfast = dfALH.groupby(by=['Description'])['Request to draw or add'].sum().sort_values(ascending=False).head(20)
#
#     html_card_title_inventories="""
#         <div class="card">
#           <div class="card-body" style="border-radius: 10px 10px 0px 0px; padding-top: 5px; width: 800px;
#            height: 50px;">
#             <h1 class="card-title" style=color:#ff4f00; font-family:Georgia; text-align: left; padding: 0px 0;">INVENTORIES MOVEMENT Nov 2021</h1>
#           </div>
#         </div>
#         """
#     st.markdown(html_card_title_inventories, unsafe_allow_html=True)
#     st.markdown('##')
#     st.markdown('##')
#     st.subheader('ALH')
#
#     total_inventory_balanceALH = dfALH['Quantity'].sum()
#     #total_inventory_requestedALH = dfALH['Request to draw or add'].sum()
#     total_inventory_requestedALH = 0
#     total_replenishmentALH = 0
#
#     column01_inventory, column02_inventory, column03_inventory = st.columns(3)
#
#     with column01_inventory, _lock:
#         st.markdown('**Balance**')
#         st.markdown(f"<h2 style='text-align: left; color: #703bef;'>{total_inventory_balanceALH}</h2>", unsafe_allow_html=True)
#     with column02_inventory, _lock:
#         st.markdown('**Requested**')
#         st.markdown(f"<h2 style='text-align: left; color: #3c9992;'>{total_inventory_requestedALH}</h2>", unsafe_allow_html=True)
#     with column03_inventory, _lock:
#         st.markdown('**Replenishment**')
#         st.markdown(f"<h2 style='text-align: left; color: #d0c101;'>{total_replenishmentALH}</h2>", unsafe_allow_html=True)
#
#
#     st.markdown('##')
#     st.subheader('EC-H4')
#
#     total_inventory_balanceECH4 = dfECH4['Quantity'].sum()
#     total_inventory_requestedECH4 = dfECH4['Request to draw or add'].sum()
#     total_replenishmentECH4 = 0
#
#     column04_inventory, column05_inventory, column06_inventory = st.columns(3)
#
#     with column04_inventory, _lock:
#         st.markdown('**Balance**')
#         st.markdown(f"<h2 style='text-align: left; color: #703bef;'>{total_inventory_balanceECH4}</h2>",
#                     unsafe_allow_html=True)
#     with column05_inventory, _lock:
#         st.markdown('**Requested**')
#         st.markdown(f"<h2 style='text-align: left; color: #3c9992;'>{total_inventory_requestedECH4}</h2>",
#                     unsafe_allow_html=True)
#     with column06_inventory, _lock:
#         st.markdown('**Replenishment**')
#         st.markdown(f"<h2 style='text-align: left; color: #d0c101;'>{total_replenishmentECH4}</h2>",
#                     unsafe_allow_html=True)
#
#     html_card_subheader_inventoriesALH = """
#         <div class="card">
#           <div class="card-body" style="border-radius: 10px 10px 0px 0px; background:#ff4f00; padding-top: 5px; width: 600px;
#            height: 50px;">
#             <h3 class="card-title" style="background-color:#ff4f00; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">Inventory Movement Morning-ALH</h3>
#           </div>
#         </div>
#         """
#     st.markdown('##')
#     st.markdown('##')
#     st.markdown(html_card_subheader_inventoriesALH, unsafe_allow_html=True)
#     st.markdown('##')
#
#     xinventories_daily_ALH = serALH_daily.index
#     yinventories_daily_ALH = serALH_daily.values
#     yinventories_mean_ALH = serALH_daily.values.mean()
#
#     xinventories_fast_ALH = serALHfast.index
#     yinventories_fast_ALH = serALHfast.values
#
#     figinventories_daily, figinventories_fast = st.columns(2)
#
#     with figinventories_daily, _lock:
#         figinventories_daily = go.Figure(data=go.Scatter(x=xinventories_daily_ALH, y=yinventories_daily_ALH, mode='lines+markers+text', line=dict(color='#13bbaf', width=3),
#                                 text=yinventories_daily_ALH, textfont=dict(family='sana serif', size=14, color='#c4fff7'), textposition='top center'))
#         figinventories_daily.add_hline(y=yinventories_mean_ALH, line_dash='dot', line_color='#96ae8d', line_width=2, annotation_text='Average Line',
#                                 annotation_position='bottom right', annotation_font_size=18, annotation_font_color='green')
#         figinventories_daily.update_xaxes(title_text='Date', tickangle=-45, title_font_color='#74a662', tickmode='linear',
#                                    range=[1, 31], showgrid=False, showline=True, linewidth=1, linecolor='#59656d')
#         figinventories_daily.update_yaxes(title_text='Number of Inventory', title_font_color='#74a662', showgrid=False,
#                                    gridwidth=0.1, gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
#         figinventories_daily.update_layout(title='Daily Movement', plot_bgcolor='rgba(0, 0, 0, 0)',
#                                  # xaxis=dict(showticklabels=True, ticks='outside', tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)')),
#                                  # yaxis=dict(showticklabels=True, ticks='outside', tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)'))
#                                  )
#         st.plotly_chart(figinventories_daily, use_container_width=True)
#
#
#     with figinventories_fast, _lock:
#         figinventories_fast = go.Figure(data=[go.Bar(x=yinventories_fast_ALH, y=xinventories_fast_ALH, text=yinventories_fast_ALH,
#                                                      orientation='h', textfont=dict(family='sana serif', size=14, color='#c4fff7'),
#                                                     textposition='outside', textangle=0)
#                                             ])
#         figinventories_fast.update_xaxes(title_text="Number of Inventory", tickangle=-45, title_font_color='#087871', showgrid=True,
#                                          gridwidth=0.1, gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
#         figinventories_fast.update_yaxes(title_text='Description', title_font_color='#087871', showgrid=False, gridwidth=0.1,
#                             gridcolor='#1f3b4d', showline=True, linewidth=1, linecolor='#59656d')
#         figinventories_fast.update_traces(marker_color='#087871', marker_line_color='#087871', marker_line_width=1)
#         figinventories_fast.update_layout(title='Fast Moving Inventories-Top20', plot_bgcolor='rgba(0,0,0,0)')
#         st.plotly_chart(figinventories_fast, use_container_width=True)
#
#     html_card_subheader_inventoriesECH4 = """
#         <div class="card">
#           <div class="card-body" style="border-radius: 10px 10px 0px 0px; background:#ff4f00; padding-top: 5px; width: 600px;
#            height: 50px;">
#             <h3 class="card-title" style="background-color:#ff4f00; color:#eabd1d; font-family:Georgia; text-align: center; padding: 0px 0;">Inventory Movement Morning-ECH4</h3>
#           </div>
#         </div>
#         """
#     st.markdown('##')
#     st.markdown('##')
#     st.markdown(html_card_subheader_inventoriesECH4, unsafe_allow_html=True)
#     st.markdown('##')
#     st.dataframe(dfECH4)

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)
