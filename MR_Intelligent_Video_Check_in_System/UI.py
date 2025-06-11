import tkinter as tk
from tkinter import messagebox, simpledialog

from service.hr_service import update_admin
from util import camera
from util import public_tools as tool
from service import hr_service as hr
from entity import organizations as o
import threading

# 全局变量：管理员登录状态
# ADMIN_LOGIN = tk.BooleanVar(value=False)


# 加载员工数据
hr.load_emp_data()

# 人脸打卡
def face_clock():
    def run_clock_in():
        messagebox.showinfo("打卡", "请正面对准摄像头进行打卡")
        name = camera.clock_in()
        if name:
            hr.add_lock_record(name)
            messagebox.showinfo("打卡成功", f"{name} 打卡成功！")
        else:
            messagebox.showerror("打卡失败", "识别失败，请重试")

    threading.Thread(target=run_clock_in).start()

# 查看记录
def check_record():
    if not ADMIN_LOGIN.get():
        messagebox.showerror("权限错误", "请先进行管理员登录")
        return

    record_window = tk.Toplevel(root)
    record_window.title("查看记录")
    record_window.geometry("400x300")

    def handle_option(option):
        if option == "1":
            employee_list = hr.get_employee_report()
            messagebox.showinfo("员工列表", employee_list)
        elif option == "2":
            record_list = hr.get_record_all()
            messagebox.showinfo("打卡记录", record_list)
        elif option == "3":
            record_window.destroy()

    tk.Label(record_window, text="查看记录功能菜单", font=("Arial", 12, "bold")).pack()
    tk.Button(record_window, text="①查看员工列表", command=lambda: handle_option("1")).pack(fill="x")
    tk.Button(record_window, text="②查看打卡记录", command=lambda: handle_option("2")).pack(fill="x")
    tk.Button(record_window, text="③返回上级菜单", command=lambda: handle_option("3")).pack(fill="x")

# 员工管理
def employee_management():
    if not ADMIN_LOGIN.get():
        messagebox.showerror("权限错误", "请先进行管理员登录")
        return

    management_window = tk.Toplevel(root)
    management_window.title("员工管理")
    management_window.geometry("400x300")

    # 获取并格式化员工名单
    raw_report = hr.get_employee_report()
    lines = raw_report.strip().splitlines()
    formatted = "###########################################\n员工名单如下：\n"
    for line in lines:
        formatted += line + "\n"
    formatted += "###########################################"

    # 显示员工名单
    tk.Label(management_window, text=formatted, justify="left", anchor="w", font=("Courier New", 10), bg="white").pack(
        padx=10, pady=10, fill="x")

    def handle_option(option):
        if option == "1":
            name = simpledialog.askstring("录入新员工", "请输入新员工姓名(输入0取消操作)：")
            if name and name != "0":
                code = hr.add_new_employee(name)
                messagebox.showinfo("拍照提示", "请面对摄像头，敲击三次回车键完成拍照！")
                camera.register(code)
                messagebox.showinfo("成功", f"员工 {name} 录入成功！")
        elif option == "2":
            employee_list = hr.get_employee_report()
            messagebox.showinfo("员工列表", employee_list)
            id = simpledialog.askinteger("删除员工", "请输入要删除的员工编号(输入0取消操作)：")
            if id and id > 0:
                if hr.check_id(id):
                    verification = tool.randomNumber(4)
                    inputVer = simpledialog.askstring("验证码", f"请输入验证码 [{verification}]：")
                    if str(verification) == str(inputVer).strip():
                        hr.remove_employee(id)
                        messagebox.showinfo("删除成功", f"{id} 号员工已删除！")
                    else:
                        messagebox.showerror("错误", "验证码有误，操作取消")
                else:
                    messagebox.showerror("错误", "无此员工，操作取消")
        elif option == "3":
            management_window.destroy()

    tk.Label(management_window, text="员工管理功能菜单", font=("Arial", 12, "bold")).pack()
    tk.Button(management_window, text="①录入新员工", command=lambda: handle_option("1")).pack(fill="x")
    tk.Button(management_window, text="②删除员工", command=lambda: handle_option("2")).pack(fill="x")
    tk.Button(management_window, text="③返回上级菜单", command=lambda: handle_option("3")).pack(fill="x")

# 报表设置
def report_config():
    config_window = tk.Toplevel(root)
    config_window.title("报表设置")
    config_window.geometry("400x300")

    def handle_option(option):
        if option == "1":
            work_time = simpledialog.askstring("设置上班时间", "请输入上班时间（格式 08:00:00）：")
            if not tool.valid_time(work_time):
                messagebox.showerror("错误", "上班时间格式错误")
                return
            close_time = simpledialog.askstring("设置下班时间", "请输入下班时间（格式 23:59:59）：")
            if not tool.valid_time(close_time):
                messagebox.showerror("错误", "下班时间格式错误")
                return
            hr.save_work_time(work_time, close_time)
            messagebox.showinfo("设置成功", f"上班：{work_time} 下班：{close_time}")
        elif option == "2":
            config_window.destroy()

    tk.Label(config_window, text="报表设置功能菜单", font=("Arial", 12, "bold")).pack()
    tk.Button(config_window, text="①作息时间设置", command=lambda: handle_option("1")).pack(fill="x")
    tk.Button(config_window, text="②返回上级菜单", command=lambda: handle_option("2")).pack(fill="x")

