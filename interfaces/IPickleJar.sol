pragma solidity ^0.6.7;

import { IERC20 } from "./IERC20.sol";

interface IPickleJar is IERC20 {
    function balance() external view returns (uint256);

    function setMin(uint256 _min) external;

    function setGovernance(address _governance) external;

    function setTimelock(address _timelock) external;

    function setController(address _controller) external;

    function available() external view returns (uint256);

    function earn() external;

    function depositAll() external;

    function deposit(uint256 _amount) external;

    function withdrawAll() external;

    // Used to swap any borrowed reserve over the debt limit to liquidate to 'token'
    function harvest(address reserve, uint256 amount) external;

    // No rebalance implementation for lower fees and faster swaps
    function withdraw(uint256 _shares) external;

    function getRatio() external view returns (uint256);
}
