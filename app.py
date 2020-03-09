import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import requests
import numpy
import statsmodels
from statsmodels.tsa.holtwinters import ExponentialSmoothing

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gameweeks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
             29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
false_id = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

bg_colour = '#121212'
font_colour = '#FFFFFF'
player1_colour = '#e43075'
player2_colour = '#5dca36'
player3_colour = '#2474a3'


def make_graph(x11, y11, x12, y12, x21, y21, x22, y22, x31, y31, x32, y32):
    base_graph = go.Figure()
    base_graph.add_trace(
        go.Scatter(name="Player 1 - Current", x=x11, y=y11, mode='lines+markers', hoverinfo='x+y',
                   line=dict(color=player1_colour, dash='solid'), marker=dict(symbol='circle', color=player1_colour)))
    base_graph.add_trace(
        go.Scatter(name="Player 1 - Future", x=x12, y=y12, mode='lines+markers', hoverinfo='x+y',
                   line=dict(color=player1_colour, dash='dash'), marker=dict(symbol='circle', color=player1_colour)))
    base_graph.add_trace(
        go.Scatter(name="Player 2 - Current", x=x21, y=y21, mode='lines+markers', hoverinfo='x+y',
                   line=dict(color=player2_colour, dash='solid'), marker=dict(symbol='circle', color=player2_colour)))
    base_graph.add_trace(
        go.Scatter(name="Player 2 - Future", x=x22, y=y22, mode='lines+markers', hoverinfo='x+y',
                   line=dict(color=player2_colour, dash='dash'), marker=dict(symbol='circle', color=player2_colour)))
    base_graph.add_trace(
        go.Scatter(name="Player 3 - Current", x=x31, y=y31, mode='lines+markers', hoverinfo='x+y',
                   line=dict(color=player3_colour, dash='solid'), marker=dict(symbol='circle', color=player3_colour)))
    base_graph.add_trace(
        go.Scatter(name="Player 3 - Future", x=x32, y=y32, mode='lines+markers', hoverinfo='x+y',
                   line=dict(color=player3_colour, dash='dash'), marker=dict(symbol='circle', color=player3_colour)))
    base_graph.update_layout(font=dict(color=font_colour), xaxis_title="Gameweeks", yaxis_title="Points",
                             margin={'t': 25, 'l': 0, 'r': 0, 'b': 0},
                             plot_bgcolor=bg_colour, paper_bgcolor=bg_colour)
    base_graph.update_xaxes(showline=True, linewidth=1, range=[0, 40], linecolor=font_colour, showgrid=False)
    base_graph.update_yaxes(showline=True, linewidth=1, range=[0, 2500], linecolor=font_colour, showgrid=False)
    return base_graph


def data_model(team_id):
    # Retrieving Data
    response = requests.get("https://fantasy.premierleague.com/api/entry/{0}/history/".format(team_id))

    if response.status_code == 404:
        return [false_id, []]

    # Add Data into Arrays
    start_week = response.json()["current"][0].get("event")
    current_points = [0]
    if start_week != 1:
        for x in range(1, start_week):
            current_points.append(0)
        for week in response.json()["current"]:
            current_points.append(week.get("total_points"))
    else:
        for week in response.json()["current"]:
            current_points.append(week.get("total_points"))

    # Model the Data
    model = statsmodels.tsa.holtwinters.ExponentialSmoothing(current_points, 'add', False, None)

    # Fit the Model
    model_fit = model.fit()

    # Forecast Data
    forecast = model_fit.forecast(len(gameweeks) - len(current_points))
    future_results = numpy.round(forecast)

    plot = [current_points, future_results]

    return plot


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'FPL Points Visualizer & Predictor'

server = app.server

