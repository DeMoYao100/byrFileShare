import json
import os

# 指定目录来保存CSR和私钥
data_directory = "user_data"

# 创建目录（如果不存在）
os.makedirs(data_directory, exist_ok=True)


def generate_key_pair():
    # 在实际应用中，使用真正的密钥生成算法
    private_key = "user_private_key"
    public_key = "user_public_key"
    return private_key, public_key


def generate_csr(user_id, org_name, public_key):
    csr_data = {
        "user_id": user_id,
        "org_name": org_name,
        "public_key": public_key
    }

    user_directory = os.path.join(data_directory, user_id)
    os.makedirs(user_directory, exist_ok=True)  # 创建用户目录

    # 保存CSR到用户目录
    csr_path = os.path.join(user_directory, "user-csr.json")
    with open(csr_path, "w") as csr_file:
        json.dump(csr_data, csr_file)

    return json.dumps(csr_data)


def save_data_to_file(user_id, private_key):
    user_directory = os.path.join(data_directory, user_id)
    os.makedirs(user_directory, exist_ok=True)

    private_key_path = os.path.join(user_directory, "private_key.pem")

    with open(private_key_path, "w") as private_key_file:
        private_key_file.write(private_key)


def main():
    user_id = input("Enter your user ID: ")
    org_name = input("Enter your organization name: ")

    # 生成用户密钥对
    private_key, public_key = generate_key_pair()

    # 生成CSR
    csr = generate_csr(user_id, org_name, public_key)

    # 保存私钥和CSR到指定目录
    save_data_to_file(user_id, private_key)

    print("User Key Pair Generated.")
    print("CSR Generated and Saved.")


if __name__ == "__main__":
    main()
