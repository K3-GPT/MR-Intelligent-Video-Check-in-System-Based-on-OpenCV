## # Clock 人脸识别打卡考勤系统

## 📌 项目简介

本项目是一个基于 OpenCV 和 Python 实现的人脸识别考勤打卡系统。管理员可以管理员工信息，员工通过摄像头识别人脸，实现上下班打卡。数据存储基于本地文件。

##  项目结构

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
 └── requirements.txt              # 所需依赖库



## 使用方法

### 1. 安装依赖

pip install -r requirements.txt

### 2. 运行程序

```bash
python main.py
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
- 管理员登录次数限制
- 使用 Tkinter，增加图形化界面（UI）支持
- 检测用户迟到或未打卡(弹窗提示)

存在问题：

打卡时间窗口展现

打卡时间冲突













# 添加功能：

## 管理员登录次数限制为3次(main.py)


