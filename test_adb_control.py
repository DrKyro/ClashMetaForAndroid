#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClashMetaForAndroid ADB 测试脚本 (Python版本)
用于测试 ClashMetaForAndroid 的 ADB 控制功能
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# 配置参数
CONFIG_FILE = "socks5_config.yaml"
# 使用应用的外部存储目录，避免权限问题
DEVICE_CONFIG_PATH = "/sdcard/Android/data/{package_name}/files/socks5_config.yaml"
# 支持多个构建变体的包名
PACKAGE_VARIANTS = [
    "com.github.metacubex.clash.alpha",  # Alpha 版本
    "com.github.metacubex.clash.meta"     # Meta 版本
]
ACTIVITY_NAME = "{package_name}/com.github.kr328.clash.ExternalControlActivity"

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """打印标题"""
    print(f"{Colors.HEADER}{text}{Colors.ENDC}")

def print_success(text):
    """打印成功信息"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """打印错误信息"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    """打印信息"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def run_adb_command(command, check_result=True):
    """执行 ADB 命令"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check_result,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except Exception as e:
        return False, "", str(e)

def check_adb_available():
    """检查 ADB 是否可用"""
    success, _, _ = run_adb_command("adb version", False)
    if not success:
        print_error("ADB 未找到或无法运行，请确保已安装 Android SDK 并将 ADB 添加到 PATH")
        return False
    return True

def detect_package_name():
    """检测设备上安装的包名"""
    for package in PACKAGE_VARIANTS:
        success, output, _ = run_adb_command(f"adb shell pm list packages {package}", False)
        if success and package in output:
            print_success(f"检测到已安装的包: {package}")
            return package
    
    # 如果都没有找到，使用第一个作为默认
    print_warning(f"未检测到已安装的包，使用默认包名: {PACKAGE_VARIANTS[0]}")
    return PACKAGE_VARIANTS[0]

def check_device_connected():
    """检查设备是否连接"""
    success, output, _ = run_adb_command("adb devices", False)
    if not success or "device" not in output:
        print_error("未找到已连接的 Android 设备，请确保设备已连接并启用 USB 调试")
        return False
    return True

def upload_config_file(package_name):
    """上传配置文件到设备"""
    device_path = DEVICE_CONFIG_PATH.format(package_name=package_name)
    print_info(f"正在上传配置文件到设备 (包名: {package_name})...")
    
    if not os.path.exists(CONFIG_FILE):
        print_error(f"配置文件 {CONFIG_FILE} 不存在")
        return False
    
    # 确保目标目录存在
    dir_path = os.path.dirname(device_path)
    run_adb_command(f"adb shell mkdir -p {dir_path}", False)
    
    success, _, error = run_adb_command(f"adb push {CONFIG_FILE} {device_path}")
    if success:
        print_success(f"配置文件上传成功: {device_path}")
        return True, device_path
    else:
        print_error(f"配置文件上传失败: {error}")
        return False, None

def switch_to_config(package_name, config_path):
    """切换到指定的配置文件"""
    print_info(f"正在切换到本地配置文件 (包名: {package_name})...")
    
    activity_name = ACTIVITY_NAME.format(package_name=package_name)
    command = f'adb shell am start -a {package_name}.action.SWITCH_TO_CONFIG --es config_path "{config_path}" {activity_name}'
    success, _, error = run_adb_command(command)
    if success:
        print_success("配置切换命令已发送")
        print_info("请在设备上确认配置切换是否成功")
        return True
    else:
        print_error(f"配置切换失败: {error}")
        return False

def start_clash(package_name):
    """启动代理服务"""
    print_info(f"正在启动代理服务 (包名: {package_name})...")
    
    activity_name = ACTIVITY_NAME.format(package_name=package_name)
    command = f'adb shell am start -a {package_name}.action.START_CLASH {activity_name}'
    success, _, error = run_adb_command(command)
    if success:
        print_success("代理启动命令已发送")
        return True
    else:
        print_error(f"代理启动失败: {error}")
        return False

def stop_clash(package_name):
    """停止代理服务"""
    print_info(f"正在停止代理服务 (包名: {package_name})...")
    
    activity_name = ACTIVITY_NAME.format(package_name=package_name)
    command = f'adb shell am start -a {package_name}.action.STOP_CLASH {activity_name}'
    success, _, error = run_adb_command(command)
    if success:
        print_success("代理停止命令已发送")
        return True
    else:
        print_error(f"代理停止失败: {error}")
        return False

def toggle_clash(package_name):
    """切换代理状态"""
    print_info(f"正在切换代理状态 (包名: {package_name})...")
    
    activity_name = ACTIVITY_NAME.format(package_name=package_name)
    command = f'adb shell am start -a {package_name}.action.TOGGLE_CLASH {activity_name}'
    success, _, error = run_adb_command(command)
    if success:
        print_success("代理状态切换命令已发送")
        return True
    else:
        print_error(f"代理状态切换失败: {error}")
        return False

def show_test_info():
    """显示测试信息"""
    print("\n" + "="*50)
    print_header("ClashMetaForAndroid ADB 控制测试")
    print("="*50)
    print()
    
    print_info("测试步骤:")
    print("1. 上传配置文件到设备")
    print("2. 切换到上传的配置文件")
    print("3. 启动代理服务")
    print("4. 显示测试完成后的操作选项")
    print()

def show_post_test_options(package_name):
    """显示测试完成后的操作选项"""
    activity_name = ACTIVITY_NAME.format(package_name=package_name)
    print("\n" + "="*50)
    print_header("测试完成后的操作选项")
    print("="*50)
    print()
    print_info("手动测试命令:")
    print(f"停止代理: adb shell am start -a {package_name}.action.STOP_CLASH {activity_name}")
    print(f"切换代理状态: adb shell am start -a {package_name}.action.TOGGLE_CLASH {activity_name}")
    print()
    print_info("检查代理是否正常工作:")
    print("curl -x socks5://127.0.0.1:7891 http://www.google.com")
    print()


def main():
    """主函数"""
    show_test_info()
    
    # 检查 ADB 是否可用
    if not check_adb_available():
        sys.exit(1)
    
    # 检查设备是否连接
    if not check_device_connected():
        sys.exit(1)
    
    # 检测包名
    package_name = detect_package_name()
    print_info(f"使用包名: {package_name}")
    
    # 1. 上传配置文件
    success, config_path = upload_config_file(package_name)
    if not success:
        sys.exit(1)
    
    # 等待上传完成
    time.sleep(2)
    
    # 2. 切换到配置文件
    if not switch_to_config(package_name, config_path):
        sys.exit(1)
    
    # 等待配置切换完成
    print_info("等待配置切换完成...")
    time.sleep(3)
    
    # 3. 启动代理服务
    if not start_clash(package_name):
        sys.exit(1)
    
    # 等待代理启动完成
    print_info("等待代理启动完成...")
    time.sleep(5)
    
    # 5. 等待5秒后测试关闭代理
    print_info("5秒后将测试关闭代理...")
    time.sleep(5)
    
    # 6. 关闭代理服务
    if not stop_clash(package_name):
        print_warning("代理关闭失败，请手动关闭")
    else:
        print_success("代理已关闭")
    
    # 7. 显示测试完成信息
    print_success("测试脚本执行完成")
    show_post_test_options(package_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(0)
    except Exception as e:
        print_error(f"发生未知错误: {e}")
        sys.exit(1)