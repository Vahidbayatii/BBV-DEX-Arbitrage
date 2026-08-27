#!/usr/bin/env python3
"""
BBV DEX Arbitrage Scanner — Cross-DEX & Cross-Chain Arbitrage Finder
Built by @bboyvahid1989
"""
import os, sys, json, time, requests
from web3 import Web3

# DEX Router Addresses
DEXES = {
    "pancakeswap": "0x10ED43C718714eb63d5aA57B78B54704E256024E",
    "uniswap_eth": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    "uniswap_bsc": "0xB6e2176B9776B5C3B5C3B5C3B5C3B5C3B5C3B5C3",
    "biswap": "0x3a6d8cA21D1CF76f653A67577FA0D27453350dD8",
    "ape_swap": "0xcF0feBd3f17CEf5b47b0cD79a1E4B2F8E6A1E5B2",
}

ROUTER_ABI = json.loads('[{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"}]')

def check_arbitrage(token_in, token_out, amount_in=Web3.to_wei(1, 'ether')):
    opportunities = []
    for dex1_name, dex1_addr in DEXES.items():
        for dex2_name, dex2_addr in DEXES.items():
            if dex1_name == dex2_name:
                continue
            try:
                router1 = w3.eth.contract(address=Web3.to_checksum_address(dex1_addr), abi=ROUTER_ABI)
                router2 = w3.eth.contract(address=Web3.to_checksum_address(dex2_addr), abi=ROUTER_ABI)
                out1 = router1.functions.getAmountsOut(amount_in, [token_in, token_out]).call()
                out2 = router2.functions.getAmountsOut(out1[-1], [token_out, token_in]).call()
                profit = out2[-1] - amount_in
                if profit > 0:
                    opportunities.append({
                        "buy_on": dex1_name,
                        "sell_on": dex2_name,
                        "profit_wei": profit,
                        "profit_eth": profit / 1e18,
                        "profit_percent": (profit / amount_in) * 100
                    })
            except:
                pass
    return opportunities

if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org"))
    WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
    BUSD = "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
    opps = check_arbitrage(WBNB, BUSD)
    for opp in opps:
        print(f"[+] {opp['buy_on']} → {opp['sell_on']}: {opp['profit_percent']:.2f}%")
