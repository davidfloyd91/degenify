// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;

import { IERC20 } from "../interfaces/IERC20.sol";
import { IPickleFarm } from "../interfaces/IPickleFarm.sol";
import { IPickleJar } from "../interfaces/IPickleJar.sol";
import { IUniswapV2Router02 } from "../interfaces/IUniswapV2Router02.sol";
import { IUniswapV2Factory } from "../interfaces/IUniswapV2Factory.sol";
import { SafeMath } from './libraries/SafeMath.sol';
import { UniswapV2Library } from './libraries/UniswapV2Library.sol';

contract Degenify {
    using SafeMath for uint256;

    string public name = "Degenify";

    address payable public owner;

    address wethAddress = address(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2);

    address wbtcAddress = address(0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599);
    IERC20 wbtc = IERC20(wbtcAddress);

    address slpEthWbtcAddress;

    address pslpEthWbtcAddress = address(0xde74b6c547bd574c3527316a2eE30cd8F6041525);
    IPickleJar pslpEthWbtcJar = IPickleJar(pslpEthWbtcAddress);

    address pslpEthWbtcGaugeAddress = address(0xD55331E7bCE14709d825557E5Bca75C73ad89bFb);
    IPickleFarm pslpEthWbtcFarm = IPickleFarm(pslpEthWbtcGaugeAddress);

    IUniswapV2Router02 sushiRouter = IUniswapV2Router02(address(0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F));

    event AddPickleFarm(uint pslpEthWbtcFarmBalanceAfter);
    event AddPickleJar(uint pslpETHWbtcBalanceAfter);
    event AddSushi(uint amountToken, uint amountETH, uint liquidity);
    event RemovePickleFarm(uint pslpEthWbtcFarmBalanceBefore, uint tpslpEthWbtcFarmBalanceAfter);
    event RemovePickleJar(uint slpEthWbtcBalanceBefore, uint slpEthWbtcBalanceAfter);
    event RemoveSushi(uint amountToken, uint amountETH);

    constructor() public {
        owner = payable(msg.sender);
    }

    modifier onlyOwner() {
        require(owner == msg.sender, "caller is not the owner");
        _;
    }

    function apeIntoSushiAndPickle(
        uint _value,
        uint amountTokenDesired,
        uint amountTokenMin,
        uint amountETHMin,
        uint deadline,
        uint _percentToPickleJar,
        uint _percentToPickleFarm
    ) public onlyOwner {
        slpEthWbtcAddress = UniswapV2Library.pairFor(address(0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac), wbtcAddress, wethAddress);

        uint slpEthWbtcBalanceBefore = IERC20(slpEthWbtcAddress).balanceOf(address(this));
        uint slpEthWbtcBalanceAfter = slpEthWbtcBalanceBefore;

        if (amountTokenDesired > 0) {
            (uint amountToken, uint amountETH, uint liquidity) = addLiquidityToETHWbtcSushi(
                _value,
                amountTokenDesired,
                amountTokenMin,
                amountETHMin,
                deadline
            );

            emit AddSushi(amountToken, amountETH, liquidity);

            slpEthWbtcBalanceAfter = IERC20(slpEthWbtcAddress).balanceOf(address(this));

            require(slpEthWbtcBalanceAfter >= liquidity, "didn't receive eth-wbtc sushi lp token");
        }

        uint pslpEthWbtcBalanceBefore = pslpEthWbtcJar.balanceOf(address(this));
        uint pslpETHWbtcBalanceAfter = pslpEthWbtcBalanceBefore;

        if (_percentToPickleJar > 0) {
            uint percentToPickleJar = _percentToPickleJar;

            if (_percentToPickleJar > 100) {
                percentToPickleJar = 100;
            }

            depositSlpEthWbtcToJar(percentToPickleJar, slpEthWbtcBalanceAfter);

            pslpETHWbtcBalanceAfter = pslpEthWbtcJar.balanceOf(address(this));

            emit AddPickleJar(pslpETHWbtcBalanceAfter);

            require(pslpETHWbtcBalanceAfter > pslpEthWbtcBalanceBefore, "didn't receive eth-wbtc slp pickle jar token");
        }

        uint pslpEthWbtcFarmBalanceBefore = pslpEthWbtcFarm.balanceOf(address(this));
        uint pslpEthWbtcFarmBalanceAfter = pslpEthWbtcFarmBalanceBefore;

        if (pslpETHWbtcBalanceAfter > 0 && _percentToPickleFarm > 0) {
            uint percentToPickleFarm = _percentToPickleFarm;

            if (_percentToPickleFarm > 100) {
                percentToPickleFarm = 100;
            }

            despositPslpEthWbtcToFarm(percentToPickleFarm, pslpETHWbtcBalanceAfter);

            pslpEthWbtcFarmBalanceAfter = pslpEthWbtcFarm.balanceOf(address(this));

            emit AddPickleFarm(pslpEthWbtcFarmBalanceAfter);

            require(pslpEthWbtcFarmBalanceAfter > pslpEthWbtcFarmBalanceBefore, "didn't receive eth-wbtc slp pickle farm token");
        }
    }

    function removeFromPickleFarm(
        uint pslpEthWbtcFarmBalanceBefore,
        uint _percentFromPickleFarm
    ) private {
        uint percentFromPickleFarm = _percentFromPickleFarm;

        if (_percentFromPickleFarm > 100) {
            percentFromPickleFarm = 100;
        }

        uint pslpEthWbtcToRemove = pslpEthWbtcFarmBalanceBefore.mul(percentFromPickleFarm).div(100);

        pslpEthWbtcFarm.withdraw(pslpEthWbtcToRemove);

        uint pslpEthWbtcFarmBalanceAfter = pslpEthWbtcFarm.balanceOf(address(this));

        emit RemovePickleFarm(pslpEthWbtcFarmBalanceBefore, pslpEthWbtcFarmBalanceAfter);
    }

    function removeFromPickleJar(
        uint slpEthWbtcBalanceBefore,
        uint _percentFromPickleJar
    ) private {
        uint percentFromPickleJar = _percentFromPickleJar;

        if (_percentFromPickleJar > 100) {
            percentFromPickleJar = 100;
        }

        uint pslpEthWbtcBalance = pslpEthWbtcJar.balanceOf(address(this));
        uint pslpEthWbtcToRemove = pslpEthWbtcBalance.mul(percentFromPickleJar).div(100);

        pslpEthWbtcJar.withdraw(pslpEthWbtcToRemove);

        uint slpEthWbtcBalanceAfter = IERC20(slpEthWbtcAddress).balanceOf(address(this));

        emit RemovePickleJar(slpEthWbtcBalanceBefore, slpEthWbtcBalanceAfter);
    }

    function removeFromSushi(
        uint slpEthWbtcBalance,
        uint _percentFromSushi,
        uint amountTokenMin,
        uint amountETHMin,
        uint deadline
    ) private {
        uint percentFromSushi = _percentFromSushi;

        if (_percentFromSushi > 100) {
            percentFromSushi = 100;
        }

        uint slpEthWbtcToRemove = slpEthWbtcBalance.mul(percentFromSushi).div(100);
        IERC20(slpEthWbtcAddress).approve(address(sushiRouter), slpEthWbtcToRemove);

        (uint amountToken, uint amountETH) = sushiRouter.removeLiquidityETH(
            wbtcAddress,
            slpEthWbtcToRemove,
            amountTokenMin,
            amountETHMin,
            address(this),
            deadline
        );

        emit RemoveSushi(amountToken, amountETH);
    }

    function bailOutOfSushiAndPickle(
        uint amountTokenMin,
        uint amountETHMin,
        uint deadline,
        uint _percentFromSushi,
        uint _percentFromPickleJar,
        uint _percentFromPickleFarm
    ) public onlyOwner {
        uint pslpEthWbtcFarmBalanceBefore = pslpEthWbtcFarm.balanceOf(address(this));

        if (pslpEthWbtcFarmBalanceBefore > 0 && _percentFromPickleFarm > 0) {
            removeFromPickleFarm(pslpEthWbtcFarmBalanceBefore, _percentFromPickleFarm);
        }

        uint pslpEthWbtcBalanceBefore = IERC20(pslpEthWbtcAddress).balanceOf(address(this));

        if (pslpEthWbtcBalanceBefore > 0 && _percentFromPickleJar > 0) {
            removeFromPickleJar(pslpEthWbtcBalanceBefore, _percentFromPickleJar);
        }

        uint slpEthWbtcBalance = IERC20(slpEthWbtcAddress).balanceOf(address(this));

        if (slpEthWbtcBalance > 0 && _percentFromSushi > 0) {
            removeFromSushi(slpEthWbtcBalance, _percentFromSushi, amountTokenMin, amountETHMin, deadline);
        }
    }

    function addLiquidityToETHWbtcSushi(
        uint _value,
        uint amountTokenDesired,
        uint amountTokenMin,
        uint amountETHMin,
        uint deadline
    ) private returns (uint amountToken, uint amountETH, uint liquidity) {
        wbtc.approve(address(sushiRouter), uint(-1));
        IERC20(wethAddress).approve(address(sushiRouter), uint(-1));

        (uint _amountToken, uint _amountETH, uint _liquidity) = sushiRouter.addLiquidityETH{
            value: _value
        }(
            wbtcAddress,
            amountTokenDesired,
            amountTokenMin,
            amountETHMin,
            address(this),
            deadline
        );

        return (_amountToken, _amountETH, _liquidity);
    }

    function despositPslpEthWbtcToFarm(
        uint percentToPickleFarm,
        uint pslpETHWbtcBalance
    ) private {
        uint depositAmount = pslpETHWbtcBalance.mul(percentToPickleFarm).div(100);
        IERC20(pslpEthWbtcAddress).approve(address(pslpEthWbtcFarm), depositAmount);

        pslpEthWbtcFarm.deposit(depositAmount);
    }

    function depositSlpEthWbtcToJar(
        uint percentToPickleJar,
        uint slpEthWbtcBalance
    ) private {
        uint depositAmount = slpEthWbtcBalance.mul(percentToPickleJar).div(100);
        IERC20(slpEthWbtcAddress).approve(address(pslpEthWbtcJar), depositAmount);

        pslpEthWbtcJar.deposit(depositAmount);
    }

    function updateOwner(address payable _owner) public onlyOwner {
        owner = _owner;
    }

    function withdrawETH(uint _amount) public onlyOwner {
        owner.transfer(_amount);
    }

    function withdrawToken(uint _amount, address _token) public onlyOwner {
        IERC20(_token).transfer(owner, _amount);
    }

    receive() external payable {}
}
