async function generateKey() {
    const key = await crypto.subtle.generateKey(
      {
        name: "AES-CBC",
        length: 256
      },
      true,
      ["encrypt", "decrypt"]
    );
    return key;
  }
  
  async function encryptArrayBuffer(key, arrayBuffer) {
    const iv = crypto.getRandomValues(new Uint8Array(16));
    const ciphertext = await crypto.subtle.encrypt(
      {
        name: "AES-CBC",
        iv: iv
      },
      key,
      arrayBuffer
    );
  
    return { ciphertext, iv };
  }
  
  async function encryptAndUpload() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
  
    if (!file) {
      alert("Please select a file!");
      return;
    }
  
    const reader = new FileReader();
  
    reader.onload = async function (event) {
      const arrayBuffer = event.target.result;
  
      // 生成密钥并加密文件
      // const key = await generateKey();
      const rawKey = new TextEncoder().encode('This_is_an_example_key_for_demo!');
      const key = await crypto.subtle.importKey(
        'raw', 
        rawKey, 
        { name: 'AES-CBC', length: 256 }, 
        true, 
        ['encrypt', 'decrypt']
      );
      const { ciphertext, iv } = await encryptArrayBuffer(key, arrayBuffer);
  
      // 创建 FormData 对象并添加加密后的文件和 IV
      const formData = new FormData();
      formData.append("fileInput", new Blob([new Uint8Array(ciphertext)]), file.name + ".enc");
      formData.append("iv", new Blob([iv]));
  
      fetch('http://127.0.0.1:5000/', {
        method: 'POST',
        body: formData
      }).then(response => response.json())
        .then(data => {
          console.log("Upload successful:", data);
        })
        .catch(error => {
          console.log("Upload failed:", error);
        });
    };
  
    reader.onerror = function (event) {
      console.error("File read error:", event.target.error);
    };
  
    reader.readAsArrayBuffer(file);
  }
  