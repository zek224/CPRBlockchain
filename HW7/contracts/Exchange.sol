// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Uncomment this line to use console.log

import "hardhat/console.sol";

contract Exchange {
    event LiquidityProvided(
        uint256 amountERC20TokenDeposited,
        uint256 amountEthDeposited,
        uint256 liquidityPositionsIssued
    );
    event LiquidityWithdrew(
        uint256 amountERC20TokenWithdrew,
        uint256 amountEthWithdrew,
        uint256 liquidityPositionsBurned
    );
    event SwapForEth(
        uint256 amountERC20TokenDeposited,
        uint256 amountEthWithdrew
    );
    event SwapForERC20Token(
        uint256 amountERC20TokenWithdrew,
        uint256 amountEthDeposited
    );

    address public ERC20TokenAddress;
    uint256 public totalLiquidityPositions;
    uint256 public totalERC20TokenDeposited;
    uint256 public totalEthDeposited;
    uint256 public K;
    mapping(address => uint256) public liquidityPositions;

    constructor(address _ERC20TokenAddress) {
        ERC20TokenAddress = _ERC20TokenAddress;
    }

    //transfer ERC20 token to this contract
    // function transferERC20TokenToContract(uint _amountERC20Token) external {
    //     IERC20(ERC20TokenAddress).transferFrom(msg.sender, address(this), _amountERC20Token);
    // }

    function provideLiquidity(uint _amountERC20Token) external payable {
        curRatio = totalEthDeposited / totalERC20TokenDeposited;

        // transferERC20TokenToContract(_amountERC20Token);
        // uint amountERC20TokenDeposited = IERC20(ERC20TokenAddress).balanceOf(address(this)) - totalERC20TokenDeposited;

        // uint amountERC20TokenDeposited = IERC20(ERC20TokenAddress).balanceOf(address(this)) - totalERC20TokenDeposited;
        // uint amountEthDeposited = address(this).balance - totalEthDeposited;
        // uint liquidityPositionsIssued = 0;
    }

    function estimateEthToProvide(uint _amountERC20Token) public view returns (uint)
    {
        uint contractEthBalance = address(this).balance;
        uint contractERC20TokenBalance = IERC20(ERC20TokenAddress).balanceOf(address(this));
        uint amountEth = (contractEthBalance * _amountERC20Token) / contractERC20TokenBalance;
        return amountEth;
    }

    function estimateERC20TokenToProvide(uint _amountEth) public view returns (uint) {
        uint contractEthBalance = address(this).balance;
        uint contractERC20TokenBalance = IERC20(ERC20TokenAddress).balanceOf(address(this));
        uint amountERC20 = (contractERC20TokenBalance * _amountERC20Token) / contractEthBalance;
        return amountERC20;
    }

    function getMyLiquidityPositions() public view {}

    function withdrawLiquidity(uint _liquidityPositionsToBurn) external {}

    function swapForEth(uint _amountERC20Token) public view {}

    function estimateSwapForEth(uint _amountERC20Token) public view {}
}
