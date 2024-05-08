from web3 import Web3


def get_w3_binance_mainnet():
    return Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))


def get_w3_ethereum_mainnet():
    return Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))


def get_w3_espento_mainnet():
    return Web3(Web3.HTTPProvider('https://rpc.escscan.com'))


def get_w3_binance_testnet():
    return Web3(Web3.HTTPProvider('https://bsc-testnet-rpc.publicnode.com'))


def get_w3_ethereum_testnet():
    return Web3(Web3.HTTPProvider('https://ethereum-sepolia.rpc.subquery.network/public'))


def get_w3_espento_testnet():
    return Web3(Web3.HTTPProvider('https://rpc-testnet.escscan.com'))
