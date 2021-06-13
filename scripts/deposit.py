import time
from brownie import Contract, accounts

# TODO: fix so that you can use mainnet-fork

eth_decimals = 18
wbtc_decimals = 8

def main():
    acct = accounts.load('degenify')
    degenify_address = '0x2BCA6A5301B41457B05DDb201A00A68b4Dbc8571'
    degenify = Contract(degenify_address)

    wbtc = Contract('0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599')

    eth_balance = acct.balance()
    wbtc_balance = wbtc.balanceOf(acct)

    print(
        "eth_balance", eth_balance,
        "\nwbtc_balance", wbtc_balance
    )

    #################################################
    ########## change these with each call ##########
    #################################################
    eth_deposit_amount = 0
    wbtc_deposit_amount = 0
    amount_eth_min = 0 # idk hopefully it's fine
    deadline = time.time() + 6000000
    percent_to_pickle_jar = 100
    percent_to_pickle_farm = 100
    #################################################
    #################################################
    #################################################

    if eth_balance < eth_deposit_amount or wbtc_balance < wbtc_deposit_amount:
        raise Exception("account has insufficient eth or wbtc")

    if eth_deposit_amount > 0:
        acct.transfer(degenify_address, eth_deposit_amount)
    
    if wbtc_deposit_amount > 0:
        wbtc.approve(degenify_address, wbtc_deposit_amount, {'from': acct})
        wbtc.transfer(degenify_address, wbtc_deposit_amount, {'from': acct})
    
    degenify_eth_balance = degenify.balance()
    degenify_wbtc_balance = wbtc.balanceOf(degenify_address)

    print(
        "degenify_eth_balance", degenify_eth_balance,
        "\ndegenify_wbtc_balance", degenify_wbtc_balance
    )

    if degenify_eth_balance == 0 or degenify_wbtc_balance == 0:
        raise Exception("contract has no eth or no wbtc")

    degenify.apeIntoSushiAndPickle(
        degenify_eth_balance,   # uint _value
        degenify_wbtc_balance,  # uint amountTokenDesired
        degenify_wbtc_balance,  # uint amountTokenMin
        amount_eth_min,         # uint amountETHMin
        deadline,               # uint deadline
        percent_to_pickle_jar,  # uint _percentToPickleJar
        percent_to_pickle_farm, # uint _percentToPickleFarm
        {
            'from': acct
        }
    )
