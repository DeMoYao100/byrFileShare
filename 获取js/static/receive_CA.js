/*
 传入服务器的api获取的CA
 本地u盾信息校验
*/
async function checkCA(CA){
    const fileCA = document.getElementById("dropCA");
    const file = fileCA.file[0];

    if (!file) {
        alert("Plz select a file.");
        return false;
    }

    const reader = new FileReader();
    reader.onload = async function (event) {
        const arraybuffer = event.target.result;
        //这里用arraybuffer检查CA，通过并返回True即可
        
    }



    return false;
}

/*
 服务器获取内容
*/
async function fetchAndParseJSON() {
    try {
        const response = await fetch('/api/send_CA');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data.CA);
        if (!checkCA(data.CA)){
            alert("The connection of you and the server is unsafe. Plz check your web connect.")
        }
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  }
fetchAndParseJSON();

checkCA(CA)