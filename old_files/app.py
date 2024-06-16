from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import yaml
import predict


app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

blockchain = predict.blockchain_predict()
cost = predict.cost_predict(blockchain.blockchain_size_gb)


t_fields_config = blockchain.transaction_fields


t_fields_hmtl = []
for field, value in t_fields_config.items():
    input_field = dcc.Input(id=field, value=value, type='number', style={'width': '50%'})
    t_fields_hmtl.append(html.Div([field, input_field], style={'width': '8%','display': 'inline-block', 'margin-right': '0px'}))  # Use CSS para exibir os campos lado a lado


#print(t_fields_hmtl)

x_period = np.arange(blockchain.x_period)
y_predict = []
for x in x_period:
    print(x, blockchain.batch_timeout, blockchain.block_size, blockchain.genesis_block_size)
    y_predict.append(blockchain.calculate_blockchain_size(x, blockchain.batch_timeout, blockchain.block_size, blockchain.genesis_block_size))
print(x_period)
print(y_predict)

fig = go.Figure(data=go.Scatter(x=x_period, y=y_predict))

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div([

    html.H2('Blochain Predict'),
    html.H2('Values for Transaction Fields #Bytes'),
    html.Div(t_fields_hmtl,
            style={}), #'border-style': 'dotted dashed solid double'
    html.Br(),
    html.Div([

        html.Div(["TPS", 
                  dcc.Input(id="tps", value=blockchain.tps, type='number', 
                                style={'width': '50%', 'margin-left': '1%'})],                                
                    style={'width': '8%','display': 'inline-block', 'margin-right': '0px'}),

        html.Div(["BatchTimeout (s)", 
                dcc.Input(id="batch_timeout", value=blockchain.batch_timeout, type='number', 
                                style={'width': '40%', 'margin-left': '1%'})],
                    style={'width': '20%','display': 'inline-block', 'margin-right': '0px'}),
            
        html.Div(["BatchSize:MaxMessageCount", 
                dcc.Input(id="max_message_count", value=blockchain.max_message_count, type='number', 
                                style={'width': '40%', 'margin-left': '1%'})],
                    style={'width': '35%','display': 'inline-block', 'margin-right': '0px'})

    ],
    style={}), #'border-style': 'dotted dashed solid double'
    html.Br(),
    html.Div([

        html.Div(["Period", 
                  dcc.Input(id="period", value=blockchain.x_period, type='number', 
                                style={'width': '50%', 'margin-left': '1%'})],                                
                    style={'width': '8%','display': 'inline-block', 'margin-right': '0px'}),
    ],
    style={}),
    html.Br(),
    html.Br(),

    dcc.Input(id="input-1", type="text", value="Montréal"),
    dcc.Input(id="input-2", type="text", value="Canada"),
    dcc.Graph(id="graph", figure=fig),
    dcc.Checklist(
        id="checklist",
        options=["Asia", "Europe", "Africa","Americas","Oceania"],
        value=["Americas", "Oceania"],
        inline=True
    ),
])

if __name__ == '__main__':

    app.run(debug=True)
