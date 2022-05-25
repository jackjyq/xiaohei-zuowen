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
  const 谓语标签 = document.querySelectorAll(
    ".输入区域 > div > div label[for='谓语']"
  )[0];
  谓语标签.style.opacity = "1";
}

function 隐藏谓语标签() {
  const 谓语标签 = document.querySelectorAll(
    ".输入区域 > div > div label[for='谓语']"
  )[0];
  谓语标签.style.opacity = "0";
}

function 显示宾语标签() {
  const 宾语标签 = document.querySelectorAll(
    ".输入区域  > div > div label[for='宾语']"
  )[0];
  宾语标签.style.opacity = "1";
}

function 隐藏宾语标签() {
  const 宾语标签 = document.querySelectorAll(
    ".输入区域 > div > div label[for='宾语']"
  )[0];
  宾语标签.style.opacity = "0";
}

window.addEventListener("click", function (事件) {
  // 控制示例区域显示
  const 示例区域 = document.getElementsByClassName("示例区域")[0];
  const 输入区域 = document.getElementsByClassName("输入区域")[0];
  const 谓语输入框 = document.getElementsByName("谓语")[0];
  const 宾语输入框 = document.getElementsByName("宾语")[0];
  const 点击区域 = 事件.target;
  if (!window.matchMedia("only screen and (max-width: 904px)").matches) {
    // 多栏布局不执行以下代码
    return;
  } else if (谓语输入框.contains(点击区域) || 宾语输入框.contains(点击区域)) {
    // 1000px 是一个随意指定的很大的数字
    示例区域.style.maxHeight = "1000px";
    示例区域.style.marginTop = "8px";
  } else if (!输入区域.contains(点击区域) && !示例区域.contains(点击区域)) {
    示例区域.style.maxHeight = "0";
    示例区域.style.marginTop = "0";
  } else {
    return;
  }
});
