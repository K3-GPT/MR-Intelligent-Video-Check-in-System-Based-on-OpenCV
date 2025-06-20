"""
重要！
人事管理服务
提供人事管理相关的服务，包括员工管理、打卡记录管理、报表生成等

在 main 和 UI 中添加方法的同时，也需要在本文件中添加对应的方法

员工增删:
添加新员工: add_new_employee() 为新员工生成一个随机特征码，创建员工对象并保存到组织结构中，同时更新员工信息文件
删除员工: remove_employee()   删除指定员工的图片、从组织结构中移除员工，并更新员工信息和打卡记录文件

打卡记录管理:
获取打卡记录: get_record_all() 遍历所有员工的打卡记录，生成一个包含所有打卡时间的报表
添加打卡记录: add_lock_record()
    基础版:直接将当前时间添加到打卡记录中
    进阶版:判断打卡时间是否在上班或下班时间内，并避免重复打卡(未完整实现)

生成打卡日报: get_today_report(), get_day_report()      根据指定日期（默认为当天），生成包含迟到、早退、缺席等信息的打卡日报
生成打卡月报: get_pre_month_report(),get_month_report() 生成指定月份的打卡月报，以CSV文件格式保存，包含每天的打卡情况（如迟到、早退、缺席等）

管理员管理:
验证管理员账号和密码: valid_user()    检查输入的管理员账号和密码是否匹配
更新管理员账号和密码: update_admin()  更新管理员账号和密码，并将新的信息保存到文件中

报表生成:
员工信息报表: get_employee_report()  生成包含所有员工信息的报表，格式化输出员工名单
打卡记录报表: get_record_all()       生成包含所有员工打卡记录的报表

辅助功能:
通过特征码获取员工姓名: get_name_with_code()  根据员工特征码查找对应的员工姓名
通过ID获取员工特征码: get_code_with_id()     根据员工ID查找对应的员工特征码
检查ID是否存在: check_id()        检查指定的员工ID是否存在于系统中
保存上下班时间: save_work_time()  更新并保存上下班时间配置
加载数据: load_emp_data()        加载管理员账号、打卡记录、员工信息、员工照片等数据

数据结构:
员工信息: o.EMPLOYEES()                        存储所有员工的详细信息，包括ID、姓名、特征码等
打卡记录: o.LOCK_RECORD()                      存储员工的打卡记录，以字典形式保存，键为员工姓名，值为打卡时间列表
管理员账号信息: o.USERS()                       存储管理员账号和密码的映射关系
上下班时间配置: o.WORK_TIME() o.CLOSING_TIME()  存储系统中设置的上班时间和下班时间

文件操作:
保存员工信息: io.save_employee_all()              将员工信息保存到文件中
保存打卡记录: io.save_lock_record()               将打卡记录保存到文件中
保存管理员账号: io.save_users()                   将管理员账号和密码保存到文件中
保存上下班时间配置: io.save_work_time_config()     将上下班时间保存到文件中
生成CSV文件: io.create_CSV()                     将打卡月报以CSV格式保存到文件中

功能流程:
系统启动时加载数据: load_emp_data()   系统启动时，加载管理员账号、打卡记录、员工信息等数据
员工管理:
   - 添加新员工时，生成随机特征码并保存信息
   - 删除员工时，清除相关数据并更新文件
打卡管理:
   - 员工打卡时，根据时间判断是上班打卡还是下班打卡，并记录当前时间
   - 生成打卡日报和月报，统计迟到、早退、缺席等情况
管理员管理:
   - 验证管理员账号和密码
   - 更新管理员账号和密码
报表生成:
   - 生成员工信息报表和打卡记录报表
   - 生成打卡日报和月报，以文本或CSV格式输出
"""

from entity import organizations as o
from util import public_tools as tool
from util import io_tools as io
import datetime
import calendar



# 添加新员工
def add_new_employee(name):
    code = tool.randomCode()  # 生成随机特征码
    newEmp = o.Employee(o.get_new_id(), name, code)  # 创建员工对象
    o.add(newEmp)  # 组织结构中添加新员工
    io.save_employee_all()  # 保存最新的员工信息
    return code  # 新员工的特征码


# 删除某个员工
def remove_employee(id):
    io.remove_pics(id)  # 删除该员工所有图片
    o.remove(id)  # 从组织结构中删除
    io.save_employee_all()  # 保存最新的员工信息
    io.save_lock_record()  # 保存最新的打卡记录


