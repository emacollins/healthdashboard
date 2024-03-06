# Import necessary libraries
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Initialize your Dash app
app = dash.Dash(__name__)

df = pd.read_csv("test.csv")

# Creating a simple line chart as an example
fig = px.line(df, x="creationDate", y="value", title="Daily Steps")

# Define your Dash app layout
app.layout = html.Div(children=[
    html.H1(children='Health Dashboard'),
    
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    # Example graph
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
