import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import paho.mqtt.client as mqtt
import threading
import time

# Global variable to store incoming data
data = {
    'Normal': [],
    'Horizontal_Mis_2mm': [],
    'Vertical_Mis_127mm': []
}

# MQTT client setup
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("test/topic1")

def on_message(client, userdata, msg):
    global data
    label = msg.payload.decode()
    if label in data:
        data[label].append(1)
        for other_label in data:
            if other_label != label:
                data[other_label].append(0)
        # Limit the length of the data for visualization purposes
        for key in data:
            if len(data[key]) > 100:
                data[key] = data[key][-100:]

client = mqtt.Client(client_id="Subscriber")
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost")

# Start MQTT client in a separate thread
thread = threading.Thread(target=client.loop_forever)
thread.start()

# Dash app setup
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Real-time Label Timeline'),
    dcc.Graph(id='label-timeline'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('label-timeline', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    global data
    time_points = list(range(len(data['Normal'])))
    figure = {
        'data': [
            go.Scatter(
                x=time_points,
                y=data[label],
                mode='lines+markers',
                name=label
            ) for label in data
        ],
        'layout': go.Layout(
            title='Label Timeline',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Value'},
            height=600
        )
    }
    return figure

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