# 所有员工信息报表
def get_employee_report():
    # report = list()   # 员工信息列表
    report = "###########################################\n"
    report += "员工名单如下：\n"
    i = 0  # 换行计数器
    for emp in o.EMPLOYEES:  # 遍历所有员工
        report += "(" + str(emp.id) + ")" + emp.name + "\t"
        i += 1  # 计数器自增
        if i == 4:  # 每四个员工换一行
            report += "\n"
            i = 0  # 计数器归零
    report = report.strip()  # 清除报表结尾可能出现的换行符
    report += "\n###########################################"
    return report


# 通过特征码获取员工姓名
def get_name_with_code(code):
    for emp in o.EMPLOYEES:
        if str(code) == str(emp.code):
            return emp.name


# 通过id获取员工特征码
def get_code_with_id(id):
    for emp in o.EMPLOYEES:
        if str(id) == str(emp.id):
            return emp.code


# 获取所有员工的打卡记录信息
def get_record_all():
    record = o.LOCK_RECORD  # 获得打卡记录字典
    report = ""  # 报表内容
    for name in record.keys():  # 遍历所有名字
        report += "-----------------------------------\n"
        report += name + "  打卡记录如下：\n"
        for date in record[name]:  # 遍历所有时间字符串
            report += date + "\n"
    return report


# 为指定员工添加打卡记录
# 列表法

def add_lock_record(name):
    record = o.LOCK_RECORD  # 所有打卡记录
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 当前时间
    if name in record.keys():  # 如果这个人有打卡记录
        r_list = record[name]  # 去除他的记录
        if len(r_list) == 0:  # 如果记录为空
            r_list = list()  # 创建新列表
        r_list.append(now_time)  # 记录当前时间
    else:  # 如果这个人从未打过卡
        r_list = list()  # 创建新列表
        r_list.append(now_time)  # 记录当前时间
        record[name] = r_list  # 将记录保存在字典中
    io.save_lock_record()  # 保存所有打卡记录

#打卡进阶功能(未实现)
'''
def add_lock_record(name):
    record = o.LOCK_RECORD  # 所有打卡记录
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")  # 当前时间完整字符串
    today_str = now.strftime("%Y-%m-%d")         # 当前日期
    now_time = now.time()

    # 上下班时间
    work_time = datetime.datetime.strptime(o.WORK_TIME, "%H:%M:%S").time()
    close_time = datetime.datetime.strptime(o.CLOSE_TIME, "%H:%M:%S").time()

    # 获取该员工的历史打卡记录
    if name not in record:
        record[name] = []

    today_clock_list = [t for t in record[name] if today_str in t]  # 只取今天的记录

    # 判断今天是否已打上班卡或下班卡
    has_on = False
    has_off = False
    for t in today_clock_list:
        time_obj = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S").time()
        if time_obj <= datetime.time(12, 0):
            has_on = True
        else:
            has_off = True

    # 根据时间判断是否记录上班或下班打卡
    if now_time <= datetime.time(12, 0):
        if not has_on:
            record[name].append(now_str)
        else:
            print(f"{name} 今天已打过上班卡")
    else:
        if not has_off:
            record[name].append(now_str)
        else:
            print(f"{name} 今天已打过下班卡")

    io.save_lock_record()  # 保存所有打卡记录
'''

# 验证管理员账号和密码
def valid_user(username, password):
    if username in o.USERS.keys():  # 如果有这个账号
        if o.USERS.get(username) == password:  # 如果账号和密码匹配
            return True  # 验证成功
    return False  # 验证失败

# 管理员密码修改
def update_admin(new_user, new_password):
    # 读取当前管理员账号和密码
    users = o.USERS
    users[new_user] = new_password  # 更新管理员账号和密码
    # 将新的管理员账号和密码写入文件
    with open(io.USER_PASSWORD, "w", encoding="utf-8") as file:
        file.write(str(users))  # 将字典转换为字符串并写入文件
    return True


# 打印今天的打卡日报
def get_today_report():
    date = datetime.datetime.now().strftime("%Y-%m-%d")  # 今天的日期
    get_day_report(str(date))  # 打印今天的日报


