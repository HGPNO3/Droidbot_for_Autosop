# DroidBot 项目文档

## 1. 项目简介
**DroidBot** 是一个轻量级的 Android 应用测试输入生成器。
它不需要对 App 进行任何修改（插桩），也不需要 root 权限，即可通过 ADB 向设备发送随机或脚本化的输入事件（如点击、滑动、按键等），从而快速探索 App 的 UI 结构，提高测试覆盖率。

### 核心功能
*   **自动化探索**：使用不同的策略（如贪婪深度优先搜索 DFS、随机策略等）自动遍历 App 的各个界面。
*   **无需插桩**：直接在 APK 上运行，甚至可以直接在设备上已安装的 App 上运行。
*   **生成 UI 转换图 (UTG)**：测试结束后，会生成一个包含所有探索到的状态（界面）和转换（操作）的有向图。
*   **可编程**：支持通过 JSON 脚本自定义特定场景的输入。

## 2. 快速开始

### 安装
```bash
git clone https://github.com/honeynet/droidbot.git
cd droidbot/
pip install -e .
```

### 基本使用
启动 DroidBot 并开始探索一个 APK：
```bash
droidbot -a <path_to_apk> -o <output_dir> -count <event_count>
```
*   `-a`: 目标 APK 文件路径。
*   `-o`: 结果输出目录。
*   `-count`: 要发送的事件总数（默认为极大值，建议根据需求设置，如 200）。
*   `-policy`: 探索策略（默认 `greedy_dfs`）。
*   `-ignore_views_text`: **(新增)** 启用“结构优先”模式。在判断界面状态时，忽略控件的文字内容，仅根据控件结构（类名+ID）来区分状态。这对于解决日历、倒计时、动态列表导致的“状态爆炸”问题非常有效。

## 3. 输出内容详解
运行完成后，DroidBot 会在指定的输出目录（`-o` 参数）生成丰富的测试报告和数据。

### 目录结构示例
```
output_dir/
├── index.html          # 可视化测试报告（入口文件）
├── utg.js              # UI 转换图的数据文件
├── events/             # 记录所有执行的输入事件
├── states/             # 记录所有探索到的界面状态
├── views/              # 界面中的 View 截图（如果是 CV 模式）
├── logcat.txt          # 运行期间的系统日志
└── droidbot_env.json   # 运行环境信息
```

### 关键文件说明

#### 1. `index.html` (可视化报告)
这是查看结果的最佳方式。在浏览器中打开此文件，可以看到一个交互式的 **UI 转换图 (UTG)**。
*   **节点 (Node)**：代表 App 的一个界面（State）。点击节点可以看到该界面的截图和详细结构。
*   **边 (Edge)**：代表一个操作（Event），如点击某个按钮跳转到下一个界面。

#### 2. `utg.js`
存储了 UTG 的核心数据结构，包含所有节点和边的信息，供 `index.html` 调用。

#### 3. `events/` 目录
包含一系列 `.json` 文件，每个文件代表一个执行的事件。
*   **命名格式**：`event_<timestamp>.json`
*   **内容示例**：
    ```json
    {
      "event": {
        "event_type": "touch",   // 事件类型：点击
        "view": { ... }          // 被点击的控件信息
      },
      "start_state": "...",      // 事件发生前的状态哈希
      "stop_state": "..."        // 事件发生后的状态哈希
    }
    ```

#### 4. `states/` 目录
包含 App 运行过程中所有捕捉到的界面状态。每个状态通常包含三个文件：
*   `state_<timestamp>.json`: 界面的结构信息（View Hierarchy，包含所有控件的坐标、属性等）。
*   `screen_<timestamp>.png`: 当前界面的截图。
*   `state_str`: 状态的哈希值。

#### 5. `logcat.txt`
完整的 ADB logcat 输出，用于调试 App 在运行期间的崩溃或异常行为。
