import time
from brownie import chain, reverts

# brownie test --interactive -s -v

# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
cyan = "\033[36m"
green = "\033[32m"
magenta = "\033[35m"
white = "\033[0m"
yellow = "\033[33m"

def test_update_owner(
    degenify_contract,
    owner,
    puppet,
    very_bad_man
):
    assert degenify_contract.owner() == owner, "failed to set owner"
    with reverts():
        degenify_contract.updateOwner(very_bad_man, {'from': very_bad_man})
    degenify_contract.updateOwner(puppet, {'from': owner})
    assert degenify_contract.owner() == puppet, "failed to update owner"
    with reverts():
        degenify_contract.updateOwner(owner, {'from': owner})
    degenify_contract.updateOwner(owner, {'from': puppet})
    assert degenify_contract.owner() == owner, "failed to re-update owner"

def test_receive_and_witdraw_ether(
    degenify_contract,
    owner,
    very_bad_man,
    whale
):
    receive_amount = 1_000_000 * 10 ** 18
    degenify_contract_balance_before = degenify_contract.balance()
    whale.transfer(degenify_contract, receive_amount)
    degenify_contract_balance_after = degenify_contract.balance()
    assert degenify_contract_balance_after - degenify_contract_balance_before == receive_amount, "failed to receive ether"
    with reverts():
        degenify_contract.withdrawETH(receive_amount, {'from': very_bad_man})
    owner_balance_before = owner.balance()
    degenify_contract.withdrawETH(receive_amount, {'from': owner})
    owner_balance_after = owner.balance()
    assert owner_balance_after - owner_balance_before == receive_amount, "failed to withdraw ether"

def test_receive_and_withdraw_tokens(
    degenify_contract,
    owner,
    wbtc_address,
    wbtc_contract,
    wbtc_whale,
    very_bad_man
):
    receive_amount = 1_000 * 10 ** 8
    degenify_contract_balance_before = wbtc_contract.balanceOf(degenify_contract)
    wbtc_contract.transfer(degenify_contract, receive_amount, {'from': wbtc_whale})
    degenify_contract_balance_after = wbtc_contract.balanceOf(degenify_contract)
    assert degenify_contract_balance_after - degenify_contract_balance_before == receive_amount, "failed to receive tokens"
    with reverts():
        degenify_contract.withdrawToken(receive_amount, wbtc_address, {'from': very_bad_man})
    owner_balance_before = wbtc_contract.balanceOf(owner)
    degenify_contract.withdrawToken(receive_amount, wbtc_address, {'from': owner})
    owner_balance_after = wbtc_contract.balanceOf(owner)
    assert owner_balance_after - owner_balance_before == receive_amount, "failed to withdraw tokens"

