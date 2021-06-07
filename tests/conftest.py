import pytest
from brownie import Contract

@pytest.fixture
def degenify_contract(Degenify, owner):
    yield owner.deploy(Degenify)

############
# accounts #
############

@pytest.fixture
def owner(accounts):
    yield accounts[0]

@pytest.fixture
def puppet(accounts):
    yield accounts[2]

@pytest.fixture
def very_bad_man(accounts):
    yield accounts[1]

@pytest.fixture
def whale(accounts):
    yield accounts.at("0x73bceb1cd57c711feac4224d062b0f6ff338501e", True)

@pytest.fixture
def wbtc_whale(accounts):
    yield accounts.at("0xbf72da2bd84c5170618fbe5914b0eca9638d5eb5", True)

##########
# assets #
##########

@pytest.fixture
def pslp_eth_wbtc_address():
    yield "0xde74b6c547bd574c3527316a2eE30cd8F6041525"

@pytest.fixture
def pslp_eth_wbtc_contract(pslp_eth_wbtc_address):
    yield Contract(pslp_eth_wbtc_address)

@pytest.fixture
def pslp_eth_wbtc_farm_address():
    yield "0xD55331E7bCE14709d825557E5Bca75C73ad89bFb"

@pytest.fixture
def pslp_eth_wbtc_farm_contract(pslp_eth_wbtc_farm_address):
    yield Contract(pslp_eth_wbtc_farm_address)

@pytest.fixture
def slp_eth_wbtc_address(
    sushi_factory,
    wbtc_address,
    weth_address
):
    yield sushi_factory.getPair(wbtc_address, weth_address)

@pytest.fixture
def slp_eth_wbtc_contract(
    slp_eth_wbtc_address
):
    yield Contract(slp_eth_wbtc_address)

@pytest.fixture
def sushi_factory_address():
    yield "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"

@pytest.fixture
def sushi_factory(sushi_factory_address):
    yield Contract(sushi_factory_address)

@pytest.fixture
def wbtc_address():
    yield "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"

@pytest.fixture
def wbtc_contract(wbtc_address):
    yield Contract(wbtc_address)

@pytest.fixture
def weth_address():
    yield "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"

@pytest.fixture
def weth_contract(weth_address):
    yield Contract(weth_address)
