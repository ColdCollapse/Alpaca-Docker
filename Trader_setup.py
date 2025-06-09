#!/bin/python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run trader bot for a specific symbol.")
    parser.add_argument("-sy", "--symbol", required=True, help="Stock symbol to trade")

    args = parser.parse_args()
    symbol = args.symbol

    print(f"Running strategy for symbol: {symbol}")
    # Call your trading logic here...

if __name__ == "__main__":
    main()