def test_stake_in_sushi_only(
    degenify_contract,
    owner,
    slp_eth_wbtc_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 500 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        0,                      # uint _percentToPickleJar,
        0,                      # uint _percentToPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    print(f"""
==================================
slp_eth_wbtc_balance
{cyan}{slp_eth_wbtc_balance}
{white}==================================
    """)
    assert slp_eth_wbtc_balance > 0, "didn't receive positive sushi liquidity token balance"

def test_stake_in_sushi_and_pickle_some_in_jar(
    degenify_contract,
    owner,
    slp_eth_wbtc_contract,
    pslp_eth_wbtc_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 500 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        50,                     # uint _percentToPickleJar,
        0,                      # uint _percentToPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_balance = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    print(f"""
==================================
slp_eth_wbtc_balance
{cyan}{slp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_balance
{magenta}{pslp_eth_wbtc_balance}
{white}==================================
    """)
    assert pslp_eth_wbtc_balance > 0, "didn't receive positive pickle jar token balance"
    assert slp_eth_wbtc_balance > 0, "didn't receive zero sushi liquidity token balance"

def test_stake_in_sushi_and_pickle_all_in_jar(
    degenify_contract,
    owner,
    slp_eth_wbtc_contract,
    pslp_eth_wbtc_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 500 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        100,                    # uint _percentToPickleJar,
        0,                      # uint _percentToPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_balance = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    print(f"""
==================================
slp_eth_wbtc_balance
{cyan}{slp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_balance
{magenta}{pslp_eth_wbtc_balance}
{white}==================================
    """)
    assert pslp_eth_wbtc_balance > 0, "didn't receive positive pickle jar token balance"
    assert slp_eth_wbtc_balance == 0, "didn't receive zero sushi liquidity token balance"

def test_stake_in_sushi_and_pickle_farm_some(
    degenify_contract,
    owner,
    slp_eth_wbtc_contract,
    pslp_eth_wbtc_contract,
    pslp_eth_wbtc_farm_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 500 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        100,                    # uint _percentToPickleJar,
        50,                     # uint _percentToPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_balance = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_farm_balance = pslp_eth_wbtc_farm_contract.balanceOf(degenify_contract)
    print(f"""
==================================
slp_eth_wbtc_balance
{cyan}{slp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_balance
{magenta}{pslp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_farm_balance
{yellow}{pslp_eth_wbtc_farm_balance}
{white}==================================
    """)
    assert pslp_eth_wbtc_farm_balance > 0, "didn't receive positive pickle farm token balance"    
    assert pslp_eth_wbtc_balance > 0, "didn't receive positive pickle jar token balance"
    assert slp_eth_wbtc_balance == 0, "didn't receive zero sushi liquidity token balance"

def test_stake_in_sushi_and_pickle_farm_all(
    degenify_contract,
    owner,
    slp_eth_wbtc_contract,
    pslp_eth_wbtc_contract,
    pslp_eth_wbtc_farm_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 500 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        100,                    # uint _percentToPickleJar,
        100,                    # uint _percentToPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_balance = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_farm_balance = pslp_eth_wbtc_farm_contract.balanceOf(degenify_contract)
    print(f"""
==================================
slp_eth_wbtc_balance
{cyan}{slp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_balance
{magenta}{pslp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_farm_balance
{yellow}{pslp_eth_wbtc_farm_balance}
{white}==================================
    """)
    assert pslp_eth_wbtc_farm_balance > 0, "didn't receive positive pickle farm token balance"    
    assert pslp_eth_wbtc_balance == 0, "didn't receive zero pickle jar token balance"
    assert slp_eth_wbtc_balance == 0, "didn't receive zero sushi liquidity token balance"

def test_stake_in_sushi_then_pickle_later(
    degenify_contract,
    owner,
    slp_eth_wbtc_contract,
    pslp_eth_wbtc_contract,
    pslp_eth_wbtc_farm_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 500 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        0,                      # uint _percentToPickleJar,
        0,                      # uint _percentToPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_balance = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_farm_balance = pslp_eth_wbtc_farm_contract.balanceOf(degenify_contract)
    print(f"""
==================================
slp_eth_wbtc_balance
{cyan}{slp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_balance
{magenta}{pslp_eth_wbtc_balance}
{white}==================================
pslp_eth_wbtc_farm_balance
{yellow}{pslp_eth_wbtc_farm_balance}
{white}==================================
    """)
    assert pslp_eth_wbtc_farm_balance == 0, "didn't receive zero pickle farm token balance"    
    assert pslp_eth_wbtc_balance == 0, "didn't receive zero pickle jar token balance"
    assert slp_eth_wbtc_balance > 0, "didn't receive positive sushi liquidity token balance"
    degenify_contract.apeIntoSushiAndPickle(
        0,                      # uint _value
        0,                      # uint amountTokenDesired,
        0,                      # uint amountTokenMin,
        0,                      # uint amountETHMin,
        0,                      # uint deadline,
        95,                     # uint _percentToPickleJar,
        0,                      # uint _percentToPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance_now = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_balance_now = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_farm_balance_now = pslp_eth_wbtc_farm_contract.balanceOf(degenify_contract)
    print(f"""
==================================
slp_eth_wbtc_balance_now
{cyan}{slp_eth_wbtc_balance_now}
{white}==================================
pslp_eth_wbtc_balance_now
{magenta}{pslp_eth_wbtc_balance_now}
{white}==================================
pslp_eth_wbtc_farm_balance_now
{yellow}{pslp_eth_wbtc_farm_balance_now}
{white}==================================
    """)
    assert pslp_eth_wbtc_farm_balance_now == 0, "didn't receive zero pickle farm token balance"    
    assert pslp_eth_wbtc_balance_now > 0, "didn't receive positive pickle jar token balance"
    assert slp_eth_wbtc_balance_now > 0, "didn't receive positive sushi liquidity token balance"
    degenify_contract.apeIntoSushiAndPickle(
        0,                      # uint _value
        0,                      # uint amountTokenDesired,
        0,                      # uint amountTokenMin,
        0,                      # uint amountETHMin,
        0,                      # uint deadline,
        100,                    # uint _percentToPickleJar,
        100,                    # uint _percentToPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance_now_now = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_balance_now_now = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_farm_balance_now_now = pslp_eth_wbtc_farm_contract.balanceOf(degenify_contract)
    print(f"""
==================================
slp_eth_wbtc_balance_now_now
{cyan}{slp_eth_wbtc_balance_now_now}
{white}==================================
pslp_eth_wbtc_balance_now_now
{magenta}{pslp_eth_wbtc_balance_now_now}
{white}==================================
pslp_eth_wbtc_farm_balance_now_now
{yellow}{pslp_eth_wbtc_farm_balance_now_now}
{white}==================================
    """)
    assert pslp_eth_wbtc_farm_balance_now_now > 0, "didn't receive positive pickle farm token balance"    
    assert pslp_eth_wbtc_balance_now_now == 0, "didn't receive zero pickle jar token balance"
    assert slp_eth_wbtc_balance_now_now == 0, "didn't receive zero sushi liquidity token balance"

def test_remove_some_from_sushi(
    degenify_contract,
    owner,
    slp_eth_wbtc_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 5 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        0,                      # uint _percentToPickleJar,
        0,                      # uint _percentToPickleFarm
        {'from': owner}
    )
    eth_balance_before = degenify_contract.balance()
    wbtc_balance_before = wbtc_contract.balanceOf(degenify_contract)
    slp_eth_wbtc_balance_before = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    degenify_contract.bailOutOfSushiAndPickle(
        0,                      # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        50,                     # uint _percentFromSushi,
        0,                      # uint _percentFromPickleJar,
        0,                      # uint _percentFromPickleFarm
        {'from': owner}
    )
    eth_balance_after = degenify_contract.balance()
    wbtc_balance_after = wbtc_contract.balanceOf(degenify_contract)
    slp_eth_wbtc_balance_after = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    print(f"""
==================================
eth_balance_before
{eth_balance_before}
==================================
eth_balance_after
{eth_balance_after}
==================================
wbtc_balance_before
{wbtc_balance_before}
==================================
wbtc_balance_after
{wbtc_balance_after}
==================================
slp_eth_wbtc_balance_before
{cyan}{slp_eth_wbtc_balance_before}
{white}==================================
slp_eth_wbtc_balance_after
{cyan}{slp_eth_wbtc_balance_after}
{white}==================================
    """)
    assert eth_balance_after > eth_balance_before, "didn't increase eth balance"
    assert wbtc_balance_after > wbtc_balance_before, "didn't increase wbtc balance"
    assert slp_eth_wbtc_balance_after < slp_eth_wbtc_balance_before, "didn't reduce sushi liquidity token balance"

def test_remove_some_from_pickle_jar(
    degenify_contract,
    owner,
    pslp_eth_wbtc_contract,
    slp_eth_wbtc_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 5 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        100,                    # uint _percentToPickleJar,
        0,                      # uint _percentToPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance_before = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_balance_before = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    degenify_contract.bailOutOfSushiAndPickle(
        0,                      # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        0,                      # uint _percentFromSushi,
        50,                     # uint _percentFromPickleJar,
        0,                      # uint _percentFromPickleFarm
        {'from': owner}
    )
    slp_eth_wbtc_balance_after = slp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_balance_after = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    print(f"""
==================================
slp_eth_wbtc_balance_before
{cyan}{slp_eth_wbtc_balance_before}
{white}==================================
slp_eth_wbtc_balance_after
{cyan}{slp_eth_wbtc_balance_after}
{white}==================================
pslp_eth_wbtc_balance_before
{magenta}{pslp_eth_wbtc_balance_before}
{white}==================================
pslp_eth_wbtc_balance_after
{magenta}{pslp_eth_wbtc_balance_after}
{white}==================================
    """)
    assert slp_eth_wbtc_balance_after > slp_eth_wbtc_balance_before, "didn't increase sushi liquidity token balance"
    assert pslp_eth_wbtc_balance_after < pslp_eth_wbtc_balance_before, "didn't reduce pickle jar token balance"

def test_remove_some_from_pickle_farm(
    degenify_contract,
    owner,
    pslp_eth_wbtc_contract,
    pslp_eth_wbtc_farm_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 5 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        100,                    # uint _percentToPickleJar,
        100,                    # uint _percentToPickleFarm
        {'from': owner}
    )
    pslp_eth_wbtc_balance_before = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_farm_balance_before = pslp_eth_wbtc_farm_contract.balanceOf(degenify_contract)
    degenify_contract.bailOutOfSushiAndPickle(
        0,                      # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        0,                      # uint _percentFromSushi,
        0,                      # uint _percentFromPickleJar,
        50,                     # uint _percentFromPickleFarm
        {'from': owner}
    )
    pslp_eth_wbtc_balance_after = pslp_eth_wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_farm_balance_after = pslp_eth_wbtc_farm_contract.balanceOf(degenify_contract)
    print(f"""
==================================
pslp_eth_wbtc_balance_before
{cyan}{pslp_eth_wbtc_balance_before}
{white}==================================
pslp_eth_wbtc_balance_after
{cyan}{pslp_eth_wbtc_balance_after}
{white}==================================
pslp_eth_wbtc_farm_balance_before
{magenta}{pslp_eth_wbtc_farm_balance_before}
{white}==================================
pslp_eth_wbtc_farm_balance_after
{magenta}{pslp_eth_wbtc_farm_balance_after}
{white}==================================
    """)
    assert pslp_eth_wbtc_balance_after > pslp_eth_wbtc_balance_before, "didn't increase sushi liquidity token balance"
    assert pslp_eth_wbtc_farm_balance_after < pslp_eth_wbtc_farm_balance_before, "didn't reduce pickle farm token balance"

def test_full_circle(
    degenify_contract,
    owner,
    pslp_eth_wbtc_farm_contract,
    wbtc_address,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 500 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        100,                    # uint _percentToPickleJar,
        100,                    # uint _percentToPickleFarm
        {'from': owner}
    )
    pslp_eth_wbtc_farm_balance_before = pslp_eth_wbtc_farm_contract.balanceOf(degenify_contract)
    assert pslp_eth_wbtc_farm_balance_before > 0, "didn't receive positive pickle farm token balance"
    eth_balance_before = degenify_contract.balance()
    wbtc_balance_before = wbtc_contract.balanceOf(degenify_contract)
    degenify_contract.bailOutOfSushiAndPickle(
        0,                      # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        100,                    # uint _percentFromSushi,
        100,                    # uint _percentFromPickleJar,
        100,                    # uint _percentFromPickleFarm
        {'from': owner}
    )
    eth_balance_after = degenify_contract.balance()
    wbtc_balance_after = wbtc_contract.balanceOf(degenify_contract)
    pslp_eth_wbtc_farm_balance_after = pslp_eth_wbtc_farm_contract.balanceOf(degenify_contract)
    print(f"""
==================================
eth_balance_before
{eth_balance_before}
==================================
eth_balance_after
{eth_balance_after}
==================================
wbtc_balance_before
{wbtc_balance_before}
==================================
wbtc_balance_after
{wbtc_balance_after}
==================================
pslp_eth_wbtc_farm_balance_before
{yellow}{pslp_eth_wbtc_farm_balance_before}
{white}==================================
pslp_eth_wbtc_farm_balance_after
{yellow}{pslp_eth_wbtc_farm_balance_after}
{white}==================================
    """)
    assert pslp_eth_wbtc_farm_balance_after == 0, "didn't receive zero pickle farm token balance"
    assert eth_balance_after > eth_balance_before, "didn't increase eth balance"
    assert wbtc_balance_after > wbtc_balance_before, "didn't increase wbtc balance"
    owner_eth_balance_before = owner.balance()
    degenify_contract.withdrawETH(eth_balance_after, {'from': owner})
    owner_eth_balance_after = owner.balance()
    degenify_contract_eth_balance_after = degenify_contract.balance()
    assert owner_eth_balance_after - owner_eth_balance_before > 0, "failed to withdraw eth (owner balance)"
    assert degenify_contract_eth_balance_after == 0, "failed to withdraw eth (contract balance)"
    owner_wbtc_balance_before = wbtc_contract.balanceOf(owner)
    degenify_contract.withdrawToken(wbtc_balance_after, wbtc_address, {'from': owner})
    owner_wbtc_balance_after = wbtc_contract.balanceOf(owner)
    degenify_contract_wbtc_balance_after = wbtc_contract.balanceOf(degenify_contract)
    assert owner_wbtc_balance_after - owner_wbtc_balance_before > 0, "failed to withdraw wbtc (owner balance)"
    assert degenify_contract_wbtc_balance_after == 0, "failed to withdraw wbtc (contract balance)"
    print(f"""
==================================
owner_eth_balance_before
{owner_eth_balance_before}
==================================
owner_eth_balance_after
{owner_eth_balance_after}
==================================
owner_wbtc_balance_before
{owner_wbtc_balance_before}
==================================
owner_wbtc_balance_after
{owner_wbtc_balance_after}
==================================
degenify_contract_eth_balance_after
{degenify_contract_eth_balance_after}
==================================
degenify_contract_wbtc_balance_after
{degenify_contract_wbtc_balance_after}
==================================
    """)

def test_harvest_pickles(
    degenify_contract,
    owner,
    pickle_address,
    pickle_contract,
    wbtc_contract,
    wbtc_whale,
    whale
):
    eth_receive_amount = 500 * 10 ** 18
    whale.transfer(degenify_contract, eth_receive_amount)
    wbtc_receive_amount = 1 * 10 ** (8 - 1)
    wbtc_contract.transfer(degenify_contract, wbtc_receive_amount, {'from': wbtc_whale})
    degenify_contract.apeIntoSushiAndPickle(
        eth_receive_amount,     # uint _value
        wbtc_receive_amount,    # uint amountTokenDesired,
        wbtc_receive_amount,    # uint amountTokenMin,
        0,                      # uint amountETHMin,
        time.time() + 6000000,  # uint deadline,
        100,                    # uint _percentToPickleJar,
        100,                    # uint _percentToPickleFarm
        {'from': owner}
    )
    chain.sleep(60)
    chain.mine(1000)
    chain.sleep(60)
    degenify_contract.harvestPickle({'from': owner})
    degenify_pickle_balance_before = pickle_contract.balanceOf(degenify_contract)
    assert degenify_pickle_balance_before > 0, "didn't receive positive pickle dao token balance"    
    degenify_contract.withdrawToken(degenify_pickle_balance_before, pickle_address, {'from': owner})
    degenify_pickle_balance_after = pickle_contract.balanceOf(degenify_contract)
    assert degenify_pickle_balance_after == 0, "didn't receive zero pickle dao token balance"
    owner_pickle_balance = pickle_contract.balanceOf(owner)
    assert owner_pickle_balance == degenify_pickle_balance_before and owner_pickle_balance > 0, "didn't receive positive pickle dao token balance for owner"
    print(f"""
==================================
degenify_pickle_balance_before
{green}{degenify_pickle_balance_before}
{white}==================================
degenify_pickle_balance_after
{green}{degenify_pickle_balance_after}
{white}==================================
owner_pickle_balance
{green}{owner_pickle_balance}
{white}==================================
    """)

