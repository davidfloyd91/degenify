from brownie import Degenify, accounts

def main():
    acct = accounts.load('degenify')
    acct.deploy(Degenify)

# v2

# Transaction sent: 0x64bccc401de3e9a295bafea792724f2f0ccff51942e3c3020cbac37b9f8b30f1
#   Gas price: 10.0 gwei   Gas limit: 1855620   Nonce: 10
#   Degenify.constructor confirmed - Block: 12622349   Gas used: 1686928 (90.91%)
#   Degenify deployed at: 0x2BCA6A5301B41457B05DDb201A00A68b4Dbc8571

# v1

# Transaction sent: 0x20988deeed2ce5fb6fda414d2f986d7c989da87e3f6a17c6045a585ee67d62d3
#   Gas price: 10.000001459 gwei   Gas limit: 1812860   Nonce: 0
#   Degenify.constructor confirmed - Block: 12611149   Gas used: 1648055 (90.91%)
#   Degenify deployed at: 0xcc3eB2EF87B6872b802b58A98BcACe061Fe054dF
