async function fetchAndParseJSON() {
    try {
      // 发起 GET 请求从后端获取 JSON 数据
      const response = await fetch('/api/send_CA');
      
      // 检查 HTTP 响应状态
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      // 解析 JSON 数据
      const data = await response.json();
      
      // 打印或处理解析后的数据
      console.log(data.CA);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  }
  
  // 调用函数
  fetchAndParseJSON();