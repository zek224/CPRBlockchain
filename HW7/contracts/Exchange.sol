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

    function provideLiquidity() external payable {
        uint amountERC20TokenDeposited = IERC20(ERC20TokenAddress).balanceOf(address(this)) - totalERC20TokenDeposited;
        uint amountEthDeposited = address(this).balance - totalEthDeposited;
        uint liquidityPositionsIssued = 0;
        if (totalLiquidityPositions == 0) {
            liquidityPositionsIssued = (amountERC20TokenDeposited * amountEthDeposited) / 1000000000000000000;
        } else {
            liquidityPositionsIssued = (amountERC20TokenDeposited * totalLiquidityPositions) / totalERC20TokenDeposited;
        }
        totalLiquidityPositions += liquidityPositionsIssued;
        totalERC20TokenDeposited += amountERC20TokenDeposited;
        totalEthDeposited += amountEthDeposited;
        emit LiquidityProvided(amountERC20TokenDeposited, amountEthDeposited, liquidityPositionsIssued);
    }

    function estimateEthToProvide(uint _amountERC20Token) public view{

    }

    function estimateERC20TokenToProvide(uint _amountEth) public view{

    }

    function getMyLiquidityPositions() public view {

    }

    function withdrawLiquidity(uint _liquidityPositionsToBurn) external {

    }

    function swapForEth(uint _amountERC20Token) public view {

    }

    function estimateSwapForEth(uint _amountERC20Token) public view{

    }

}
