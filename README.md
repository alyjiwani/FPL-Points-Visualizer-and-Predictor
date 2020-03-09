# FPL Points Visualizer and Predictor
This web app is a point visualizer for the 2019-2020 Fantasy Premier League season. Combining current points obtained from the FPL API (https://fantasy.premierleague.com/api/entry/{Team_ID}/history/) and using a Double Exponential Smoothing Model to predict future points, this app is the perfect way for players to visualize their progression over FPL gameweeks. Adding up to two additional Team IDs allows players to see how they stack up against their FPL rivals. \
This project was written in Python and HTML/CSS and was built using Dash, a framework written on top of Flask, Plotly.js and React.js. Dash is great for creating effective graphs to visualize meaningful data.
``` python
import dash
```
# How to Use It?
https://fpl-visualizer.herokuapp.com/ \
Start by entering your Team ID which can be found when viewing your team from the FPL application on your desktop.
![Link](/images/link.png)
Clicking "Generate" will populate the graph with a line illustrating your current and predicted points cumulative points.
![Example](/images/example.png)
# The Data Process - Why Double Exponential Smoothing?
In this section, I want to dive more deeply into the model chosen for the prediction aspect of this web app and provide some reasoning as to why it was chosen. 
``` python
model = statsmodels.tsa.holtwinters.ExponentialSmoothing(current_points, 'add', False, None)
```
The FPL data we are considering is an example of a time series. This form of data naturally lends itself to a variety of time series analyses and forecasting. 
