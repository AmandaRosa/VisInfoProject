import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Sample data preparation
time_points = pd.date_range(start='2023-01-01', periods=100, freq='D')
data = {
    'time': time_points,
    'normal': [1 if i % 7 == 0 else 0 for i in range(100)],
    'fault1': [1 if i % 8 == 0 else 0 for i in range(100)],
    'fault2': [1 if i % 9 == 0 else 0 for i in range(100)],
    'fault3': [1 if i % 10 == 0 else 0 for i in range(100)],
    'fault4': [1 if i % 11 == 0 else 0 for i in range(100)],
    'fault5': [1 if i % 12 == 0 else 0 for i in range(100)]
}

df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Label Timeline'),
    dcc.Graph(
        id='label-timeline',
        figure={
            'data': [
                go.Scatter(
                    x=df['time'],
                    y=df[label],
                    mode='lines+markers',
                    name=label
                ) for label in ['normal', 'fault1', 'fault2', 'fault3', 'fault4', 'fault5']
            ],
            'layout': go.Layout(
                title='Label Timeline',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Value'},
                height=600
            )
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
