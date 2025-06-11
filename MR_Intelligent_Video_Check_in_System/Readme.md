## # Clock 人脸识别打卡考勤系统

## 📌 项目简介

本项目是一个基于 OpenCV 和 Python 实现的人脸识别考勤打卡系统。管理员可以管理员工信息，员工通过摄像头识别人脸，实现上下班打卡。数据存储基于本地文件。

##  项目结构

```
clock/
 ├── main.py                       # 主入口程序
 ├── test.py                       # 模拟测试脚本
 ├── entity/
 │   └── organizations.py          # 组织结构定义
 ├── service/
 │   ├── hr_service.py             # 人事管理模块
 │   └── recognize_service.py      # 人脸识别模块
 ├── util/
 │   ├── camera.py                 # 摄像头操作工具
 │   └── public_tools.py           # 通用工具
 ├── cascades/
 │   └── haarcascade_frontalface_default.xml  # OpenCV 人脸识别模型
 ├── data/
 │   ├── employee_data.txt         # 员工信息
 │   ├── user_password.txt         # 管理员账号密码
 │   ├── work_time.txt             # 上下班时间设定
 │   ├── lock_record.txt           # 打卡记录
 │   └── faces/                    # 员工人脸图像数据
 ├── UI.py                         # UI版本
 └── requirements.txt              # 所需依赖库
```



## 各文件解析

### ✅ `main.py`

**功能：系统主入口**

- 控制台启动页，提供功能菜单（打卡、记录、员工管理、报表、修改密码等）
- 调用各模块实现逻辑，用户通过键盘交互操作系统

🔧 **注释建议：**

- 每个菜单项后添加对应功能的模块路径说明
- `login()` 函数处补充管理员验证逻辑的流程说明

------

### ✅ `UI.py`

**功能：图形界面模块**

- 使用 `tkinter` 创建 UI 界面
- 包含“人脸打卡”、“员工管理”等按钮，并集成已有功能
- 使用多线程防止界面卡顿

🔧 **注释建议：**

- 各 UI 控件的创建位置加注释（如 `face_clock()` 按钮对应哪个功能）
- 明确线程使用目的（UI不卡死）

------

### ✅ `service/hr_service.py`

**功能：员工管理服务**

- 加载/保存员工数据
- 添加/删除员工
- 验证管理员账号
- 管理打卡记录和考勤报表

------

### ✅ `service/recognize_service.py`

**功能：人脸识别服务**

- 加载人脸识别模型（LBPH）
- 识别人脸并返回 ID
- 训练识别模型

- 模型训练部分说明保存路径、
- `predict()` 函数说明如何处理匹配不成功情况

------

### ✅ `util/camera.py`

**功能：摄像头工具类**

- 打开摄像头
- 拍摄人脸图像
- 录入图像文件用于训练

------

### ✅ `util/io_tools.py`

**功能：文件读写操作**

- 封装通用文件读取、保存功能

------

### ✅ `util/public_tools.py`

**功能：辅助工具集**

- 获取时间、员工编号生成、路径拼接等小工具

------

### ✅ `entity/organizations.py`

**功能：定义组织类结构**

- `Employee` 员工类
- 可能包含工号、姓名、组织编号等字段





## 使用方法

### 1. 安装依赖

pip install -r requirements.txt

### 2. 运行程序

```bash
python main.py  #运行控制台版本
python UI.py  #运行 UI 版本
```

### 3. 功能说明

- 📷 打开摄像头自动识别人脸
- ✅ 成功识别后自动记录打卡时间
- 🔒 管理员可登录查看员工信息和打卡记录
- 📝 所有数据以文本文件形式保存在 `data/` 目录中

------

## 🛠 技术栈

- Python 3.8
- OpenCV (cv2)
- Numpy

------

## 📌 注意事项

- 请确保摄像头正常工作
- 建议在光线良好的环境中使用以提升识别精度
- 运行目录应保持结构完整，尤其是 `cascades/` 和 `data/faces/`

------



## 🧩 功能添加

- 管理员登录次数限制(使用global局部变量读全局变量ADMIN_LOGIN)
- 作息时间设置栏设计可退出选项(Y/N)
- 使用 Tkinter，增加图形化界面（UI）支持
- 管理员密码修改/管理员账号添加

# 功能实现：

# main.py

## 管理员登录次数限制为3次

