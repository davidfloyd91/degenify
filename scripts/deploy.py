from brownie import Degenify, accounts

def main():
    acct = accounts.load('deploy_account')
    acct.deploy(Degenify)

# Transaction sent: 0x20988deeed2ce5fb6fda414d2f986d7c989da87e3f6a17c6045a585ee67d62d3
#   Gas price: 10.000001459 gwei   Gas limit: 1812860   Nonce: 0
#   Degenify.constructor confirmed - Block: 12611149   Gas used: 1648055 (90.91%)
#   Degenify deployed at: 0xcc3eB2EF87B6872b802b58A98BcACe061Fe054dF
