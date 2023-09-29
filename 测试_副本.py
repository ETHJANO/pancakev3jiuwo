import traceback

from hexbytes import HexBytes
from web3 import Web3

from utils import get_abi

# 初始化 Web3
w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))

# Uniswap V3 Quoter 合约 ABI（请从官方源获得真实的 ABI）
UNISWAP_V3_QUOTER_ABI = get_abi('UniswapV3Quoter')
# Quoter 合约地址
UNISWAP_V3_QUOTER_ADDRESS = Web3.to_checksum_address('0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997')
quoter_contract = w3.eth.contract(address=UNISWAP_V3_QUOTER_ADDRESS, abi=UNISWAP_V3_QUOTER_ABI)
CANTO_ADDRESS = Web3.to_checksum_address('0x56C03B8C4FA80Ba37F5A7b60CAAAEF749bB5b220')
WETH_ADDRESS = Web3.to_checksum_address('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
USDT_ADDRESS = Web3.to_checksum_address('0xdAC17F958D2ee523a2206206994597C13D831ec7')


def calculate_path(*param) -> HexBytes:
    """
    计算路径
    :param param: [token_address, fee, token_address, fee, ...
    :return:
    """
    if len(param) < 3:
        Exception("param count must be greater than 3")
    i = 0
    path = ""
    while i < len(param):
        if i % 2 == 0:
            # token address
            path += param[i][2:].lower()
        else:
            # fee
            hex_num_with_zero = format(param[i], '06x')
            path += hex_num_with_zero
        i += 1
    path = '0x' + path
    return HexBytes(path)


def main():
    path_bytes = calculate_path(CANTO_ADDRESS, 10000, WETH_ADDRESS, 500, USDT_ADDRESS)

    amount_in = w3.to_wei(1, 'ether')  # 例如，你想知道 1 Token的报价

    try:
        # 使用 quoteExactInput 函数
        quote = quoter_contract.functions.quoteExactInput(path_bytes, amount_in).call()
        expected_output_amount = quote[0]
        print(f"For {amount_in} of token, you get {expected_output_amount} USDT")
    except Exception as e:
        print(f"Error getting quote: {e}")
        traceback.print_exc()


if __name__ == '__main__':
    main()
