# FPL Points Visualizer and Predictor
https://fpl-visualizer.herokuapp.com/
This web app is a point visualizer for the 2019-2020 Fantasy Premier League season. Combining current points obtained from the FPL API (https://fantasy.premierleague.com/api/entry/{Team_ID}/history/) and using a Double Exponential Smoothing Model to predict future points, this app is the perfect way for players to visualize their progression over FPL gameweeks. Adding up to two additional Team IDs allows players to see how they stack up against their FPL rivals. 
This project was built using Dash, a framework written on top of Flask, Plotly.js and React.js and is great for creating effective graphs to visualize meaningful data.
import dash
# The Data Process
