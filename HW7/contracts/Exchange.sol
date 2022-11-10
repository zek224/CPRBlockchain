// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Uncomment this line to use console.log

import "hardhat/console.sol";

contract Exchange {
    event LiquidityProvided(
        uint amountERC20TokenDeposited,
        uint amountEthDeposited,
        uint liquidityPositionsIssued
    );
    event LiquidityWithdrew(
        uint amountERC20TokenWithdrew,
        uint amountEthWithdrew,
        uint liquidityPositionsBurned
    );
    event SwapForEth(
        uint amountERC20TokenDeposited,
        uint amountEthWithdrew
    );
    event SwapForERC20Token(
        uint amountERC20TokenWithdrew,
        uint amountEthDeposited
    );

    address public ERC20TokenAddress;
    uint public totalLiquidityPositions;
    uint public K;
    mapping(address => uint) public liquidityPositions;

    constructor(address _ERC20TokenAddress) {
        ERC20TokenAddress = _ERC20TokenAddress;
    }

    //helper function
    function ethBalance() public view returns (uint) {
        return address(this).balance;
    }

    //helper function
    function erc20TokenBalance() public view returns (uint) {
        return ERC20(ERC20TokenAddress).balanceOf(address(this));
    }

    function provideLiquidity(uint _amountERC20Token) external payable returns (uint) {
        require(ERC20(ERC20TokenAddress).transferFrom(msg.sender, address(this), _amountERC20Token), "You must approve the contract to transfer your ERC20 tokens");
        require(payable(msg.sender).transfer(msg.value), "You must approve the contract to transfer your ETH");
        require(_amountERC20Token > 0, "Amount must be greater than 0");
        require(msg.value > 0, "Amount must be greater than 0");
        
        uint liquidityPositionsIssued = 0;

        if(totalLiquidityPositions == 0) {
            liquidityPositionsIssued = 100;
        } else {
            require((totalLiquidityPositions * _amountERC20Token)/ erc20TokenBalance() == (totalLiquidityPositions * msg.value) / (ethBalance() - msg.value), "You must send ETH to provide liquidity");
            liquidityPositionsIssued = totalLiquidityPositions * _amountERC20Token / erc20TokenBalance();
        }

        liquidityPositions[msg.sender] += liquidityPositionsIssued;
        totalLiquidityPositions += liquidityPositionsIssued;

        K = ethBalance() * erc20TokenBalance();

        emit LiquidityProvided(_amountERC20Token, msg.value, liquidityPositionsIssued);
        return liquidityPositionsIssued;

        //amountEth -> msg.value
        //use transferFrom to transfer ERC20Token from msg.sender to this contract
    }

    function estimateEthToProvide(uint _amountERC20Token) public view returns (uint)
    {
        uint amountEth = (ethBalance() * _amountERC20Token) / erc20TokenBalance();
        return amountEth;
    }

    function estimateERC20TokenToProvide(uint _amountEth) public view returns (uint) {
        uint amountERC20 = (erc20TokenBalance() * _amountEth) / ethBalance();
        return amountERC20;
    }

    function getMyLiquidityPositions() public view returns (uint) {
        return liquidityPositions[msg.sender];
    }

    function withdrawLiquidity(uint _liquidityPositionsToBurn) public returns (uint, uint) {
        uint amountEthToSend = _liquidityPositionsToBurn * ethBalance() / totalLiquidityPositions;
        uint amountERC20TokenToSend = _liquidityPositionsToBurn * erc20TokenBalance() / totalLiquidityPositions;
        
        require(liquidityPositions[msg.sender] >= _liquidityPositionsToBurn, "You don't have enough liquidity positions to burn");
        require(_liquidityPositionsToBurn < totalLiquidityPositions, "You can't burn all liquidity positions");
        
        liquidityPositions[msg.sender] -= _liquidityPositionsToBurn;
        totalLiquidityPositions -= _liquidityPositionsToBurn;

        require(payable(msg.sender).send(amountEthToSend), "You must have enough ETH to withdraw");
        require(ERC20(ERC20TokenAddress).transfer(msg.sender, amountERC20TokenToSend), "You must have enough ERC20 tokens to withdraw");
       
        K = ethBalance() * erc20TokenBalance();
        
        emit LiquidityWithdrew(amountERC20TokenToSend, amountEthToSend, _liquidityPositionsToBurn);
        return (amountERC20TokenToSend, amountEthToSend);
        
    }

    function swapForEth(uint _amountERC20Token) public returns (uint) {
        require(_amountERC20Token > 0, "Amount must be greater than 0");
        
        uint contractEthBalanceAfterSwap = K / (erc20TokenBalance() - _amountERC20Token);
        uint ethToSend = ethBalance() - contractEthBalanceAfterSwap;

        require(ERC20(ERC20TokenAddress).transferFrom(msg.sender, address(this), _amountERC20Token), "You must approve the contract to transfer your ERC20 tokens");

        require(payable(msg.sender).send(ethToSend), "You must have enough ETH to swap");

        emit SwapForEth(_amountERC20Token, ethToSend);
        
        return ethToSend;

    }

    function estimateSwapForEth(uint _amountERC20Token) public view returns (uint){
        uint contractEthBalanceAfterSwap = K / (erc20TokenBalance() - _amountERC20Token);
        uint ethToSend = ethBalance() - contractEthBalanceAfterSwap;

        return ethToSend;
    }

    function swapForERC20Token() payable public returns (uint) {
        require(msg.value > 0, "Amount must be greater than 0");
        
        require(payable(address(this)).send(msg.value), "You must have enough ETH to swap");

        uint contractERC20TokenBalanceAfterSwap = K / ethBalance();
        
        uint ERC20TokenToSend = erc20TokenBalance() - contractERC20TokenBalanceAfterSwap;

        require(ERC20(ERC20TokenAddress).transfer(msg.sender, ERC20TokenToSend), "You must have enough ERC20 tokens to swap");

        emit SwapForERC20Token(ERC20TokenToSend, msg.value);

        return ERC20TokenToSend;
        
    }

    function estimateSwapForERC20Token(uint _amountEth) public view returns (uint){
        uint contractERC20TokenBalanceAfterSwap = K / (ethBalance() - _amountEth);
        uint erc20TokenToSend = erc20TokenBalance() - contractERC20TokenBalanceAfterSwap;

        return erc20TokenToSend;
    }
}