function 复制作文() {
  const 作文 = document.getElementById("作文").textContent;
  const 临时文本区域 = document.createElement("textarea");
  临时文本区域.style.width = "0";
  临时文本区域.style.height = "0";
  临时文本区域.value = 作文;
  document.body.appendChild(临时文本区域);
  临时文本区域.select();
  临时文本区域.setSelectionRange(0, 99999);
  document.execCommand("copy");
  document.body.removeChild(临时文本区域);
}

function 显示谓语标签() {
  const 谓语标签 = document.querySelectorAll(".输入框 label")[0];
  谓语标签.style.display = "block";
}

function 隐藏谓语标签() {
  const 谓语标签 = document.querySelectorAll(".输入框 label")[0];
  谓语标签.style.display = "none";
}

function 显示宾语标签() {
  const 宾语标签 = document.querySelectorAll(".输入框 label")[1];
  宾语标签.style.display = "block";
}

function 隐藏宾语标签() {
  const 宾语标签 = document.querySelectorAll(".输入框 label")[1];
  宾语标签.style.display = "none";
}

window.addEventListener("click", function (事件) {
  // 控制示例区域显示
  const 示例区域 = document.getElementById("示例");
  const 谓语输入框 = document.getElementById("谓语");
  const 宾语输入框 = document.getElementById("宾语");
  const 输入框及示例区域 = document.getElementsByTagName("header")[0];
  const 点击区域 = 事件.target;
  if (谓语输入框.contains(点击区域) || 宾语输入框.contains(点击区域)) {
    // 1000px 是一个随意指定的很大的数字
    示例区域.style.maxHeight = "1000px";
  } else if (!输入框及示例区域.contains(点击区域)) {
    示例区域.style.maxHeight = "0";
  } else {
  }
});
