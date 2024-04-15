import yaml
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pprint


CONF = None
with open('conf.yml', 'r') as file:
    CONF = list(yaml.safe_load_all(file))[0]
#print(CONF)

###############################################################################################

t_fields = CONF['TransactionFields']
t_size = t_fields['H4'] + t_fields['S4'] + t_fields['P4'] + t_fields['R4'] + t_fields['E4']

###############################################################################################

tps               = CONF['BlockchainParameters']['TPS']
batch_timeout     = CONF['BlockchainParameters']['BatchTimeout']
max_message_count = CONF['BlockchainParameters']['BatchSize']['MaxMessageCount']

total_transactions = tps * batch_timeout
if total_transactions > max_message_count:
    print('Undefined: total_transactions > max_message_count')
    print('Total_transactions : ', total_transactions)
    exit(0)

###############################################################################################

absolute_max_bytes = CONF['BlockchainParameters']['BatchSize']['AbsoluteMaxBytes']
size_total_transacoes = total_transactions * t_size

if size_total_transacoes > absolute_max_bytes:
    print('Undefined: size_total_transacoes > absolute_max_bytes')
    print('size_total_transacoes : ', size_total_transacoes)
    exit(0)

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

vm_pricing                 = CONF['Cloud']['VirtualMachine']['Pricing']
vm_utilization             = CONF['Cloud']['VirtualMachine']['Utilization']
storage_pricing            = CONF['Cloud']['Storage']['Pricing']
network_throughput_pricing = CONF['Cloud']['NetworkThroughput']['Pricing']
additional = CONF['Cloud']['Additional']

custo_mensal = (vm_utilization  * vm_pricing)      + \
               (blockchain_size_gb * storage_pricing)     + \
               (blockchain_size_gb * network_throughput_pricing ) + additional

custo_total = custo_mensal * 12 * x_period

custo_total_em_milhares = custo_total / 1000

# Informações adicionais
total_blocos = (x_period * 31536000) / batch_timeout
objeto_saida = {
    "Custo mensal = " : custo_mensal,
    "Custo total no período = " : custo_total,
    "Custo total no período em milhares = " : custo_total_em_milhares,
    "Tamanho estimado por transação = ": t_size,
    "Tamanho estimado por bloco em bytes= " : block_size,
    "Total de blocos = " : total_blocos,
    "Tamanho estimado da blockchain no período em GB = " : blockchain_size_gb
}

# pprint.pprint(objeto_saida)
# # Plotando o gráfico

# plt.plot([0, x_period], [0, custo_total], label='Custo Total em Milhares', color='orange', marker='o')
# plt.plot([0, x_period], [0, blockchain_size_gb], label='BlockChain em GB', color='palevioletred', marker='o')


# plt.xlabel('Periodo em anos')
# plt.ylabel('Predição')
# plt.title('Gráfico do Custo em relação a Periodo')
# plt.legend()
# plt.show()