function 复制作文() {
    const 作文 = document.getElementById("作文").textContent;
    const 临时文本区域 = document.createElement('textarea');
    临时文本区域.style.width = "0";
    临时文本区域.style.height = "0";
    临时文本区域.value =  作文;
    document.body.appendChild(临时文本区域);
    临时文本区域.select();
    临时文本区域.setSelectionRange(0, 99999)
    document.execCommand("copy");
    document.body.removeChild(临时文本区域);
    }

function 发送作文() {
    const 作文 = encodeURIComponent(document.getElementById("作文").textContent);
    const 标题 = encodeURIComponent(document.getElementById("标题").textContent);
    location.href = "mailto:" + "?&subject=" + 标题 + "&body=" + 作文;
    }

// https://stackoverflow.com/questions/3665115/how-to-create-a-file-in-memory-for-user-to-download-but-not-through-server
function 下载作文() {
    const 临时文本区域 = document.createElement('a');
    const 作文 = encodeURIComponent(document.getElementById("作文").textContent);
    const 标题 = document.getElementById("标题").textContent;
    临时文本区域.setAttribute('href', 'data:text/plain;charset=utf-8,' + 作文);
    临时文本区域.setAttribute('download', 标题+"(zuowen.jackjyq.com).txt");
    临时文本区域.style.display = 'none';
    document.body.appendChild(临时文本区域);
    临时文本区域.click();
    document.body.removeChild(临时文本区域);
    }

function 再来一篇() {
    location.reload()
}