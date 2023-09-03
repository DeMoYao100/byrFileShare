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
        //这里检查arraybuffer，通过并返回True即可

    }



    return false;
}

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