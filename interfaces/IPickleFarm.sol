// SPDX-License-Identifier: MIT

pragma solidity ^0.6.7;

interface IPickleFarm {
    function totalSupply() external view returns (uint256);

    function balanceOf(address account) external view returns (uint256);

    function lastTimeRewardApplicable() external view returns (uint256);

    function rewardPerToken() external view returns (uint256);
    
    function derivedBalance(address account) external view returns (uint);
    
    function kick(address account) external;

    function earned(address account) external view returns (uint256);

    function getRewardForDuration() external view returns (uint256);
    
    function depositAll() external;
    
    function deposit(uint256 amount) external;
    
    function depositFor(uint256 amount, address account) external;
    
    function withdrawAll() external;

    function withdraw(uint256 amount) external;

    function getReward() external;

    function exit() external;
    
    function notifyRewardAmount(uint256 reward) external;
}
