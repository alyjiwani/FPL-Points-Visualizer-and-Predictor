# FPL Points Visualizer and Predictor
This web app is a point visualizer for the 2019-2020 Fantasy Premier League season. Combining current points obtained from the FPL API (https://fantasy.premierleague.com/api/entry/{Team_ID}/history/) and using a Double Exponential Smoothing Model to predict future points, this app is the perfect way for players to visualize their progression over FPL gameweeks. Adding up to two additional Team IDs allows players to see how they stack up against their FPL rivals as well. \
This project was written in Python and HTML/CSS and was built using Dash, a framework written on top of Flask, Plotly.js and React.js. Dash is great for creating effective graphs to visualize meaningful data.
``` python
import dash
```
# How to Use It?
https://fpl-visualizer.herokuapp.com/ \
Start by entering your Team ID which can be found when viewing your team from the FPL application on your desktop. \
![Link](/images/link.png)
Clicking "Generate" will populate the graph with a line illustrating your current and predicted points cumulative points. \
![Example](/images/example.png)
# The Data Process - Why Double Exponential Smoothing?
In this section, I want to dive into the model chosen for the prediction aspect of this web app and provide some reasoning as to why it was chosen. 
``` python
model = statsmodels.tsa.holtwinters.ExponentialSmoothing(current_points, 'add', False, None)
```
The FPL data we are considering is an example of a time series. This form of data naturally lends itself to a variety of time series analyses and forecasting. Because the data being plotted is cumulative, it displays a general upward trend and thus is best modelled using Double Exponential Smoothing. This model (along with other exponential smoothing models) builds on the idea of assigning weights (or factors) to more recent data in a time series while older data is considered less. The amount of weight being placed on recent data depends on the value of α (0 < α < 1). Double Exponential Smoothing not only places weight on the level (ie. the point values) but also a weight on the overall trend (linear or exponential) known as β. \
Because fantasy football is a dynamic game, making changes to your team is essential for success. A team with players who were in form five gameweeks ago may be rendered useless in the upcoming gameweeks as a result of injuries, fixtures, blank gameweeks etc. The Double Exponential Smoothing model allows for a α and β value to be chosen when fitting the data, allowing for recent gameweek results or overall trends to have a larger factor on final score. Essentially, this makes sure that users who performed extremely well in early gameweeks (and have not adapted to the new best players) are not predicted an inflated final score (as may be done with models such as a linear regression).
