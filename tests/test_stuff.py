import time
from brownie import reverts

# brownie test --interactive -s -v

def test_update_owner(
    degenify_contract,
    owner,
    puppet,
    very_bad_man
):
    assert(degenify_contract.owner() == owner)
    with reverts():
        degenify_contract.updateOwner(very_bad_man, {'from': very_bad_man})
    assert(degenify_contract.owner() == owner)
    degenify_contract.updateOwner(puppet, {'from': owner})
    assert(degenify_contract.owner() == puppet)
    with reverts():
        degenify_contract.updateOwner(owner, {'from': owner})
    degenify_contract.updateOwner(owner, {'from': puppet})
    assert(degenify_contract.owner() == owner)

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
    assert(degenify_contract_balance_after - degenify_contract_balance_before == receive_amount)
    with reverts():
        degenify_contract.withdrawETH(receive_amount, {'from': very_bad_man})
    owner_balance_before = owner.balance()
    degenify_contract.withdrawETH(receive_amount, {'from': owner})
    owner_balance_after = owner.balance()
    assert(owner_balance_after - owner_balance_before == receive_amount)

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
    assert(degenify_contract_balance_after - degenify_contract_balance_before == receive_amount)
    with reverts():
        degenify_contract.withdrawToken(receive_amount, wbtc_address, {'from': very_bad_man})
    owner_balance_before = wbtc_contract.balanceOf(owner)
    degenify_contract.withdrawToken(receive_amount, wbtc_address, {'from': owner})
    owner_balance_after = wbtc_contract.balanceOf(owner)
    assert(owner_balance_after - owner_balance_before == receive_amount)

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
    degenify_contract.apeSushiAndPickle(
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
    print("slp_eth_wbtc_balance", slp_eth_wbtc_balance)
    assert(slp_eth_wbtc_balance > 0)
