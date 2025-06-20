"""
程序主入口
提供人脸识别相关的服务，包括训练识别器、识别图像中的人脸等。

系统运行顺序：
如需成功打卡，需要先进入 ③员工管理 层下 ①录入新员工 录入成功后，才可在首页进行打卡
管理员密码请看 /data/user_password.txt的内容 {'mr': 'mrsoft', 'a': 's'} 账号为 a,密码为 s
操作步骤：
3 --- 1 --- (输入员工名字) --- (摄像头打开后)按三次enter键 (注①)--- "录入成功" --- 3 --- 1  #打卡完成

注①:如果弹出的摄像头在后台，就把窗口点出前台，按3次回车，如果没有反应
    把编译器窗口拖动至屏幕右边，窗口放在左边，点击窗口，再点击控制台，再点击窗口(玄学点击，反正要摄像头窗口在前台)
    见下方图片
"""

# 首先第一步导包，这里使用到了 util 文件夹下的 camera 和 public_tools 并改名为tool
# 以及service 文件下的 hr_service并改名为 hr(改名都是为了方便调包时的高可读性)
from util import camera
from util import public_tools as tool
from service import hr_service as hr

# 全局变量，默认管理员没有登录，保护数据安全
ADMIN_LOGIN = False  # 管理员登录状态

# 管理员登录
'''
实现:管理员登录三次限制
超过3次限制则退出系统，可添加退出系统锁定等功能
同时，在后续系统选项中，除 "打卡" 外的所有功能都需登录管理员账号
登录后，则变为管理员身份，可以实现所有功能
 ①打卡  ②查看记录  ③员工管理  ④考勤报表  ⑤退出
 ⑥管理员密码修改
'''


def login():
    global ADMIN_LOGIN  # 用global声明全局变量(在函数中，无法调用函数外的参数，需要用global声明)
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
            print(f"账号或密码错误，请重新输入！(还有{3 - attempt_count}次机会)")
            print("---------------------------")
            attempt_count += 1  # 尝试次数加1

    print("输入错误次数过多，已退出登录界面！")  # 超过3次尝试后提示并退出


'''
#原代码
def login():
    while True:
        username = input("请输入管理员账号(输入0取消操作)：")
        if username == "0":  # 如果只输入0
            return  # 结束方法
        passowrd = input("请输入管理员密码：")
        if hr.valid_user(username.strip(), passowrd.strip()):  # 校验账号密码
            global ADMIN_LOGIN  # 读取全局变量
            ADMIN_LOGIN = True  # 设置为管理员已登录状态
            print(username + "登录成功！请选择重新选择功能菜单")
            break
        else:
            print("账号或密码错误，请重新输入！")
            print("---------------------------")
'''

# 员工管理
'''
此功能需登录管理员账号后才能进入

录入新员工 在上方 "系统运行程序" 已详解，不赘述
删除员工: 输入员工前编号对应员工，输入随机生成的验证码( [] 中的四位数字即是验证码)，完成删除。
操作步骤： 3 --- a s(管理员账号密码)  --- 3 --- 2 --- 5(员工编号) --- 4432(随机验证码) --> 删除员工
'''


