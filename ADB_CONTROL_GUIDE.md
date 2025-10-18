# ClashMetaForAndroid ADB 控制命令使用说明

## 功能概述
已为 ClashMetaForAndroid 添加了通过 ADB 命令控制代理的功能，支持以下操作：
1. 启动代理服务
2. 关闭代理服务
3. 使用指定配置文件路径启动代理

## ADB 命令使用方法

### 1. 启动代理
```bash
adb shell am start -a com.github.metacubex.clash.meta.action.START_CLASH com.github.metacubex.clash/.ExternalControlActivity
```

### 2. 关闭代理
```bash
adb shell am start -a com.github.metacubex.clash.meta.action.STOP_CLASH com.github.metacubex.clash/.ExternalControlActivity
```

### 3. 切换代理状态（启动/关闭）
```bash
adb shell am start -a com.github.metacubex.clash.meta.action.TOGGLE_CLASH com.github.metacubex.clash/.ExternalControlActivity
```

### 4. 使用指定配置文件切换配置
```bash
adb shell am start -a com.github.metacubex.clash.meta.action.SWITCH_TO_CONFIG \
    --es config_path "/sdcard/Android/data/{package_name}/files/config.yaml" \
    com.github.metacubex.clash/.ExternalControlActivity
```

### 5. 使用网络URL配置文件切换配置
```bash
adb shell am start -a com.github.metacubex.clash.meta.action.SWITCH_TO_URL \
    --es config_url "https://example.com/config.yaml" \
    com.github.metacubex.clash/.ExternalControlActivity
```

## 参数说明
- `--es config_path`: 指定配置文件的完整路径，例如 `/sdcard/Android/data/{package_name}/files/config.yaml`
- `--es config_url`: 指定网络配置文件的URL，例如 `https://example.com/config.yaml`
- 配置文件必须是 Clash Meta 兼容的 YAML 格式文件
- URL配置文件支持HTTP和HTTPS协议

## 测试脚本
项目提供了一个 Python 测试脚本 `test_adb_control.py`，可以自动测试 ADB 控制功能：

### 使用测试脚本
```bash
python3 test_adb_control.py
```

### 测试脚本功能
1. 自动检测设备上安装的 ClashMetaForAndroid 包名（支持 Alpha 和 Meta 版本）
2. 上传配置文件到设备（使用应用的外部存储目录，避免权限问题）
3. 切换到上传的配置文件
4. 启动代理服务
5. 等待5秒后测试关闭代理服务
6. 显示测试完成后的操作选项

### 测试脚本配置
- 默认配置文件：`socks5_config.yaml`（需与脚本在同一目录）
- 设备上的配置文件路径：`/sdcard/Android/data/{package_name}/files/socks5_config.yaml`
- 支持的包名：
  - `com.github.metacubex.clash.alpha`（Alpha 版本）
  - `com.github.metacubex.clash.meta`（Meta 版本）

## 实现细节
1. 在 `common/src/main/java/com/github/kr328/clash/common/constants/Intents.kt` 中添加了新的 Intent 常量：
   - `ACTION_SWITCH_TO_CONFIG` - 切换到本地配置文件
   - `ACTION_SWITCH_TO_URL` - 切换到网络URL配置文件
   - `EXTRA_CONFIG_PATH` - 本地配置文件路径参数
   - `EXTRA_CONFIG_URL` - 网络配置文件URL参数

2. 在 `ExternalControlActivity.kt` 中实现了以下方法：
   - `switchToConfig()` 方法：
     - 验证配置文件是否存在
     - 创建新的 Profile 并导入配置文件
     - 设置为活动配置（不启动代理服务）
   - `switchToUrl()` 方法：
     - 创建新的 URL 类型的 Profile
     - 从网络URL下载并应用配置
     - 设置为活动配置（不启动代理服务）

3. 在 `AndroidManifest.xml` 中注册了新的 Intent 过滤器以支持新的 Action

4. 在 `ProfileManager.kt` 中增强了文件处理逻辑：
   - 添加了详细的日志记录
   - 改进了文件复制功能
   - 增强了错误处理和验证

## 注意事项
1. 使用本地配置文件切换时，应用会自动创建一个新的 Profile，名称为配置文件名（不含扩展名）
2. 使用URL配置文件切换时，应用会自动创建一个新的 Profile，名称为"URL配置_时间戳"
3. 如果本地配置文件不存在，会显示错误提示
4. 切换配置命令仅更换配置文件，不会自动启动代理服务
5. 启动代理需要使用单独的 `ACTION_START_CLASH` 命令
6. 确保应用有读取指定配置文件的权限
7. URL配置文件需要设备能够访问相应的网络地址
8. URL配置文件下载可能需要一些时间，取决于网络状况和文件大小
9. 测试脚本会自动检测设备上安装的包名，无需手动指定
10. 测试脚本使用应用的外部存储目录（`/sdcard/Android/data/{package_name}/files/`）来避免权限问题
11. 测试脚本包含完整的启动和关闭代理测试流程，适合自动化测试