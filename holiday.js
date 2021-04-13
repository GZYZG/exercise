
// info是个人信息，如果有需要更改的，则把对应的信息写道对应的位置。
// 例如，要修改姓名，可以在 "学号"所对应的"" 内填入 名字，如 "赵琼"
info = {
学号: "202032051315",
姓名: "谢梦圆",
身份证号: "423422199804255335",
电话: "15275601582",
学期: "第二学期",
请假天数: "",
请假类型: "其他事假",
请假开始时间: "2021-03-30",
请假结束时间: "2021-03-30",
请假事由: "",
审核时间: "2021-03-29 10:12:22"

}

// holiday 是修改信息的函数
function holiday(info){
	if(info.学号 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > a").innerText = info.学号;
	
	if(info.姓名 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4)").innerText = info.姓名;
	
	if(info.身份证号 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(4)").innerText = info.身份证号;

	if(info.电话 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(4)").innerText = info.电话;

	if(info.学期 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(4)").innerText = info.学期;
	
	if(info.请假天数 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(2) > td:nth-child(2)").innerText = info.请假天数;

	if(info.请假类型 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(2) > td:nth-child(4)").innerText = info.请假类型;

	if(info.请假开始时间 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(3) > td:nth-child(2)").innerText = info.请假开始时间;

	if(info.请假结束时间 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(3) > td:nth-child(4)").innerText = info.请假结束时间;
	
	if(info.请假事由 != "")
		document.querySelector("#form > div:nth-child(5) > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(4) > td").innerText = info.请假事由;
	
	if(info.审核时间 != "")
		document.querySelector("#shlccx_table > tbody > tr:nth-child(2) > td:nth-child(5)").innerText = info.审核时间;
}


// 修改流程：
// 1. 使用电脑的浏览器登录你的学生管理系统账号；
// 2. 日常事务 =》 请假管理 =》 请假申请；
// 3. 在请假表格处，点击第一行的学号列，弹出"请假申请信息" 表；
// 4. 按F12键，在浏览器右侧或者下侧会出现一个面板，在这个面板里找到 "控制台" 或 "console" 字样，点击它；
// 5. 可以在 "控制台" 或 "console" 下方看到类似与这样的符号：">"，这表示你可以在这里输入信息；
// 6. 把上面的 info 填好，复制粘贴到 ">" 那里，回车表示确认输入；
// 7. 把上面的 holiday复制到 ">" 那里，回车确认之；
// 8. 在 ">" 后输入 holiday(info)，回车确认之；
// 9. 查看 "请假申请信息" 表中的信息是否如你所愿？
// 10. 若如你所愿，再按F12，关掉 4. 中的面板，调整好 "请假申请信息"表的位置，截图，请假成过；
// 11. 若不如你所愿，按照流程检查自己是否操作得当，若操作无误，请联系赵琼；
//
// 祝请假成功！！！




