// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Uncomment this line to use console.log
// import "hardhat/console.sol";

contract Exchange {
    event LiquidityProvided(uint amountERC20TokenDeposited, uint amountEthDeposited, uint liquidityPositionsIssued);
    event LiquidityWithdrew(uint amountERC20TokenWithdrew, uint amountEthWithdrew, uint liquidityPositionsBurned);
    event SwapForEth(uint amountERC20TokenDeposited, uint amountEthWithdrew);
    event SwapForERC20Token(uint amountERC20TokenWithdrew, uint amountEthDeposited);

    address public ERC20TokenAddress;
    uint public totalLiquidityPositions;
    uint public totalERC20TokenDeposited;
    uint public totalEthDeposited;

    constructor(address _ERC20TokenAddress) {
        ERC20TokenAddress = _ERC20TokenAddress;
    }


    function provideLiquidity(uint _amountERC20Token) external payable {
        uint ERC20TokenDeposit = IERC20(ERC20TokenAddress).balanceOf(address(this)) - totalERC20TokenDeposited;



    }

    function estimateEthToProvide(uint _amountERC20Token){

    }

    function estimateERC20TokenToProvide(uint _amountEth){

    }

    function getMyLiquidityPositions(){

    }

    function withdrawLiquidity(uint _liquidityPositionsToBurn) external {

    }

    }

    function swapForEth(uint _amountERC20Token){

    }

    function estimateSwapForEth(uint _amountERC20Token){

    }



}
