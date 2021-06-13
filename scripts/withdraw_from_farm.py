import time
from brownie import Contract, accounts

def main():
    acct = accounts.load('degenify')
    degenify_address = '0x2BCA6A5301B41457B05DDb201A00A68b4Dbc8571'
    degenify = Contract(degenify_address)

    degenify.bailOutOfSushiAndPickle(
        0,                      # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        0,                      # uint _percentFromSushi,
        0,                      # uint _percentFromPickleJar,
        100,                    # uint _percentFromPickleFarm
        {'from': acct}
    )
