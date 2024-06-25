import dash
from dash import html, dcc, Input, Output
import plotly.graph_objs as go

# Inicializa a aplicação Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Exemplo de Dashboard com Dash"),

    # Botões
    html.Div([
        html.Button('COLETAR', id='botao-coletar', n_clicks=0),
        html.Button('PROCESSAR', id='botao-processar', n_clicks=0),
        html.Button('PAUSAR', id='botao-pausar', n_clicks=0),
    ], style={'padding': '20px', 'textAlign': 'center'}),
    
    # Gráficos de Pizza na mesma linha
    html.Div([
        html.Div([
            html.H2("Gráfico de Pizza"),
            dcc.Graph(
                id='grafico-pizza',
                figure={
                    'data': [
                        go.Pie(
                            labels=['A', 'B', 'C', 'D'],
                            values=[10, 20, 30, 40]
                        )
                    ],
                    'layout': go.Layout(
                        title='Gráfico de Pizza'
                    )
                }
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            html.H2("Gráfico de Rosca"),
            dcc.Graph(
                id='grafico-rosca',
                figure={
                    'data': [
                        go.Pie(
                            labels=['A', 'B', 'C', 'D'],
                            values=[10, 20, 30, 40],
                            hole=0.4  # Define o buraco no centro
                        )
                    ],
                    'layout': go.Layout(
                        title='Gráfico de Rosca'
                    )
                }
            )
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    # Gráfico de Pontos
    html.Div([
        html.H2("Gráfico de Pontos"),
        dcc.Graph(
            id='grafico-pontos',
            figure={
                'data': [
                    go.Scatter(
                        x=[1, 2, 3, 4, 5],
                        y=[10, 11, 12, 13, 14],
                        mode='markers'
                    )
                ],
                'layout': go.Layout(
                    title='Gráfico de Pontos'
                )
            }
        )
    ]),
    
    # Gráfico de Barras
    html.Div([
        html.H2("Gráfico de Barras"),
        dcc.Graph(
            id='grafico-barras',
            figure={
                'data': [
                    go.Bar(
                        x=['A', 'B', 'C', 'D'],
                        y=[10, 20, 30, 40]
                    )
                ],
                'layout': go.Layout(
                    title='Gráfico de Barras'
                )
            }
        )
    ])
])

# Define a callback function for the "COLETAR" button
@app.callback(
    Output('grafico-pizza', 'figure'),
    Input('botao-coletar', 'n_clicks')
)
def update_graph(n_clicks):
    # Logica da função de callback (atualiza o gráfico de pizza como exemplo)
    if n_clicks > 0:
        new_values = [20, 30, 40, 50]  # Exemplo de novos valores
        return {
            'data': [
                go.Pie(
                    labels=['A', 'B', 'C', 'D'],
                    values=new_values
                )
            ],
            'layout': go.Layout(
                title='Gráfico de Pizza Atualizado'
            )
        }
    return {
        'data': [
            go.Pie(
                labels=['A', 'B', 'C', 'D'],
                values=[10, 20, 30, 40]
            )
        ],
        'layout': go.Layout(
            title='Gráfico de Pizza'
        )
    }

# Executa a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
