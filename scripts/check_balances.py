import time
from brownie import Contract

cyan = "\033[36m"
green = "\033[32m"
magenta = "\033[35m"
white = "\033[0m"
yellow = "\033[33m"
bright_blue = "\033[94m"

def main():
    degenify_address = '0x2BCA6A5301B41457B05DDb201A00A68b4Dbc8571'
    degenify = Contract(degenify_address)

    wbtc_address = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    wbtc_contract = Contract(wbtc_address)

    weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

    pslp_eth_wbtc_address = "0xde74b6c547bd574c3527316a2eE30cd8F6041525"
    pslp_eth_wbtc_contract = Contract(pslp_eth_wbtc_address)

    pslp_eth_wbtc_farm_address = "0xD55331E7bCE14709d825557E5Bca75C73ad89bFb"
    pslp_eth_wbtc_farm_contract = Contract(pslp_eth_wbtc_farm_address)

    sushi_factory_address = "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
    sushi_factory_contract = Contract(sushi_factory_address)
    slp_eth_wbtc_address = sushi_factory_contract.getPair(wbtc_address, weth_address)
    slp_eth_wbtc_contract = Contract(slp_eth_wbtc_address)

    eth_balance = degenify.balance()
    wbtc_balance = wbtc_contract.balanceOf(degenify_address)
    slp_eth_wbtc_balance = slp_eth_wbtc_contract.balanceOf(degenify_address)
    pslp_eth_wbtc_balance = pslp_eth_wbtc_contract.balanceOf(degenify_address)
    pslp_eth_wbtc_farm_balance = pslp_eth_wbtc_farm_contract.balanceOf(degenify_address)

    print(f"""
==================================
eth_balance
{cyan}{eth_balance}
{white}==================================
wbtc_balance
{magenta}{wbtc_balance}
{white}==================================
slp_eth_wbtc_balance
{yellow}{slp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_balance
{green}{pslp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_farm_balance
{bright_blue}{pslp_eth_wbtc_farm_balance}
{white}==================================
    """)