# 打印指定日期的打卡日报
def get_day_report(date):
    io.load_work_time_config()  # 读取上下班时间

    earliest_time = datetime.datetime.strptime(date + " 00:00:00", "%Y-%m-%d %H:%M:%S")  # 今天0点
    noon_time = datetime.datetime.strptime(date + " 12:00:00", "%Y-%m-%d %H:%M:%S")  # 今天中午12点
    latest_time = datetime.datetime.strptime(date + " 23:59:59", "%Y-%m-%d %H:%M:%S")  # 今晚0点之前
    work_time = datetime.datetime.strptime(date + " " + o.WORK_TIME, "%Y-%m-%d %H:%M:%S")  # 上班时间
    closing_time = datetime.datetime.strptime(date + " " + o.CLOSING_TIME, "%Y-%m-%d %H:%M:%S")  # 下班时间

    late_list = []  # 迟到名单
    left_early = []  # 早退名单
    absent_list = []  # 缺席名单

    for emp in o.EMPLOYEES:  # 遍历所有员工
        if emp.name in o.LOCK_RECORD.keys():  # 如果该员工有打卡记录
            emp_lock_list = o.LOCK_RECORD.get(emp.name)  # 获取该员工所有的打卡记录
            is_absent = True  # 缺席状态
            for lock_time_str in emp_lock_list:  # 遍历所有打卡记录
                lock_time = datetime.datetime.strptime(lock_time_str, "%Y-%m-%d %H:%M:%S")  # 打卡记录转为日期格式
                if earliest_time < lock_time < latest_time:  # 如果当天有打卡记录
                    is_absent = False  # 不缺席
                    if work_time < lock_time <= noon_time:  # 上班时间后、中午之前打卡
                        late_list.append(emp.name)  # 加入迟到名单
                    if noon_time < lock_time < closing_time:  # 中午之后、下班之前打卡
                        left_early.append(emp.name)  # 加入早退名单
            if is_absent:  # 如果仍然是缺席状态
                absent_list.append(emp.name)  # 加入缺席名单
        else:  # 该员工没有打卡记录
            absent_list.append(emp.name)  # 加入缺席名单

    emp_count = len(o.EMPLOYEES)  # 员工总人数
    print("--------" + date + "--------")
    print("应到人数：" + str(emp_count))
    print("缺席人数：" + str(len(absent_list)))
    absent_name = ""  # 缺席名单
    if len(absent_list) == 0:  # 如果没有缺席的
        absent_name = "(空)"
    else:  # 有缺席的
        for name in absent_list:  # 遍历缺席列表
            absent_name += name + " "  # 拼接名字
    print("缺席名单：" + absent_name)
    print("迟到人数：" + str(len(late_list)))
    late_name = ""  # 迟到名单
    if len(late_list) == 0:  # 如果没有迟到的
        late_name = "(空)"
    else:  # 有迟到的
        for name in late_list:  # 遍历迟到列表
            late_name += name + " "  # 拼接名字
    print("迟到名单：" + str(late_name))
    print("早退人数：" + str(len(left_early)))
    early_name = ""  # 早退名单
    if len(left_early) == 0:  # 如果没有早退的
        early_name = "(空)"
    else:  # 有早退的
        for name in left_early:  # 遍历早退列表
            early_name += name + " "  # 拼接名字
    print("早退名单：" + early_name)


def is_within_time_range(start_time, end_time, current_time):
    # 将时间字符串转换为datetime对象
    start = datetime.strptime(start_time, "%H:%M:%S")
    end = datetime.strptime(end_time, "%H:%M:%S")
    now = datetime.strptime(current_time, "%H:%M:%S")
    return start <= now <= end
# 创建上个月打卡记录月报
def get_pre_month_report():
    today = datetime.date.today()  # 得到今天的日期
    pre_month_first_day = datetime.date(today.year, today.month - 1, 1)  # 获得上个月的第一天的日期
    pre_month = pre_month_first_day.strftime("%Y-%m")  # 转成年月格式字符串
    get_month_report(pre_month)  # 生成上个月的月报


