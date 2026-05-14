<p align="center">
  <img src="logo.svg" width="120" alt="QAMule Logo">
</p>

<h1 align="center">QAMule</h1>

<p align="center">
  AI 原生的 Android 测试框架 —— Agent 本身就是测试员。
</p>

<p align="center">
  <a href="README.md">English</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#工作原理">工作原理</a> •
  <a href="https://github.com/lanbaoshen/QAMule-Practice">实践参考</a> •
  <a href="LICENSE">MIT License</a>
</p>

---

## 这是什么？

QAMule 是一个 **Agent 优先** 的 Android QA 框架。不同于传统自动化（脚本是核心，AI 辅助生成），这里 **AI Agent 直接操作设备完成测试**。测试脚本仅仅是可选的加速层——在测试成功后生成，用于跳过重复场景的 Agent 推理开销。

**范式转变：**

| | 传统 AI 测试 | QAMule |
|---|---|---|
| **核心执行者** | 脚本 | AI Agent |
| **AI 的角色** | 生成/维护脚本 | 直接执行测试 |
| **脚本** | 必须 | 可选（加速缓存） |
| **失败处理** | 中断，等人修 | Agent 自我诊断并恢复 |
| **新场景** | 必须先写脚本 | Agent 直接探索并测试 |

## 快速开始

### 前置条件

- Android 设备通过 USB 连接（或模拟器）
- UV（用于管理 Python 环境和依赖）
- ADB（Android Debug Bridge）

### 安装

1. 克隆或将 QAMule 作为 agent 插件添加到项目中：

```
# Github Copilot
copilot plugin marketplace add lanbaoshen/agent-plugins
copilot plugin install QAMule@lanbaoshen

# Claude Code
/plugin marketplace add lanbaoshen/agent-plugins
/plugin install QAMule@lanbaoshen

# VSCode
# command + shift + p -> "Chat: Install plugin from Source" -> "lanbaoshen/agent-plugins"
```

2. 让 Agent 初始化：

```
/qamule:init
```

自动复制配置文件、初始化 `kb/`、`tests/`、`dataset/` 骨架，并安装依赖。

### 使用

`uiautomator2` 和 `pytest` 是内部执行技能，不直接向用户暴露；QA 和 Distiller 工作流会自动调用它们。

**测试功能：**
```
@QAMule QA 测试登录流程
```

**探索应用：**
```
@QAMule QA 探索设置页面
```

**采集 VLM 训练数据：**
```
@QAMule Distiller 在 com.android.settings 中打开蓝牙
```

**更新知识库：**
```
/qamule:kb 更新知识，该应用只能通过 UI 启动
```

**查看测试覆盖：**
```
/qamule:testcase 现在覆盖了哪些功能点
```

## 工作原理

### QA Agent —— 以测代写

QA Agent 执行类人的测试循环：

```
观察 → 计划 → 执行 → 验证 → 学习 → 记录
 ↑                                      |
 └──────────────────────────────────────┘
```

1. **观察** — 截屏，读取当前界面
2. **计划** — 将可见元素与测试目标匹配，查阅知识库
3. **执行** — 发出一条设备命令（点击、滑动、输入等）
4. **验证** — 通过截屏确认操作效果
5. **学习** — 将新发现（选择器、页面、异常行为）沉淀到 KB
6. **记录** — 成功后可选地生成 pytest 脚本，供后续加速回放

脚本是测试成功的**副产品**，不是前提条件。

### Distiller Agent —— 训练下一代

Distiller 以截图作为唯一观察输入，执行**不依赖选择器**的设备命令，并将原始像素坐标交互记录为 VLM 训练轨迹。它保留真实行为，包括误操作和纠正过程——为视觉推理模型提供真实训练信号。

### 知识库 —— 持续增长的记忆

Agent 发现的每个页面、元素、业务流程、已知缺陷都持久化到 `kb/`。Agent 不会重复探索已知内容，知识随使用不断积累，每次测试都比上次更快。

### Agents

| Agent | 目的 | 产出 |
|-------|------|------|
| **QA** | 探索式测试 & 回归测试 | KB 条目 + pytest 脚本 |
| **Distiller** | 训练数据采集 | 基于坐标的轨迹数据 |

### Skills

| Skill | 职责 |
|-------|------|
| **uiautomator2** | 内部设备操作技能，通过 `u2cli` 完成点击、滑动、输入、截屏、应用管理 |
| **kb** | 读写持久化应用知识 — 页面、流程、选择器、异常行为 |
| **pytest** | 内部 pytest 规范技能，定义脚本结构、fixture 约定、运行模式和 pause-on-failure 用法 |
| **testcase** | 在手动测试前检索已有用例，避免重复劳动 |
| **dataset** | 管理 VLM 训练轨迹 — 命名、Schema、可视化浏览 |
| **init** | 一次性项目脚手架搭建 |

## 设计理念

1. **Agent 即测试员。** AI 不是为别的东西写测试——它*自己执行*测试，直接操作设备。

2. **脚本是加速，不是必需。** 生成的 pytest 脚本是缓存：在不需要 Agent 推理的情况下重放已验证场景。没有脚本？Agent 直接上手测。

3. **知识持续累积。** 每次会话让下次更快。KB 增长，Agent 上下文更丰富，冗余探索消失。

4. **训练数据是天然副产品。** Distiller 把设备交互转化为 VLM 训练轨迹——一次交互，两份价值（测试结果 + 训练数据）。

5. **失败自愈。** 测试失败时设备状态冻结（pause-on-failure），Agent 检查、诊断、恢复——无需人工介入。

## 未来方向

- [ ] **测试报告** — 测试完成后生成结构化报告，包含结果摘要、截图和覆盖率。
- [ ] **iOS 支持** — 将 `uiautomator2` skill 替换为基于 XCUITest 的 skill，Agent 层和 KB 层无需改动。
- [ ] **鸿蒙支持** — 新增鸿蒙自动化 skill，扩展对华为设备的覆盖。

## 依赖

- [uiautomator2](https://github.com/openatx/uiautomator2) — Android 自动化库
- [uiautomator2-cli](https://github.com/lanbaoshen/uiautomator2-cli) — 为 Agent 使用设计的 CLI 封装
- [pytest](https://pytest.org/) — 生成脚本的测试框架

## 许可证

[MIT](LICENSE) © 2026 Lanbao Shen
