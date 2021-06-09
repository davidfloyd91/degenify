from brownie import Degenify, accounts

def main():
    acct = accounts.load('deploy_account')
    acct.deploy(Degenify)
