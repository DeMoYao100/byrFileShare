const fs = require('fs');
const { X509Name, CSR, hash } = require('jsrsasign');

function generateCSR() {
    // 用户信息
    const user_info = {
        organization_name: "bupt",
        common_name: "AO",
    };

    // 生成用户的公钥和私钥
    const keySize = 2048;
    const key = new RSAKey();
    key.generate(keySize, '10001'); // '10001' is the public exponent commonly used

    // 指定私钥保存路径
    const privateKeyPath = "path/to/user_private_key.pem";

    // 将私钥保存到指定路径
    const private_key_pem = key.getPEMString();
    fs.writeFileSync(privateKeyPath, private_key_pem);

    // 生成CSR
    const csr = new CSR();
    const subjectAltNames = [{ name: 'dNSName', value: user_info.common_name }];
    csr.setSubjectByParam({
        o: user_info.organization_name,
        cn: user_info.common_name,
    });
    csr.setSubjectAltNameArray(subjectAltNames);

    // 使用私钥对CSR进行签名
    csr.sign(key, hash.SHA256);

    // 将CSR保存到文件
    const csrPath = "path/to/user_csr.pem";
    const csr_pem = csr.getPEMString();
    fs.writeFileSync(csrPath, csr_pem);
}

generateCSR();
