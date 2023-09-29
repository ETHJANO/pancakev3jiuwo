def get_abi(name):
    """
    获取abi
    :param name:
    :return:
    """
    with open(f"./abi/{name}.abi", 'r') as f:
        abi = f.read()
    return abi