```python
# login方法 
def login():
    global ADMIN_LOGIN  # 读取全局变量
    attempt_count = 0  # 初始化尝试次数计数器

    while attempt_count < 3:  # 限制最多尝试3次
        username = input("请输入管理员账号(输入0取消操作)：")
        if username == "0":  # 如果只输入0
            return  # 结束方法
        password = input("请输入管理员密码：")
        if hr.valid_user(username.strip(), password.strip()):  # 校验账号密码
            ADMIN_LOGIN = True  # 设置为管理员已登录状态
            print(username + "登录成功！请选择重新选择功能菜单")
            return  # 登录成功，退出登录函数
        else:
            print(f"账号或密码错误，请重新输入！(还有{3-attempt_count}次机会)")
            print("---------------------------")
            attempt_count += 1  # 尝试次数加1

    print("输入错误次数过多，已退出登录界面！")  # 超过3次尝试后提示并退出
```



## 作息时间设置栏设计可退出选项(Y/N)

```python
# report_config()方法
def report_config():
    menu = """+-------------------------------------------------+
|                报表设置功能菜单                 |
+-------------------------------------------------+
①作息时间设置  ②返回上级菜单
---------------------------------------------------"""
    while True:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“作息时间设置”
            cont_online = 0  # 上班时间输入错误计数
            cont_offline = 0  # 下班时间输入错误计数

            # 设置上班时间
            while cont_online < 3:
                work_time = input("请设置上班时间，格式为(08:00:00)：")
                if tool.valid_time(work_time):  # 如果时间格式正确
                    break  # 结束循环
                else:  # 如果时间格式不对
                    print("上班时间格式错误，请重新输入")
                    cont_online += 1
                    if cont_online == 3:  # 如果错误次数达到3次
                        exit_option = input("输入错误次数过多，是否退出当前时间设置？(Y/N)：").strip().lower()
                        if exit_option == 'y':  # 如果用户选择退出
                            print("已退出当前时间设置")
                            return  # 退出当前时间设置
                        elif exit_option == 'n':  # 如果用户选择继续
                            cont_online = 0  # 重置尝试次数
                        else:
                            print("无效选项，继续尝试输入上班时间")

            # 设置下班时间
            while cont_offline < 3:
                close_time = input("请设置下班时间，格式为(23:59:59)：")
                if tool.valid_time(close_time):  # 如果时间格式正确
                    break
                else:  # 如果时间格式不对
                    print("下班时间格式错误，请重新输入")
                    cont_offline += 1
                    if cont_offline == 3:  # 如果错误次数达到3次
                        exit_option = input("输入错误次数过多，是否退出当前时间设置？(Y/N)：").strip().lower()
                        if exit_option == 'y':  # 如果用户选择退出
                            print("已退出当前时间设置")
                            return  # 退出当前时间设置
                        elif exit_option == 'n':  # 如果用户选择继续
                            cont_offline = 0  # 重置尝试次数
                        else:
                            print("无效选项，继续尝试输入下班时间")

            # 保存设置的时间
            hr.save_work_time(work_time, close_time)  # 保存用户设置的上班时间和下班时间
            print("设置完成，上班时间：" + work_time + ",下班时间为：" + close_time)
        elif option == "2":  # 如果选择“返回上级菜单”
            return  # 退出查看记录功能菜单
        else:
            print("输入的指令有误，请重新输入！")
```



## 管理员密码修改/管理员账号添加

```python
# change_admin_password()
# 使用字典的update()方法对user_password.txt的字典进行修改
# 同key(账号)，改value(密码)；反之key:value
def change_admin_password():
    print("+--------------------------------------------------+")
    print("|              管理员密码修改界面                  |")
    print("+--------------------------------------------------+")

    # 1. 输入旧账号密码
    old_user = input("请输入当前管理员账号：").strip()
    old_pass = input("请输入当前管理员密码：").strip()

    if not hr.valid_user(old_user, old_pass):
        print("账号或密码错误，无法修改")
        return

    # 2. 输入新账号新密码
    new_user = input("请输入新的管理员账号(只改密码请输入原账号)：").strip()
    new_pass = input("请输入新的管理员密码：").strip()
    confirm_pass = input("请再次输入新的管理员密码：").strip()

    # 3. 验证一致性
    if new_pass != confirm_pass:
        print("两次输入的新密码不一致，修改失败")
        return

    # 4. 更新管理员信息
    # if hr.update_admin(new_user, new_pass):
    if hr.update_admin(new_user,new_pass):
        print("管理员账号密码修改成功！")
    else:
        print("修改失败，请检查系统状态")
```



# UI.py

## 管理员登录次数限制为3次

```python
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
```



## 作息时间可退出选项(Y/N)

```python
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
```



## 管理员密码修改/管理员账号添加

```python
def update_admin_ui():
    if not ADMIN_LOGIN.get():
        messagebox.showerror("权限错误", "请先进行管理员登录")
        return

    update_window = tk.Toplevel(root)
    update_window.title("更新管理员账号")
    update_window.geometry("300x150")

    tk.Label(update_window, text="新管理员账号(只改密码请输入原账号)：").pack()
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
```