app.layout = html.Div(children=[
    html.Div([
        html.H4(children='FPL Points Visualizer & Predictor (2019-2020 Season)',
                style={'color': font_colour, 'backgroundColor': bg_colour, 'margin-top': 0}),
        html.H6(children="View your past Gameweek Points and see where you may end up by Gameweek 38. "
                         "Add your friends' Team IDs to see how you stack up!",
                style={'color': font_colour}),
        html.H6(children='For more information about the statistical model used and source code for the app, '
                         'click the link ->    ',
                style={'color': font_colour, 'display': 'inline'}),
        html.A('Github - Aly J.',
               href='https://github.com/OMGitsAlyJ/FPL-Points-Visualizer-and-Predictor',
               style={'color': font_colour, 'font-size': 20})
    ], style={'margin-left': 10}),
    html.Div([
        html.Div([
            html.Div(dcc.Input(id='id-1', type='number', placeholder='Team ID', min=0), style={'color': font_colour}),
            html.Div(dcc.Input(id='id-2', type='number', placeholder='Team ID', min=0),
                     style={'margin-top': 5, 'color': font_colour}),
            html.Div(dcc.Input(id='id-3', type='number', placeholder='Team ID', min=0),
                     style={'margin-top': 5, 'color': font_colour}),
            html.Button('Generate', id='generator', style={'margin-top': 5, 'color': font_colour}),
            html.Div(id='output-container-button-1',
                     children='Enter your Team ID(s) and press Generate', style={'margin-top': 5, 'color': font_colour})
        ], className='two columns', style={'margin-top': '30vh'}),
        html.Div([
            dcc.Graph(
                id='points-graph',
                figure=make_graph([], [], [], [], [], [], [], [], [], [], [], []),
                style=dict(height='80vh')
            )
        ], className='ten columns')
    ], className='row', style={'text-align': 'center'})
], style=dict(backgroundColor=bg_colour, height='100vh', width='100vw'))


@app.callback(Output('points-graph', 'figure'),
              [Input('generator', 'n_clicks')],
              [State('id-1', 'value'), State('id-2', 'value'), State('id-3', 'value')])
def update_graph(clicks, id_1, id_2, id_3):
    updated_graph = go.Figure()
    if id_1 is None and id_2 is None and id_3 is None:
        raise PreventUpdate
    elif id_1 is not None and id_2 is None and id_3 is None:
        plot1 = data_model(id_1)
        updated_graph = make_graph(gameweeks[0: len(plot1[0])], plot1[0], gameweeks[len(plot1[0]):], plot1[1],
                                   [], [], [], [], [], [], [], [])
    elif id_2 is not None and id_1 is None and id_3 is None:
        plot2 = data_model(id_2)
        updated_graph = make_graph([], [], [], [], gameweeks[0: len(plot2[0])], plot2[0],
                                   gameweeks[len(plot2[0]):], plot2[1], [], [], [], [])
    elif id_3 is not None and id_1 is None and id_2 is None:
        plot3 = data_model(id_3)
        updated_graph = make_graph([], [], [], [], [], [], [], [],
                                   gameweeks[0: len(plot3[0])], plot3[0], gameweeks[len(plot3[0]):], plot3[1])
    elif id_1 is not None and id_2 is not None and id_3 is None:
        plot1 = data_model(id_1)
        plot2 = data_model(id_2)
        updated_graph = make_graph(gameweeks[0: len(plot1[0])], plot1[0], gameweeks[len(plot1[0]):], plot1[1],
                                   gameweeks[0: len(plot2[0])], plot2[0], gameweeks[len(plot2[0]):], plot2[1],
                                   [], [], [], [])
    elif id_2 is not None and id_3 is not None and id_1 is None:
        plot2 = data_model(id_2)
        plot3 = data_model(id_3)
        updated_graph = make_graph([], [], [], [],
                                   gameweeks[0: len(plot2[0])], plot2[0], gameweeks[len(plot2[0]):], plot2[1],
                                   gameweeks[0: len(plot3[0])], plot3[0], gameweeks[len(plot3[0]):], plot3[1])
    elif id_1 is not None and id_3 is not None and id_2 is None:
        plot1 = data_model(id_1)
        plot3 = data_model(id_3)
        updated_graph = make_graph(gameweeks[0: len(plot1[0])], plot1[0], gameweeks[len(plot1[0]):], plot1[1],
                                   [], [], [], [],
                                   gameweeks[0: len(plot3[0])], plot3[0], gameweeks[len(plot3[0]):], plot3[1])
    elif id_1 is not None and id_3 is not None and id_2 is not None:
        plot1 = data_model(id_1)
        plot2 = data_model(id_2)
        plot3 = data_model(id_3)
        updated_graph = make_graph(gameweeks[0: len(plot1[0])], plot1[0], gameweeks[len(plot1[0]):], plot1[1],
                                   gameweeks[0: len(plot2[0])], plot2[0], gameweeks[len(plot2[0]):], plot2[1],
                                   gameweeks[0: len(plot3[0])], plot3[0], gameweeks[len(plot3[0]):], plot3[1])
    return updated_graph


if __name__ == '__main__':
    app.run_server(debug=True)
