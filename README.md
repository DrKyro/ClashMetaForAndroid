# Clash Meta for Android

[Clash.Meta](https://github.com/MetaCubeX/Clash.Meta) 的 Android 平台图形用户界面

## 主要功能

继承 [Clash.Meta](https://github.com/MetaCubeX/Clash.Meta) 的所有功能

[<img src="https://fdroid.gitlab.io/artwork/badge/get-it-on.png"
     alt="Get it on F-Droid"
     height="80">](https://f-droid.org/packages/com.github.metacubex.clash.meta/)

## 系统要求

- Android 5.0+ (最低要求)
- Android 7.0+ (推荐)
- `armeabi-v7a`、`arm64-v8a`、`x86` 或 `x86_64` 架构

## 构建说明

1. 更新子模块

   ```bash
   git submodule update --init --recursive
   ```

2. 安装 **OpenJDK 11**、**Android SDK**、**CMake** 和 **Golang**

3. 在项目根目录创建 `local.properties` 文件，内容如下：

   ```properties
   sdk.dir=/path/to/android-sdk
   ```

4. 在项目根目录创建 `signing.properties` 文件（用于签名）：

   ```properties
   keystore.path=/path/to/keystore/file
   keystore.password=<key store password>
   key.alias=<key alias>
   key.password=<key password>
   ```

5. 构建应用

   ```bash
   ./gradlew app:assembleMeta-AlphaRelease
   ```

## 自动化控制

应用包名为 `com.github.metacubex.clash.meta`

- 切换 Clash.Meta 服务状态
  - 向活动 `com.github.kr328.clash.ExternalControlActivity` 发送意图，动作为 `com.github.metacubex.clash.meta.action.TOGGLE_CLASH`
- 启动 Clash.Meta 服务
  - 向活动 `com.github.kr328.clash.ExternalControlActivity` 发送意图，动作为 `com.github.metacubex.clash.meta.action.START_CLASH`
- 停止 Clash.Meta 服务
  - 向活动 `com.github.kr328.clash.ExternalControlActivity` 发送意图，动作为 `com.github.metacubex.clash.meta.action.STOP_CLASH`
- 导入配置文件
  - URL Scheme: `clash://install-config?url=<encoded URI>` 或 `clashmeta://install-config?url=<encoded URI>`

## 贡献与项目维护

### Meta 内核

- CMFA 使用 `MetaCubeX/Clash.Meta` 仓库的 `android-real` 分支的内核，该分支是主 `Alpha` 分支和 `android-open` 的合并。
  - 如果你想为内核贡献通用功能，请向 Meta 内核仓库的 `Alpha` 分支提交 PR。
  - 如果你想为内核贡献 Android 特定的补丁，请向 Meta 内核仓库的 `android-open` 分支提交 PR。

### 维护流程

- 当 `MetaCubeX/Clash.Meta` 内核更新到新版本时，本仓库的 `Update Dependencies` 操作会自动触发。
  - 它将拉取新版本的 Meta 内核，更新所有 Golang 依赖，并在无需人工干预的情况下创建 PR。
  - 如果 PR 中存在任何编译错误，你需要在合并前修复。或者，你也可以直接合并 PR。
- 手动触发 `Build Pre-Release` 操作将编译并发布一个 `PreRelease` 版本。
- 手动触发 `Build Release` 操作将编译、标记并发布一个 `Release` 版本。
  - 你必须在 `Release Tag` 空白处填入你想发布的标签，格式为 `v1.2.3`。
  - `build.gradle.kts` 中的 `versionName` 和 `versionCode` 将自动更新为你填写的标签。
