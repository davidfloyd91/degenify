import time
from brownie import Contract, Degenify, accounts

def main():
    acct = accounts.load('degenify')
    degenify = Degenify[0]

    degenify.bailOutOfSushiAndPickle(
        # don't use zero for amountTokenMin and amountETHMin
        0,                      # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        100,                    # uint _percentFromSushi,
        100,                    # uint _percentFromPickleJar,
        100,                    # uint _percentFromPickleFarm
        {'from': acct}
    )

    eth_balance = degenify.balance()
    degenify.withdrawETH(eth_balance, {'from': acct})
    
    wbtc_address = '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'
    wbtc = Contract(wbtc_address)
    wbtc_balance = wbtc.balanceOf(degenify)
    degenify.withdrawToken(wbtc_balance, wbtc_address, {'from': acct})
