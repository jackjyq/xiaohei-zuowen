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

function 发送邮件() {
    const 作文 = encodeURIComponent(document.getElementById("作文").textContent);
    const 标题 = encodeURIComponent(document.getElementById("标题").textContent);
    location.href = "mailto:" + "?&subject=" + 标题 + "&body=" + 作文;
    }