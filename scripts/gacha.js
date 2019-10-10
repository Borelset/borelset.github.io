var start = document.getElementById("start");
var end = document.getElementById("end");
var screen = document.getElementById("screen");
var dianming = false; //是否正在抽奖
var names=new Array("曾绍恒", "陈昊阳", "陈奕舸", "陈语丹", "邓琳娜", "邓伊涵", "邓毅豪", "邓懿辰", "丁绪行", "杜彦希", "方敬", "付梓萱", "桂一菲", "黄恩平", "黄凯翊", "黄梦轩", "贾婷萱", "江宏博", "雷梓悦", "李博硕", "李辰恺", "李卓冉", "林明熙", "刘羽晨", "刘子墨", "路子墨", "彭昊", "邱建锟", "邱以晴", "谭陈骏", "谭欣睿", "涂天骄", "王鹤骞", "韦雅曦", "肖渝阳", "徐翊宸", "许哲岚", "杨歆艺", "杨梓雯", "叶思彤", "张浩轩", "张骏祥", "张思浩", "钟嘉朗", "周玉婷", "周祖瑶", "庄雅桐")
var length = names.length;
var index = 0;
start.onclick = function () {
    console.log("start");
    dianming = true
    while (dianming) {
        screen.text = names[index%length]
    }
}
end.onclick = function () {
    console.log("end");
    dianming = false;
}
