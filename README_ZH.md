<p align="center">
    <img src="logo.svg" alt="QAMule" width="200">
</p>

<p align="center">
    <strong>AI 驱动的 GitHub Copilot 扩展，自主探索、理解和测试 Android 应用。</strong>
</p>

<p align="center">
    <a href="README.md">English</a> | 中文
</p>

---

> **探索一次，固化为脚本，只在失败时介入。**

QAMule 是一个 [GitHub Copilot 扩展插件](https://code.visualstudio.com/docs/copilot/chat/chat-extensions)，让 AI 成为自主的 Android QA 工程师。它在真实设备上探索你的应用，将探索过程转化为 pytest 测试脚本，在应用变化时自动维护脚本，并能采集 VLM 训练轨迹 —— 全程无需手写测试代码。

## 设计理念

传统 UI 测试自动化很脆弱：选择器失效、流程变化、维护成本不断累积。QAMule 采用不同的方法：

1. **探索 (Explore)** — AI 操作真实设备，发现 UI 元素和用户流程。
2. **固化 (Solidify)** — 将探索结果转化为确定性的 pytest 脚本，运行时不需要 AI。
3. **记忆 (Remember)** — 知识库 (`kb/`) 持久化已发现的页面、选择器和流程，避免重复探索。
4. **修复 (Repair)** — 当测试失败，AI 在失败现场重新检查设备，修补脚本并更新 `kb/`。

这让测试执行保持快速和低成本，AI 仅在探索和修复环节介入 —— 这正是它真正有价值的地方。

## 智能体 (Agents)

QAMule 提供多智能体系统，每个智能体有专属职责。你只需与 **Coordinator** 交互，它会自动调度其余智能体。

| 智能体 | 职责 | 调用方 |
|---|---|---|
| **Coordinator (协调者)** | 总调度。检查测试是否存在、执行测试、将工作分派给专家智能体。 | 用户直接调用 |
| **Explorer (探索者)** | 在真实设备上探索新功能，编写并验证 pytest 脚本，将知识存入 `kb/`。 | Coordinator |
| **First Responder (急救员)** | 在设备冻结于失败现场时诊断问题，在冻结设备上验证修复，然后恢复会话。 | Coordinator |
| **Maintainer (维护者)** | 修复之前通过但现在失败的测试 —— 施加最小补丁，当 App UI 变化时更新 `kb/`。 | Coordinator |
| **Distiller (蒸馏者)** | 仅通过截图和坐标操作设备，采集 VLM 训练轨迹数据。 | 用户直接调用 |

## 技能 (Skills)

技能为智能体和提示词提供领域知识参考。

| 技能 | 说明 |
|---|---|
| **init** | 脚手架：生成完整测试项目结构（`tests/`、`kb/`、`actions/`、`helpers/`、`conftest.py`、`pyproject.toml`）并安装依赖。 |
| **pytest** | 编写和运行测试的规范 —— 设备 fixture、`--pause-on-failure`、项目结构。 |
| **uiautomator2** | `u2cli` 命令参考 —— 设备控制、元素交互、层级检查、截图。 |
| **viewer** | 启动本地 Web 服务，浏览蒸馏后的 VLM 轨迹，支持截图叠加和动作可视化。 |

## 核心特性

- **自主测试生成** — 描述一个功能，获得可运行的 pytest 脚本。
- **失败暂停 (AI-in-the-Loop)** — 测试失败时，会话在 teardown 前冻结，AI 智能体可检查活设备、修复脚本并恢复运行。
- **知识库** — `kb/` 作为 AI 的持久记忆，存储选择器、流程和页面布局。
- **VLM 轨迹蒸馏** — Distiller 智能体记录纯截图+坐标的手机操作轨迹，用于训练视觉语言模型。
- **轨迹查看器** — 零依赖本地 Web 查看器，回放采集的轨迹数据。

## 失败暂停：AI-in-the-Loop

```
pytest 执行测试套件
        │
    ┌───▼───┐
    │ 通过？ │── 是 ──▶ 下一个测试
    └───┬────┘
        │ 否
        ▼
  ╔═══════════════════════════════╗
  ║  会话已暂停                    ║
  ║  设备冻结在失败现场             ║
  ║  Teardown 尚未执行             ║
  ╚═══════════════╤═══════════════╝
                  ▼
    AI 智能体检查设备状态
    → dump-hierarchy / 截图
    → 诊断根因
    → 修复脚本或 actions.py
                  │
                  ▼
        发送 Enter 恢复执行
        │
    ┌───▼───┐
    │Teardown│──▶ 继续会话
    └───────┘
```

测试失败时，设备保持在精确的失败状态。AI 智能体检查、修复、恢复 —— 无需人工干预。

## 前置条件

| 依赖 | 版本 | 安装 |
|---|---|---|
| [uv](https://docs.astral.sh/uv/) | 最新 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [Python](https://www.python.org/) | >= 3.10 | 通过 `uv` 或系统包管理器 |
| [adb](https://developer.android.com/tools/adb) | 最新 | `brew install android-platform-tools` (macOS) |
| [VS Code](https://code.visualstudio.com/) | 最新 | — |
| [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) | 最新 | VS Code 扩展市场 |

运行前请确保 `adb devices` 能看到你的设备。

## 安装

```bash
copilot plugin install lanbaoshen/QAMule
```

在 VS Code 中启用插件：

1. 打开 **设置** (`Cmd + ,`) → 搜索 `chat.extensionPlugins.enabled` → 设为 `true`。
2. 重新加载 VS Code。

## 快速开始

**1. 初始化项目：**

```
/qamule:init my-app com.example.myapp
```

**2. 测试功能（Agent 模式 → 选择 Coordinator）：**

```
测试 com.example.myapp 的登录流程
```

**3. 查看采集的轨迹：**

```
/qamule:viewer ./dataset
```

启动本地 Web 服务，提供时间线 UI 浏览蒸馏轨迹 —— 截图、动作叠加和逐步回放。

**4. 采集 VLM 轨迹（Agent 模式 → 选择 Distiller）：**

```
在 com.android.settings 中打开蓝牙
```

## 项目结构（init 后）

```
├── kb/                      # 知识库 — AI 的记忆
│   ├── app/
│   │   ├── _overview.md     # 包名、入口
│   │   ├── _index.md        # 已知页面、流程、动作
│   │   ├── screens/         # 每个页面的选择器和备注
│   │   └── flows/           # 逐步流程文档
│   └── helpers/
│       └── _index.md        # 辅助函数注册表
├── tests/
│   ├── conftest.py          # Fixtures（设备、应用启动）
│   ├── README.md            # 测试用例索引
│   └── test_*.py            # 测试脚本
├── actions/                 # 可复用的应用动作函数
├── helpers/                 # 系统级辅助函数
├── dataset/                 # 蒸馏后的 VLM 轨迹数据
├── pytest_plugins/          # 自定义 pytest 插件
└── pyproject.toml           # 项目配置和依赖
```

## 许可证

[MIT](LICENSE)
