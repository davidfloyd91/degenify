import time
from brownie import Degenify, accounts

def main():
    acct = accounts.load('degenify')
    degenify = Degenify[0]

    degenify.bailOutOfSushiAndPickle(
        0,                      # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        0,                      # uint _percentFromSushi,
        0,                      # uint _percentFromPickleJar,
        100,                    # uint _percentFromPickleFarm
        {'from': acct}
    )
