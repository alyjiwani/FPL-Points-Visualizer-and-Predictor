import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import requests
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

num_gameweeks = 39
num_players = 3
gameweeks = list(range(num_gameweeks))
false_id = [0] * num_gameweeks

bg_colour = '#121212'
font_colour = '#FFFFFF'
player_colours = ['#e43075', '#5dca36', '#2474a3']

def make_graph(player_data, player_names=None):
    base_graph = go.Figure()
    for i, (current_x, current_y, future_x, future_y) in enumerate(player_data):
        name = player_names[i] if player_names else f"Player {i+1}"
        base_graph.add_trace(
            go.Scatter(
                name=f"{name} - Current",
                x=current_x, y=current_y, mode='lines+markers', hoverinfo='x+y',
                line=dict(color=player_colours[i], dash='solid'),
                marker=dict(symbol='circle', color=player_colours[i])
            )
        )
        base_graph.add_trace(
            go.Scatter(
                name=f"{name} - Future",
                x=future_x, y=future_y, mode='lines+markers', hoverinfo='x+y',
                line=dict(color=player_colours[i], dash='dash'),
                marker=dict(symbol='circle', color=player_colours[i])
            )
        )
    base_graph.update_layout(
        font=dict(color=font_colour),
        xaxis_title="Gameweeks",
        yaxis_title="Points",
        margin={'t': 25, 'l': 0, 'r': 0, 'b': 0},
        plot_bgcolor=bg_colour,
        paper_bgcolor=bg_colour
    )
    base_graph.update_xaxes(showline=True, linewidth=1, range=[0, num_gameweeks-1], linecolor=font_colour, showgrid=False)
    base_graph.update_yaxes(showline=True, linewidth=1, range=[0, 2500], linecolor=font_colour, showgrid=False)
    return base_graph

def data_model(team_id):
    response = requests.get(f"https://fantasy.premierleague.com/api/entry/{team_id}/history/")
    data = response.json().get("current", [])

    if response.status_code == 404 or not data:
        return [false_id, []]
    
    start_week = data[0].get("event", 1)
    current_points = [0] * (start_week if start_week > 1 else 1)
    current_points += [week.get("total_points", 0) for week in data]
    try:
        model = ExponentialSmoothing(
            endog=current_points, trend='additive',
            damped_trend=False, seasonal=None,
            initialization_method='estimated'
        )
        model_fit = model.fit(optimized=True)
        forecast = model_fit.forecast(num_gameweeks - len(current_points))
        future_results = np.round(forecast)
    except Exception:
        future_results = []
    return [current_points, future_results]

def get_manager_name(team_id):
    try:
        response = requests.get(f"https://fantasy.premierleague.com/api/entry/{team_id}/")
        data = response.json()
        first = data.get("player_first_name", "")
        last = data.get("player_last_name", "")
        if first or last:
            return f"{first} {last}".strip()
    except Exception:
        pass
    return f"Player {team_id}"

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'FPL Points Visualizer & Predictor'
server = app.server

app.layout = html.Div(children=[
    html.Div([
        html.H4(children='FPL Points Visualizer & Predictor',
                style={'color': font_colour, 'backgroundColor': bg_colour, 'margin-top': 0}),
        html.H6(children="View your past Gameweek Points and see where you may end up by Gameweek 38. "
                         "Add your friends' Team IDs to see how you stack up!",
                style={'color': font_colour}),
        html.H6(children='For more information about the statistical model used and source code for the app, '
                         'click the link ->    ',
                style={'color': font_colour, 'display': 'inline'}),
        html.A('Github - Aly J.',
               href='https://github.com/alyjiwani/FPL-Points-Visualizer-and-Predictor',
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
                figure=make_graph([([], [], [], []) for _ in range(num_players)], [""]*num_players),
                style=dict(height='80vh')
            )
        ], className='ten columns')
    ], className='row', style={'text-align': 'center'})
], style=dict(backgroundColor=bg_colour, height='100vh', width='100vw'))

@app.callback(Output('points-graph', 'figure'),
              [Input('generator', 'n_clicks')],
              [State('id-1', 'value'), State('id-2', 'value'), State('id-3', 'value')])
def update_graph(clicks, id_1, id_2, id_3):
    ids = [id_1, id_2, id_3]
    if not any(ids):
        raise PreventUpdate
    player_data = []
    player_names = []
    for idx, team_id in enumerate(ids):
        if team_id is not None:
            points, future = data_model(team_id)
            current_x = gameweeks[:len(points)]
            future_x = gameweeks[len(points):len(points)+len(future)]
            player_data.append((current_x, points, future_x, future))
            player_names.append(get_manager_name(team_id))
        else:
            player_data.append(([], [], [], []))
            player_names.append(f"Player {idx+1}")
    return make_graph(player_data, player_names)

if __name__ == '__main__':
    app.run(debug=True)