# 考勤报表
def check_report():
    if not ADMIN_LOGIN.get():
        messagebox.showerror("权限错误", "请先进行管理员登录")
        return

    report_window = tk.Toplevel(root)
    report_window.title("考勤报表")
    report_window.geometry("400x300")

    def handle_option(option):
        if option == "1":
            date = simpledialog.askstring("日报查询", "输入日期(2008-08-08)，0表示今天：")
            if date == "0":
                hr.get_today_report()
            elif tool.valid_date(date):
                hr.get_day_report(date)
            else:
                messagebox.showerror("错误", "日期格式错误")
        elif option == "2":
            date = simpledialog.askstring("月报查询", "输入月份(2008-08)，0表示上个月：")
            if date == "0":
                hr.get_pre_month_report()
            elif tool.valid_year_month(date):
                hr.get_month_report(date)
            else:
                messagebox.showerror("错误", "日期格式错误")
        elif option == "3":
            report_config()
        elif option == "4":
            report_window.destroy()

    tk.Label(report_window, text="考勤报表功能菜单", font=("Arial", 12, "bold")).pack()
    tk.Button(report_window, text="①日报", command=lambda: handle_option("1")).pack(fill="x")
    tk.Button(report_window, text="②月报", command=lambda: handle_option("2")).pack(fill="x")
    tk.Button(report_window, text="③报表设置", command=lambda: handle_option("3")).pack(fill="x")
    tk.Button(report_window, text="④返回上级菜单", command=lambda: handle_option("4")).pack(fill="x")

# 管理员登录
def login():
    attempt_count = 0
    login_window = tk.Toplevel(root)
    login_window.title("管理员登录")
    login_window.geometry("300x150")

    tk.Label(login_window, text="管理员账号：").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="管理员密码：").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def check_login():
        nonlocal attempt_count
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if hr.valid_user(username, password):
            ADMIN_LOGIN.set(True)
            messagebox.showinfo("登录成功", f"{username} 登录成功！")
            login_window.destroy()
        else:
            attempt_count += 1
            if attempt_count >= 3:
                messagebox.showerror("登录失败", "错误次数过多，已退出")
                login_window.destroy()
            else:
                messagebox.showerror("登录失败", f"账号或密码错误！剩余尝试次数：{3 - attempt_count}")

    tk.Button(login_window, text="登录", command=check_login).pack()


# 更新管理员账号
def update_admin_ui():
    if not ADMIN_LOGIN.get():
        messagebox.showerror("权限错误", "请先进行管理员登录")
        return

    update_window = tk.Toplevel(root)
    update_window.title("更新管理员账号")
    update_window.geometry("300x150")

    tk.Label(update_window, text="新管理员账号：").pack()
    new_username_entry = tk.Entry(update_window)
    new_username_entry.pack()

    tk.Label(update_window, text="新管理员密码：").pack()
    new_password_entry = tk.Entry(update_window, show="*")
    new_password_entry.pack()

    def handle_update():
        new_user = new_username_entry.get().strip()
        new_password = new_password_entry.get().strip()
        if not new_user or not new_password:
            messagebox.showerror("输入错误", "账号和密码不能为空！")
            return
        if update_admin(new_user, new_password):
            messagebox.showinfo("更新成功", "管理员账号已更新！")
            update_window.destroy()
        else:
            messagebox.showerror("更新失败", "更新管理员账号失败，请重试！")

    tk.Button(update_window, text="更新", command=handle_update).pack()


# 主窗口
root = tk.Tk()
ADMIN_LOGIN = tk.BooleanVar(value=False)
root.title("MR智能视频打卡系统")
root.geometry("400x400")

# 标题
tk.Label(root, text="MR智能视频打卡系统", font=("Arial", 16, "bold")).pack(pady=20)

# 主菜单按钮
tk.Button(root, text="①打卡", command=face_clock, width=30).pack(pady=2)
tk.Button(root, text="②查看记录", command=check_record, width=30).pack(pady=2)
tk.Button(root, text="③员工管理", command=employee_management, width=30).pack(pady=2)
tk.Button(root, text="④考勤报表", command=check_report, width=30).pack(pady=2)
tk.Button(root, text="⑤更新管理员账号", command=update_admin_ui, width=30).pack(pady=2)
tk.Button(root, text="管理员登录", command=login, width=30).pack(pady=2)
tk.Button(root, text="⑥退出", command=root.quit, width=30).pack(pady=20)

# 启动主循环
root.mainloop()