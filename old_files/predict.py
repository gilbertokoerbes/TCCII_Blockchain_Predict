import yaml
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pprint

CONF = None
class blockchain_predict:
    
    def load_config(self):
        global CONF
        if CONF == None:
            with open('conf.yml', 'r') as file:
                CONF = list(yaml.safe_load_all(file))[0]
        
    def __init__(self):
        self.load_config()
        global CONF
        self.transation_fields           = CONF['TransactionFields']
        self.tps                         = CONF['BlockchainParameters']['TPS']
        self.batch_timeout               = CONF['BlockchainParameters']['BatchTimeout']
        self.max_message_count           = CONF['BlockchainParameters']['BatchSize']['MaxMessageCount']
        self.absolute_max_bytes          = CONF['BlockchainParameters']['BatchSize']['AbsoluteMaxBytes']
        self.block_header_size           = CONF['BlockchainParameters']['Block']['HeaderSize']
        self.block_metadata_size         = CONF['BlockchainParameters']['Block']['MetadataSize']
        self.x_period                    = CONF['Predict']
        self.genesis_block_size          = CONF['BlockchainParameters']['GenesisBlockSize']

        self.transation_size = self.calculate_transaction_size(self.transation_fields)
        self.total_transactions = self.calculate_total_transactions(self.tps,  self.batch_timeout)
        self.size_total_transacoes = self.calculate_size_total_transacoes(self.total_transactions, self.transation_size)
        self.block_size = self.calculate_block_size(self.block_header_size , self.block_metadata_size , self.size_total_transacoes)
        self.blockchain_size_gb = self.calculate_blockchain_size(self.x_period, self.batch_timeout, self.block_size, self.genesis_block_size)
        self.total_blocks = self.calculate_total_blocks(self.x_period, self.batch_timeout)



    def calculate_transaction_size(self, transation_fields: list) -> int:
        self.transation_size = transation_fields['H4'] + transation_fields['S4'] + transation_fields['P4'] + transation_fields['R4'] + transation_fields['E4']
        return self.transation_size
    

    def calculate_total_transactions(self, tps: int, batch_timeout: int) -> int:
        self.total_transactions = tps * batch_timeout
        if self.total_transactions > self.max_message_count:
            print('Undefined: total_transactions > max_message_count')
            print('Total_transactions : ', self.total_transactions)
            return -1        
        return self.total_transactions


    def calculate_size_total_transacoes(self, total_transactions:int, transation_size:int) -> int:
        self.size_total_transacoes = total_transactions * transation_size
        if self.size_total_transacoes > self.absolute_max_bytes:
            print('Undefined: size_total_transacoes > absolute_max_bytes')
            print('size_total_transacoes : ', self.size_total_transacoes)
            return -1
        return self.size_total_transacoes


    def calculate_block_size(self, block_header_size: int, block_metadata_size: int, size_total_transacoes: int) -> int:
        self.block_size = block_header_size + block_metadata_size + size_total_transacoes
        return self.block_size


    def calculate_blockchain_size(self, x_period, batch_timeout, block_size, genesis_block_size):
        blockchain_size = ((x_period * 31536000) / batch_timeout) * block_size + genesis_block_size
        self.blockchain_size_gb = blockchain_size / (1024 ** 3)
        return self.blockchain_size_gb

    def calculate_total_blocks(self, x_period, batch_timeout):
        # Informações adicionais
        self.total_blocks = (x_period * 31536000) / batch_timeout
        return self.total_blocks
    def calculate_block_headers_size(self) -> int:
        return self.block_header_size + self.block_metadata_size

class CostPredict:
    def load_config(self):
        global CONF
        if CONF == None:
            with open('conf.yml', 'r') as file:
                CONF = list(yaml.safe_load_all(file))[0]
        
    def __init__(self, blockchain_size_gb = 0):
        self.load_config()
        self.vm_pricing_hours            = CONF['Cloud']['VirtualMachine']['Pricing']
        self.vm_vcpu                     = CONF['Cloud']['VirtualMachine']['VCPU']
        self.storage_pricing             = CONF['Cloud']['Storage']['Pricing']
        self.network_throughput_pricing  = CONF['Cloud']['NetworkThroughput']['Pricing']
        self.additional                  = CONF['Cloud']['Additional']

    #     self.custo_mensal = self.total_cost_month(self.vm_utilization, self.vm_pricing_hours, self.storage_pricing, self.network_throughput_pricing, self.additional, blockchain_size_gb)

    # def total_cost_month(self, vm_utilization, vm_pricing_hours, storage_pricing, network_throughput_pricing, additional, blockchain_size_gb):
    #     self.custo_mensal = (vm_utilization  * vm_pricing_hours)      + \
    #                 (blockchain_size_gb * storage_pricing)     + \
    #                 (blockchain_size_gb * network_throughput_pricing ) + additional
    #     return self.custo_mensal

class StorageDemand:
    def __init__(self):
        self.total_blocks = 0
        self.total_transactions = 0
        self.calculated_total_size_blocks = 0
        self.batch_type = ""
        self.period = 0



if __name__ == '__main__':
    blockchain = blockchain_predict()
    cost = CostPredict(blockchain.blockchain_size_gb)
    
    objeto_saida = {
        "Custo mensal = " : cost.custo_mensal,
        "Tamanho estimado da blockchain no período em GB = " : blockchain.blockchain_size_gb
    }
    for x in range(0,blockchain.x_period):
        print(x, blockchain.batch_timeout, blockchain.block_size, blockchain.genesis_block_size)
        print(blockchain.calculate_blockchain_size(x, blockchain.batch_timeout, blockchain.block_size, blockchain.genesis_block_size))
    pprint.pprint(objeto_saida)
