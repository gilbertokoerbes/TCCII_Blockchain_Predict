from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import yaml


# # Plotando o gráfico

# plt.plot([0, x_period], [0, custo_total], label='Custo Total em Milhares', color='orange', marker='o')
# plt.plot([0, x_period], [0, blockchain_size_gb], label='BlockChain em GB', color='palevioletred', marker='o')


# plt.xlabel('Periodo em anos')
# plt.ylabel('Predição')
# plt.title('Gráfico do Custo em relação a Periodo')
# plt.legend()
# plt.show()

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.




app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Period": [x_period],
#     "Cost": [custo_total],
#     #"City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.line(df, x="Period", y="Cost"  )#color="City" barmode="group"

CONF = None
with open('conf.yml', 'r') as file:
    CONF = list(yaml.safe_load_all(file))[0]
#print(CONF)

###############################################################################################

t_fields_config = CONF['TransactionFields']
t_size = t_fields_config['H4'] + t_fields_config['S4'] + t_fields_config['P4'] + t_fields_config['R4'] + t_fields_config['E4']

t_fields_hmtl = []
for field, value in t_fields_config.items():
    input_field = dcc.Input(id=field, value=value, type='number', style={'width': '50%'})
    t_fields_hmtl.append(html.Div([field, input_field], style={'width': '8%','display': 'inline-block', 'margin-right': '0px'}))  # Use CSS para exibir os campos lado a lado

tps               = CONF['BlockchainParameters']['TPS']
batch_timeout     = CONF['BlockchainParameters']['BatchTimeout']
max_message_count = CONF['BlockchainParameters']['BatchSize']['MaxMessageCount']

total_transactions = tps * batch_timeout
if total_transactions > max_message_count:
    print('Undefined: total_transactions > max_message_count')
    print('Total_transactions : ', total_transactions)
   

###############################################################################################

absolute_max_bytes = CONF['BlockchainParameters']['BatchSize']['AbsoluteMaxBytes']
size_total_transacoes = total_transactions * t_size

if size_total_transacoes > absolute_max_bytes:
    print('Undefined: size_total_transacoes > absolute_max_bytes')
    print('size_total_transacoes : ', size_total_transacoes)
    
###############################################################################################

block_header_size   = CONF['BlockchainParameters']['Block']['HeaderSize']
block_metadata_size = CONF['BlockchainParameters']['Block']['MetadataSize']

block_size = block_header_size + block_metadata_size + size_total_transacoes

###############################################################################################

x_period = CONF['Predict']
genesis_block_size =  CONF['BlockchainParameters']['GenesisBlockSize']

blockchain_size = ((x_period * 31536000) / batch_timeout) * block_size + genesis_block_size

blockchain_size_gb = blockchain_size / (1024 ** 3)
###############################################################################################

print(t_fields_hmtl)

x = np.arange(10)

fig = go.Figure(data=go.Scatter(x=x, y=x**2))

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
                  dcc.Input(id="tps", value=tps, type='number', 
                                style={'width': '50%', 'margin-left': '1%'})],                                
                    style={'width': '8%','display': 'inline-block', 'margin-right': '0px'}),

        html.Div(["BatchTimeout (s)", 
                dcc.Input(id="batch_timeout", value=batch_timeout, type='number', 
                                style={'width': '40%', 'margin-left': '1%'})],
                    style={'width': '20%','display': 'inline-block', 'margin-right': '0px'}),
            
        html.Div(["BatchSize:MaxMessageCount", 
                dcc.Input(id="max_message_count", value=max_message_count, type='number', 
                                style={'width': '40%', 'margin-left': '1%'})],
                    style={'width': '35%','display': 'inline-block', 'margin-right': '0px'})

    ],
    style={}), #'border-style': 'dotted dashed solid double'
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