# 创建指定月份的打卡记录月报
def get_month_report(month):
    io.load_work_time_config()  # 读取上下班时间
    date = datetime.datetime.strptime(month, "%Y-%m")  # 月份转为时间对象
    monthRange = calendar.monthrange(date.year, date.month)[1]  # 该月最后一天的天数
    month_first_day = datetime.date(date.year, date.month, 1)  # 该月的第一天
    month_last_day = datetime.date(date.year, date.month, monthRange)  # 该月的最后一天

    clock_in = "I"  # 正常上班打卡标志
    clock_out = "O"  # 正常下班打卡标志
    late = "L"  # 迟到标志
    left_early = "E"  # 早退标志
    absent = "A"  # 缺席标志

    lock_report = dict()  # 键为员工名，值为员工打卡情况列表

    for emp in o.EMPLOYEES:
        emp_lock_data = []  # 员工打卡情况列表
        if emp.name in o.LOCK_RECORD.keys():  # 如果员工有打卡记录
            emp_lock_list = o.LOCK_RECORD.get(emp.name)  # 从打卡记录中获取该员工的记录
            index_day = month_first_day  # 遍历日期，从该月第一天开始
            while index_day <= month_last_day:
                is_absent = True  # 缺席状态
                earliest_time = datetime.datetime.strptime(str(index_day) + " 00:00:00", "%Y-%m-%d %H:%M:%S")  # 当天0点
                noon_time = datetime.datetime.strptime(str(index_day) + " 12:00:00", "%Y-%m-%d %H:%M:%S")  # 当天中午12点
                latest_time = datetime.datetime.strptime(str(index_day) + " 23:59:59", "%Y-%m-%d %H:%M:%S")  # 当天0点之前
                work_time = datetime.datetime.strptime(str(index_day) + " " + o.WORK_TIME,
                                                       "%Y-%m-%d %H:%M:%S")  # 当天上班时间
                closing_time = datetime.datetime.strptime(str(index_day) + " "
                                                          + o.CLOSING_TIME, "%Y-%m-%d %H:%M:%S")  # 当天下班时间
                emp_today_data = ""  # 员工打卡标记汇总

                for lock_time_str in emp_lock_list:  # 遍历所有打卡记录
                    lock_time = datetime.datetime.strptime(lock_time_str, "%Y-%m-%d %H:%M:%S")  # 打卡记录转为日期格式
                    if earliest_time < lock_time < latest_time:  # 如果当前日期有打卡记录
                        is_absent = False  # 不缺席
                        if lock_time <= work_time:  # 上班时间前打卡
                            emp_today_data += clock_in  # 追加正常上班打卡标志
                        elif lock_time >= closing_time:  # 下班时间后打卡
                            emp_today_data += clock_out  # 追加正常下班打卡标志
                        elif work_time < lock_time <= noon_time:  # 上班时间后、中午之前打卡
                            emp_today_data += late  # 追加迟到标志
                        elif noon_time < lock_time < closing_time:  # 中午之后、下班之前打卡
                            emp_today_data += left_early  # 追加早退标志
                if is_absent:  # 如果缺席
                    emp_today_data = absent  # 直接赋予缺席标志
                emp_lock_data.append(emp_today_data)  # 员工打卡标记添加到打卡情况列表中
                index_day = index_day + datetime.timedelta(days=1)  # 遍历天数递增
        else:  # 没有打卡记录的员工
            index_day = month_first_day  # 从该月第一天开始
            while index_day <= month_last_day:  # 遍历整月
                emp_lock_data.append(absent)  # 每天都缺席
                index_day = index_day + datetime.timedelta(days=1)  # 日期递增
        lock_report[emp.name] = emp_lock_data  # 将打卡情况列表保存到该员工之下

    report = "\"姓名/日期\""  # cvs文件的文本内容，第一行第一列
    index_day = month_first_day  # 从该月第一天开始
    while index_day <= month_last_day:  # 遍历整月
        report += ",\"" + str(index_day) + "\""  # 添加每一天的日期
        index_day = index_day + datetime.timedelta(days=1)  # 日期递增
    report += "\n"

    for emp in lock_report.keys():  # 遍历报表中的所有员工
        report += "\"" + emp + "\""  # 第一列为员工名
        data_list = lock_report.get(emp)  # 取出员工的打卡情况列表
        for data in data_list:  # 取出每一天的打卡情况
            text = ""  # CSV中显示的内容
            if absent == data:  # 如果是缺席
                text = "【缺席】"
            elif clock_in in data and clock_out in data:  # 如果是全勤，不考虑迟到和早退
                text = ""  # 显示空白
            else:  # 如果不是全勤
                if late in data and clock_in not in data:  # 有迟到记录且无上班打卡
                    text += "【迟到】"
                if left_early in data and clock_out not in data:  # 有早退记录且无下班打卡
                    text += "【早退】"
                if clock_out not in data and left_early not in data:  # 无下班打卡和早退记录
                    text += "【下班未打卡】"
                if clock_in not in data and late not in data:  # 有无上班打卡和迟到记录
                    text += "【上班未打卡】"
            report += ",\"" + text + "\""
        report += "\n"

    title_date = month_first_day.strftime("%Y{y}%m{m}").format(y="年", m="月")  # csv文件标题日期
    file_name = title_date + "考勤月报"  # CSV的文件名
    io.create_CSV(file_name, report)  # 生成csv文件


# 检查id是否存在
def check_id(id):
    for emp in o.EMPLOYEES:
        if str(id) == str(emp.id):
            return True
    return False


# 保存上下班时间
def save_work_time(work_time, close_time):
    o.WORK_TIME = work_time
    o.CLOSING_TIME = close_time
    io.save_work_time_config()  # 上下班时间保存到文件中


# 加载数据
def load_emp_data():
    io.checking_data_files()  # 文件自检
    io.load_users()  # 载入管理员账号
    io.load_lock_record()  # 载入打卡记录
    io.load_employee_info()  # 载入员工信息
    io.load_employee_pic()  # 载入员工照片

