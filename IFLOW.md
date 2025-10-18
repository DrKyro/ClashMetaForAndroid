# ClashMetaForAndroid 项目指南

## 项目概述

ClashMetaForAndroid 是 Clash.Meta 的 Android 平台图形用户界面，提供了一个功能强大的代理管理工具。该项目基于 Kotlin 和 Android 开发，集成了 Clash.Meta 核心功能，支持多种代理协议和规则集。

### 主要技术栈
- **语言**: Kotlin
- **框架**: Android SDK
- **构建工具**: Gradle with Kotlin DSL
- **架构**: 模块化设计，包含 app、core、service、design、common 和 hideapi 模块
- **核心**: 集成 Clash.Meta 内核（Golang）

### 项目结构
```
ClashMetaForAndroid/
├── app/                 # 主应用模块
├── core/                # 核心功能模块，包含 Clash.Meta 内核集成
├── service/             # 服务模块，处理后台代理服务
├── design/              # UI 设计模块
├── common/              # 通用工具和常量
├── hideapi/             # Android 隐藏 API 访问模块
├── gradle/              # Gradle 配置
├── .github/             # GitHub Actions 工作流
└── fastlane/            # 自动化发布配置
```

## 构建和运行

### 环境要求
- **Android SDK**: API 21+ (最低), API 35+ (目标)
- **JDK**: OpenJDK 11 或更高版本
- **CMake**: 用于构建原生代码
- **Golang**: 用于编译 Clash.Meta 内核
- **架构支持**: arm64-v8a, armeabi-v7a, x86, x86_64

### 构建步骤

1. **初始化子模块**
   ```bash
   git submodule update --init --recursive
   ```

2. **配置本地环境**
   - 创建项目根目录下的 `local.properties` 文件，指定 Android SDK 路径：
     ```properties
     sdk.dir=/path/to/android-sdk
     ```

3. **配置签名（可选）**
   - 创建项目根目录下的 `signing.properties` 文件：
     ```properties
     keystore.path=/path/to/keystore/file
     keystore.password=<key store password>
     key.alias=<key alias>
     key.password=<key password>
     ```

4. **构建应用**
   ```bash
   # 构建 Alpha 版本
   ./gradlew app:assembleAlphaDebug
   
   # 构建 Meta 版本
   ./gradlew app:assembleMetaDebug
   
   # 构建发布版本
   ./gradlew app:assembleMeta-AlphaRelease
   ```

### 构建变体
项目支持两种主要变体：
- **Alpha**: 默认版本，应用 ID 为 `com.github.metacubex.clash.alpha`
- **Meta**: 完整功能版本，应用 ID 为 `com.github.metacubex.clash.meta`

## 开发约定

### 代码风格
- 遵循官方 Kotlin 代码风格指南
- 使用 AndroidX 库而非 Support 库
- 采用协程处理异步操作

### 模块依赖关系
- `app` 依赖所有其他模块
- `core` 提供核心功能和 Clash.Meta 集成
- `service` 处理后台代理服务
- `design` 提供 UI 组件和主题
- `common` 包含共享工具类和常量
- `hideapi` 提供对 Android 隐藏 API 的访问

### Intent 动作约定
项目支持多种 ADB 控制命令，用于自动化测试和控制：

- **启动代理**: `com.github.metacubex.clash.meta.action.START_CLASH`
- **停止代理**: `com.github.metacubex.clash.meta.action.STOP_CLASH`
- **切换代理状态**: `com.github.metacubex.clash.meta.action.TOGGLE_CLASH`
- **切换到本地配置**: `com.github.metacubex.clash.meta.action.SWITCH_TO_CONFIG`
- **切换到URL配置**: `com.github.metacubex.clash.meta.action.SWITCH_TO_URL`

### 测试脚本
项目提供了多种平台的测试脚本：
- **Windows**: `test_adb_control.bat` 和 `test_adb_control.py`
- **Linux/Mac**: `test_adb_control.sh`
- **Python 版本**: `test_adb_control.py`（跨平台兼容）

## 特殊功能

### ADB 控制
项目支持通过 ADB 命令控制代理服务，便于自动化测试和集成：

```bash
# 启动代理
adb shell am start -a com.github.metacubex.clash.meta.action.START_CLASH com.github.metacubex.clash/.ExternalControlActivity

# 切换到本地配置文件
adb shell am start -a com.github.metacubex.clash.meta.action.SWITCH_TO_CONFIG --es config_path "/sdcard/Download/config.yaml" com.github.metacubex.clash/.ExternalControlActivity
```

### 自动化更新
- 当 `MetaCubeX/Clash.Meta` 内核更新时，自动触发依赖更新流程
- 支持通过 GitHub Actions 自动构建和发布预发布版本

### 地理数据文件
项目使用自动化任务下载地理数据文件：
- `geoip.metadb`: IP 地理位置数据库
- `geosite.dat`: 网站域名分类数据库
- `GeoLite2-ASN.mmdb`: ASN 号码数据库

## 常见问题

### 编译错误处理
- 如果遇到 `downloadGeoFiles` 任务失败，可以跳过该任务：
  ```bash
  ./gradlew app:compileAlphaDebugKotlin -x :app:downloadGeoFiles
  ```

### ExternalControlActivity 编译问题
- 如果遇到 `profileManager` 引用错误，确保使用了正确的 `withProfile` 工具函数
- 确保所有 Toast 调用后添加了 `.show()` 方法

### 子模块更新
- 如果遇到与 Clash.Meta 内核相关的问题，尝试更新子模块：
  ```bash
  git submodule update --remote --merge
  ```

## 贡献指南

### 内核贡献
- 向 `MetaCubeX/Clash.Meta` 的 `Alpha` 分支贡献通用功能
- 向 `MetaCubeX/Clash.Meta` 的 `android-open` 分支贡献 Android 特定补丁

### 应用贡献
- 遵循现有的代码风格和架构模式
- 确保新功能与现有模块化设计保持一致
- 添加适当的测试和文档

## 发布流程

1. **预发布版本**: 手动触发 `Build Pre-Release` GitHub Action
2. **正式版本**: 手动触发 `Build Release` GitHub Action，并填写版本标签
3. **版本号**: 版本号和版本代码会在发布时自动更新

## 许可证

项目遵循开源许可证，具体信息请参见 LICENSE 文件。