def employee_management():
    menu = """+-------------------------------------------------+
|                员工管理功能菜单                 |
+-------------------------------------------------+
  ①录入新员工  ②删除员工  ③返回上级菜单
---------------------------------------------------"""
    while True:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“录入新员工”
            name = str(input("请输入新员工姓名(输入0取消操作)：")).strip()
            if name != "0":  # 只要输入的不是0
                code = hr.add_new_employee(name)  # 人事服务添加新员工，并获得该员工的特征码
                print("请面对摄像头，敲击三次回车键完成拍照！")
                camera.register(code)  # 打开摄像头为员工照相
                print("录入成功！")
                # return  # 退出员工管理功能菜单
        elif option == "2":  # 如果选择“删除员工”
            # show_employee_all()  # 展示员工列表
            print(hr.get_employee_report())  # 打印员工信息报表
            id = int(input("请输入要删除的员工编号(输入0取消操作)："))
            if id > 0:  # 只要输入的不是0
                if hr.check_id(id):  # 若此编号有对应员工
                    verification = tool.randomNumber(4)  # 生成随机4位验证码
                    inputVer = input("[" + str(verification) + "] 请输入验证码：")  # 让用户输入验证码
                    if str(verification) == str(inputVer).strip():  # 如果验证码正确
                        hr.remove_employee(id)  # 人事服务删除该员工
                        print(str(id) + "号员工已删除！")
                    else:  # 无效编号
                        print("验证码有误，操作取消")
                else:
                    print("无此员工，操作取消")
        elif option == "3":  # 如果选择“返回上级菜单”
            return  # 退出员工管理功能菜单
        else:
            print("输入的指令有误，请重新输入！")


# 查看记录
'''
此功能仅简单调用 hr 中的 get_employee_report() 和 get_record_all() 函数
同时在 hr 中 调用 o.EMPLOYEES ,使用organizations中的 class Employee 员工类,
并使用 tool 中的 save_employee_all() 函数,
用于打开文件 /data/employee_data.txt 或 /data/lock_record.txt (员工列表/员工打卡记录)
'''


def check_record():
    menu = """+-------------------------------------------------+
|                 查看记录功能菜单                |
+-------------------------------------------------+
  ①查看员工列表  ②查看打卡记录  ③返回上级菜单
---------------------------------------------------"""
    while True:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“查看员工列表”
            print(hr.get_employee_report())  # 打印员工信息报表
        elif option == "2":  # 如果选择“查看打卡记录”
            report = hr.get_record_all()
            print(report)
        elif option == "3":  # 如果选择“返回上级菜单”
            return  # 退出查看记录功能菜单
        else:
            print("输入的指令有误，请重新输入！")


# 报表设置
# 这里各种调用,有注释不赘述
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
            # work_time 和 close_time是局部变量，作用域仅限于 report_config(),所以黄线警告无所谓

            print("设置完成，上班时间：" + work_time + ",下班时间为：" + close_time)
        elif option == "2":  # 如果选择“返回上级菜单”
            return  # 退出查看记录功能菜单
        else:
            print("输入的指令有误，请重新输入！")

'''
#原
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
            cont_online = 0
            cont_offline = 0
            while cont_online < 3:
                work_time = input("请设置上班时间，格式为(08:00:00)：")
                if tool.valid_time(work_time):  # 如果时间格式正确
                    break  # 结束循环
                else:  # 如果时间格式不对
                    print("上班时间格式错误，请重新输入")
                    cont_online += 1
            print("输入错误次数过多，已退出菜单！")
            while cont_offline  < 3:
                close_time = input("请设置下班时间，格式为(23:59:59)：")
                if tool.valid_time(close_time):  # 如果时间格式正确
                    break
                else:  # 如果时间格式不对
                    print("下班时间格式错误，请重新输入")
                    cont_offline += 1
            print("输入错误次数过多，已退出菜单！")
            hr.save_work_time(work_time, close_time)  # 保存用户设置的上班时间和下班时间
            print("设置完成，上班时间：" + work_time + ",下班时间为：" + close_time)
        elif option == "2":  # 如果选择“返回上级菜单”
            return  # 退出查看记录功能菜单
        else:
            print("输入的指令有误，请重新输入！")
'''


