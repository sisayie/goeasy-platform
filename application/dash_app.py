import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from datetime import date, datetime

import pandas as pd

def gep_dash():
    external_stylesheets = ['assets/style.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    def get_data(data_url):
        print(data_url)
        df0 = pd.read_json (data_url)
        df0 = df0.drop('tpv_defined_behaviour', 1)
        return df0
        
    PAGE_SIZE = 5
    app.layout = html.Div([
        html.H1(children='Dashboard for GEP', style={'backgroundColor':'#B3ECFF', 'font_size': '80px','textAlign': 'center'}),
        html.Div(children='Select date range'),
        html.Div(dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=date(2020, 7, 1), #.strftime('%Y-%m-%d %H:%M:%S'),
            max_date_allowed = date.today(), #.strftime('%Y-%m-%d %H:%M:%S'),
            initial_visible_month=date(2020, 12, 5), #.strftime('%Y-%m-%d %H:%M:%S'),
            start_date = date(2020,12,10), #.strftime('%Y-%m-%d %H:%M:%S'),
            end_date = date.today() #.strftime('%Y-%m-%d %H:%M:%S')
        )),
        html.Div(id='output-container-date-picker-range', style={'width': '100%', 'display': 'inline-block'}),
        html.Div(className = 'row',
                children = [
                dcc.Graph(
                    id = 'graph_2',
                    ),
                dcc.Graph(
                    id='graph_1',
                    #figure=fig
                    )
                    ]
        ),
        html.Div(children='Daily tracks of journeys'),
        html.Div(id='data_url', style= {'display': 'none'}),
        html.Div(id="table1")
        ])
        #   Get parameters from users for url
    @app.callback(
        Output('data_url', 'children'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        )
    def get_url(start_time, end_time):
        url_base = "https://galileocloud.goeasyproject.eu/GEP/paib/publicstorage/journey/times"
        s_time = datetime.strptime(start_time, '%Y-%m-%d') #convert to matching format
        e_time = datetime.strptime(end_time, '%Y-%m-%d') #convert to matching format
        url = '{}?start_time={}&end_time={}'.format(url_base, s_time, e_time)
        url_enc = url.replace(' ', '%20')
        return url_enc 
    
    # Update table here
    @app.callback(
        Output('table1', 'children'),
        Input('data_url', 'children'),
        )
    def update_table(data_url):
        df0 = get_data(data_url)
        #print(df)
        #dfgb = df.groupby(['startdate']).count()
        df1 = pd.DataFrame()
        df1['Journey'] = range(1, len(df0) + 1)
        df1['journeyId'] = df0['journeyId']
        df1['startdate'] = df0['startdate']
        df1['enddate'] = df0['enddate']
        df1['elapsedtime'] = df0['elapsedtime']
        df1['distance'] = df0['distance']
        df1['tpmmd'] = df0['tpmmd']
        
        df = df1 #pd.concat([df1, df0], axis = 1)
        data = df.to_dict('records')
        #columns =  [{"name": i, "id": i,} for i in (df.columns)] #show all columns in df
        
        #show selected columns in df
        columns=[{'name': i, 'id': i} for i in df.loc[:,['startdate','enddate', 'distance', 'elapsedtime', 'tpmmd']]]
        page_current=0,
        page_size=5, #PAGE_SIZE,
        #return dash_table.DataTable(data=data, columns=columns) 
        return html.Div([
			dash_table.DataTable(
				id='table',
				columns=[{"name": i, "id": i} for i in df.columns],
				data=df.to_dict("records"),
                style_cell={
                    'width': '300px',
                    'height': '60px',
                    'textAlign': 'left',
                    'padding': '5px',
                    'color':'blue',
                    'font_size': '20px',
                    },
                page_current=0,
                page_size=PAGE_SIZE,
                style_header={
                    'backgroundColor': '#B3ECFF',
                    'fontWeight': 'bold',
                    'color':'black'
                },
                style_table={
                    'overflowY': 'scroll'
                })
			])
    @app.callback(
        Output('graph_1', 'figure'),
        Input('data_url', 'children'),
        )
    def update_graph(data_url):
        df = get_data(data_url)
        #df2 = df0.drop('tpv_defined_behaviour', 1)
        df['startdate'] = pd.to_datetime(df['startdate'])
        df['enddate'] = pd.to_datetime(df['enddate'])
        df['s_date'] = df['startdate'].map(lambda x: x.strftime('%Y-%m-%d'))
        #df2=pd.melt(df2,id_vars=['s_date'],var_name='gender', value_name='value')
        
        # Group data by keys and get sum
        xData = []
        yData = []
        for group, data in df.groupby(['s_date']):
            xData.append(group)
            yData.append(data['distance'].count()) #yData.append(data['distance'].sum())
        print(df.columns)
        #dfgb = df.groupby(['startdate']).count()
        '''fig = px.bar(df2, 
            x="s_date",     
            y='distance', 
            barmode="group",
            title="Daily Tracks",
            height=600
            )'''
        fig={
            'data': [
                {'x':xData, 'y': yData, 'type': 'bar'},
            ],
            'layout': {}
            }
        return fig
    return app
    
if __name__ == '__main__':
    app = gep_dash()
    app.run_server(debug = False, port=8047, host='127.0.0.1', dev_tools_ui=False,dev_tools_props_check=False) #, dev_tools_ui=False,dev_tools_props_check=False) 