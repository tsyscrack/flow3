import base58
from solders.keypair import Keypair
import os
from tqdm import tqdm


def generate_wallet():
    """生成一个钱包并返回地址和私钥"""
    new_account = Keypair()
    wallet_address = str(new_account.pubkey())
    private_key_bytes = new_account.secret()
    public_key_bytes = bytes(new_account.pubkey())
    encoded_keypair = private_key_bytes + public_key_bytes
    private_key = base58.b58encode(encoded_keypair).decode()
    return wallet_address, private_key


def batch_generate_wallets(count=1000, output_file="accounts.txt"):
    """
    批量生成指定数量的钱包并保存私钥

    Args:
        count (int): 要生成的钱包数量
        output_file (str): 存储私钥的文件路径

    Returns:
        list: 包含所有生成的私钥列表
    """
    private_keys = []

    # 使用 tqdm 显示生成进度
    with tqdm(total=count, desc="Generating wallets") as pbar:
        for _ in range(count):
            _, private_key = generate_wallet()
            private_keys.append(private_key)
            pbar.update(1)

    # 确保输出目录存在
    output_dir = os.path.dirname(os.path.abspath(output_file))
    os.makedirs(output_dir, exist_ok=True)

    # 写入文件（原子操作）
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(private_keys))
        print(f"成功生成 {count} 个钱包，私钥已保存至 {output_file}")
    except IOError as e:
        print(f"写入文件失败: {e}")
        raise


if __name__ == "__main__":
    # 生成1000个钱包并保存
    batch_generate_wallets(1000)