# 考勤报表
# 同上
def check_report():
    menu = """+-------------------------------------------------+
|                考勤报表功能菜单                 |
+-------------------------------------------------+
   ①日报  ②月报  ③报表设置  ④返回上级菜单
---------------------------------------------------"""
    while True:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“日报”
            while True:
                date = input("输入查询日期，格式为(2008-08-08),输入0则查询今天：")
                if date == "0":  # 如果只输入0
                    hr.get_today_report()  # 打印今天的日报
                    break  # 打印完之后结束循环
                elif tool.valid_date(date):  # 如果输入的日期格式有效
                    hr.get_day_report(date)  # 打印指定日期的日报
                    break  # 打印完之后结束循环
                else:  # 如果输入的日期格式无效
                    print("日期格式有误，请重新输入！")
        elif option == "2":  # 如果选择“月报”
            while True:
                date = input("输入查询月份，格式为(2008-08),输入0则查询上个月：")
                if date == "0":  # 如果只输入0
                    hr.get_pre_month_report()  # 生成上个月的月报
                    break  # 生成完毕之后结束循环
                elif tool.valid_year_month(date):  # 如果输入的月份格式有效
                    hr.get_month_report(date)  # 生成指定月份的月报
                    break  # 生成完毕之后结束循环
                else:
                    print("日期格式有误，请重新输入！")
        elif option == "3":  # 如果选择“报表设置”
            report_config()  # 进入“报表设置”菜单
        elif option == "4":  # 如果选择“返回上级菜单”
            return  # 退出查看记录功能菜单
        else:
            print("输入的指令有误，请重新输入！")


# 人脸打卡
# 调用 /data/camera 的 clock_in() 方法
def face_clock():
    print("请正面对准摄像头进行打卡")
    name = camera.clock_in()  # 开启摄像头，返回打卡员工名称
    if name is not None:  # 如果员工名称有效
        hr.add_lock_record(name)  # 保存打卡记录
        print(name + " 打卡成功！")


# 管理员密码修改
'''
用 strip()方法去除输入的多余空格，确保输入的账号和密码干净,
调用 /servers/hr 的valid_user() 方法验证用户输入的旧账号和密码是否正确
同时，在 hr 中使用 o.USERS 读取 /entity/organizations  中 当前管理员的账号密码
'''


def change_admin_password():
    print("+--------------------------------------------------+")
    print("|              管理员密码修改界面                  |")
    print("+--------------------------------------------------+")

    # 1. 输入旧账号密码
    # 使用 strip()方法去除输入的多余空格，确保输入的账号和密码干净
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
    if hr.update_admin(new_user, new_pass):
        print("管理员账号密码修改成功！")
    else:
        print("修改失败，请检查系统状态")


# 启动方法
'''
除 "打卡" 外的所有功能都需登录管理员账号
登录后，则变为管理员身份，可以实现所有功能
'''


def start():
    finish = False  # 程序结束标志
    menu = """
+--------------------------------------------------+
|                   主功能菜单                     |
+--------------------------------------------------+
 ①打卡  ②查看记录  ③员工管理  ④考勤报表  ⑤退出
 ⑥管理员密码修改
---------------------------------------------------"""
    while not finish:
        print(menu)  # 打印菜单
        option = input("请输入菜单序号：")
        if option == "1":  # 如果选择“打卡”
            face_clock()  # 启动人脸打卡
        elif option == "2":  # 如果选择“查看记录”
            if ADMIN_LOGIN:  # 如果管理员已登录
                check_record()  # 进入查看记录方法
            else:
                login()  # 先让管理员登录
        elif option == "3":  # 如果选择“员工管理”
            if ADMIN_LOGIN:
                employee_management()  # 进入员工管理方法
            else:
                login()
        elif option == "4":  # 如果选择“考勤报表”
            if ADMIN_LOGIN:
                check_report()  # 进入考勤报表方法
            else:
                login()
        elif option == "5":  # 如果选择“退出”
            finish = True  # 确认结束，循环停止
        elif option == "6":
            if ADMIN_LOGIN:
                change_admin_password()
            else:
                login()
        else:
            print("输入的指令有误，请重新输入！")
    print("Bye Bye !")


hr.load_emp_data()  # 数据初始化
tital = """
***************************************************
*                MR智能视频打卡系统               *
***************************************************"""
print(tital)  # 打印标题
start()  # 启动程序
