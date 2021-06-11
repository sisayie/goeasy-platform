import folium
import requests
import json
import pandas as pd

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

def getJourney(journeyId):
    print(journeyId)
    url_str = 'https://anonengine:5003/paib/publicstorage/'+str(journeyId)
    #url_str = 'https://galileocloud.goeasyproject.eu/GEP/paib/publicstorage/'+str(journeyId)
    #https://galileocloud.goeasyproject.eu/GEP/paib/publicstorage/ad805ce7-448f-4845-8e38-80840ae5af59
    headers = {"Accept": "application/json"}
    response = requests.get(url_str, headers = headers)
    journey = json.loads(response.content)
    return journey
    
def getPositions(journey):
    #print(json_data)
    latitude_list = []
    longitude_list = []
    if journey is not None:
        if journey.get('positions') is not None:
            for position in journey.get('positions'): # TODO: This is for one route. For multiple routes, use "for route in json_data: for position in route: ..."
                #print(position)
                latitude_list.append(position['lat'])
                longitude_list.append(position['lon'])
            return latitude_list, longitude_list
        else:
            return "Journey without positions"
    else:
        return "Journey not found"
    
def mapping(positions):
    routes_map = folium.Map(prefer_canvas=True)
    lats, lons = positions #getPositions(getJourney(journey_id))
    def plotDot(point):
        '''input: series that contains a numeric latitude and a numeric longitude
        this function creates a CircleMarker and adds it to routes_map'''
        folium.CircleMarker(location=[point.latitude, point.longitude],
                            radius=2,
                            weight=10).add_to(routes_map)
    data = pd.DataFrame(zip(lats,lons), columns = ['latitude', 'longitude'])
    data.apply(plotDot, axis = 1)

    #Set the zoom
    routes_map.fit_bounds(routes_map.get_bounds())
    
    '''
    #routes_map.save('using_folium12.html')
    routes_map.save(outfile)
    webbrowser.open(outfile, new=2)
    #return routes_map
    '''
    html_string = routes_map._repr_html_()
    return html_string

def get_route(journey_id):
    #TODO: show for multiple journeys
    '''for j in journey_ids:
        display(mapping(getPositions(getJourney(j))))'''
    #display(mapping(getPositions(getJourney(id))))
    ####journey_id = '035d32fe-6d8d-4b02-adb7-172e5f54b3f7' #'ad805ce7-448f-4845-8e38-80840ae5af59'
    journey = getJourney(journey_id)
    print(journey)
    positions = getPositions(journey)
    #print(positions)
    return mapping(positions) #flask.render_template_string(html_string) #to feed into a template
    #return 'Ok'
'''
def service_a():  # A function to get service from container A
    # use the docker container name and port
    url_str = 'http://dashboard:7009/' # this points to the same location as url_str = 'http://localhost:8009/'
    print(url_str)
    headers = {"Accept": "application/json",
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/86.0.4240.111 Safari/537.36'
               }
    response = requests.get(url_str, headers=headers, verify=False)#.json()
    return response
    #response_data = json.loads(response.content)
    #return response_data
'''    

def dash_funcs(dash_app):
    # styling the sidebar
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # padding for the page content
    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    sidebar = html.Div(
        [
            #html.H2("GOEASY", className="display-4"),
            html.Hr(),
            html.P("Data in Public Storage", className="lead"),
            dbc.Nav(
                [
                    #dbc.NavLink("Home", href="http://localhost/paib/dashboard/page-1", active="exact"),
                    dbc.NavLink("Journeys", href="/paib/dash/page-2", active="exact"),
                    dbc.NavLink("Positions", href="/paib/dash/page-1", active="exact"),
                    dbc.NavLink("Route Map", href="/paib/dash/page-3", active="exact"),
                    dbc.NavLink("App2", href="/paib/dash/app-2", active="exact"),
                    #dbc.NavLink("Map", href="/paib/dash/map", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

    dash_app.layout = html.Div([
        dcc.Location(id="url"),
        sidebar,
        content
    ])
    @dash_app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def render_page_content(pathname):
        '''if pathname == "/paib/dash/map":
            return [
                    html.H1('Map'),
                    html.Iframe(id="maps", srcDoc=map_dashboard(), width="100%",height="600")
                   ]'''
        if pathname == "/paib/dash/home":
            return [
                html.H1('Goeasy Dashboard'),
                html.TODO("to get journeys, positions and route map")
                #html.Iframe(id="journeys", src=dash_func(dash_app), width="100%", height="100%")
                #html.Iframe(id="journeys", src=dash_func(), width="100%", height="600")
                ]
                
        elif pathname == "/paib/dash/page-1":
            return [html.H1('Positions'),
                    html.Iframe(id="positions", src="http://localhost:5004/positions/27c72c36-09c4-4d3b-8615-dab8b55d8d47", width="100%", height="600")
                    ]
                    
        elif pathname == "/paib/dash/page-2":
            return [
                html.H1('Routes for journey'),
                # html.Textarea(id="input_id", name="input_name"),
                html.Iframe(id="route", src='http://localhost:8008/apps/app2', width='100%', height='600')
                #html.Iframe(id="route", src='http://dashboard:7009/', width='100%', height='600')
                #html.Iframe(id="route", srcDoc=service_a(), width='100%', height='600')
            ]
            
        elif pathname == "/paib/dash/page-3": #get_path(dash_app) 
            return [
            html.H1('Routes for journey'),
            dcc.Input(id="input", placeholder="Enter journey id", type="text"),
            html.P(id="output"),
            html.Iframe(id="route1", src='http://localhost:5004/routes/27c72c36-09c4-4d3b-8615-dab8b55d8d47', width='100%', height='600')
            ]
        
        elif pathname == "/paib/dash/app-2": 
            return [
            html.H1('Routes for journey2'),
            dcc.Input(id="input", placeholder="Enter journey id", type="text"),
            html.P(id="output"),
            html.Iframe(id="route2", src='http://localhost:8008', width='100%', height='600')
            ]
            
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )
    return dash_app