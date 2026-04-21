# 垫图增强功能 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `banana-app-prompt-generator` skill 中新增垫图（风格参考图）和元素约束（文字指定必须出现的元素）两个可选输入，生成增强 prompt 后通过 lovart-api 完成生图。

**Architecture:** 仅修改 `banana-app-prompt-generator` 的 SKILL.md，在输入规范、Prompt 构建原则、生图流程三处插入新内容。`lovart-api` skill 已具备 `upload` 和 `--attachments` 能力，无需改动。

**Tech Stack:** Markdown（SKILL.md）、Python CLI（agent_skill.py，已有，不修改）

---

## 文件变更清单

| 操作 | 文件 |
|------|------|
| 修改 | `.claude/skills/banana-app-prompt-generator/SKILL.md` |
| 新增（参考） | `docs/superpowers/specs/2026-04-21-reference-image-enhancement-design.md`（已存在） |

---

### Task 1: 在输入信息分析部分新增垫图和元素约束字段说明

**Files:**
- Modify: `.claude/skills/banana-app-prompt-generator/SKILL.md`（输入信息分析章节，约第 14-21 行）

- [ ] **Step 1: 在"输入信息分析"列表末尾追加两个可选字段**

找到以下内容：
```markdown
1. **应用名称** — 应用的核心标识
2. **一句话描述** — 应用的核心价值主张
3. **应用简介** — 详细的功能描述
4. **应用类型** — 工具类、社交类、效率类、游戏类等
5. **宣传素材** — 现有的图标、截图、slogan等
```

替换为：
```markdown
1. **应用名称** — 应用的核心标识
2. **一句话描述** — 应用的核心价值主张
3. **应用简介** — 详细的功能描述
4. **应用类型** — 工具类、社交类、效率类、游戏类等
5. **宣传素材** — 现有的图标、截图、slogan等
6. **参考图**（可选）— 本地图片路径，用于风格垫图；生成的图片将参考该图的色调、构图与整体风格
7. **必须包含元素**（可选）— 文字描述，指定画面中必须出现的视觉元素，如"月亮、声音波形"
```

- [ ] **Step 2: 验证修改正确**

打开 `.claude/skills/banana-app-prompt-generator/SKILL.md`，确认第 6、7 条已出现在输入列表中，格式与前五条一致。

---

### Task 2: 在 Prompt 构建原则中新增垫图与元素约束注入规则

**Files:**
- Modify: `.claude/skills/banana-app-prompt-generator/SKILL.md`（Prompt构建原则章节，"强制语言约束"小节之后）

- [ ] **Step 1: 在"强制语言约束"小节之后插入新小节**

找到以下内容（约第 75-81 行）：
```markdown
### 强制语言约束（最高优先级）

**所有生成的prompt内容必须使用中文输出**，包括：
- 正向描述词全部用中文
- 不得出现英文关键词、英文括号权重语法（如 `(keyword:1.5)`）
- 即梦版本和Banana版本统一使用中文，不区分平台语言
- **不输出负面提示词**，所有prompt只包含正向描述内容
```

在该小节**之后**（即"画面质量三原则"之前）插入：

```markdown
### 垫图与元素约束注入规则

当用户提供了**参考图**或**必须包含元素**时，在每个场景的 prompt 正文末尾追加以下语句：

**有参考图时**，追加：
```
参考附图的整体风格、色调与构图氛围
```

**有必须包含元素时**，追加（置于风格参考语句之后）：
```
画面中必须包含：[用户输入的元素描述]
```

**追加规则：**
- 两条语句均追加在 prompt 正文末尾，即梦版本和 Banana 版本均需追加
- 如两者同时存在，先追加风格参考语句，再追加元素约束语句
- 语句使用中文，与现有强制语言约束一致
- 多场景批量生图时，每个场景的 prompt 均需追加（内容相同）
```

- [ ] **Step 2: 验证修改正确**

确认新小节出现在"强制语言约束"之后、"画面质量三原则"之前，格式正确，无乱码。

---

### Task 3: 在生图标准流程中新增垫图上传步骤

**Files:**
- Modify: `.claude/skills/banana-app-prompt-generator/SKILL.md`（"Prompt生成后的生图流程"章节，"生图标准流程"小节）

- [ ] **Step 1: 在生图标准流程中插入垫图上传步骤**

找到以下内容（约第 222-229 行）：
```markdown
### 生图标准流程

```
1. config --json          → 检查 active_project，未设置则询问用户
2. threads --json         → 检查是否有相关 thread 可复用
3. chat --prompt "[生成的中文prompt]" --prefer-models '{"IMAGE":["对应模型"]}' --json --download
4. 将 downloaded[].local_path 文件作为附件发送给用户
5. 附上画布链接：https://www.lovart.ai/canvas?projectId={project_id}
```
```

替换为：
```markdown
### 生图标准流程

```
0. [仅有参考图时] 上传垫图，获取 CDN URL：
   python3 {baseDir}/agent_skill.py upload --file /path/to/ref.png
   → 记录返回的 url 字段值，后续作为 --attachments 参数使用

1. config --json          → 检查 active_project，未设置则询问用户
2. threads --json         → 检查是否有相关 thread 可复用
3. chat --prompt "[生成的中文prompt]" \
        [--attachments "CDN_URL"]  ← 仅有参考图时才加此参数 \
        --prefer-models '{"IMAGE":["对应模型"]}' \
        --json --download
4. 将 downloaded[].local_path 文件作为附件发送给用户
5. 附上画布链接：https://www.lovart.ai/canvas?projectId={project_id}
```

**多场景批量生图时有参考图：** 同一 CDN URL 复用于所有场景的 `--attachments`，无需重复上传。
```

- [ ] **Step 2: 验证修改正确**

确认 Step 0 已出现在流程中，`--attachments` 参数有条件说明，多场景复用说明存在。

---

### Task 4: 在生图标准流程中新增垫图上传失败的错误处理

**Files:**
- Modify: `.claude/skills/banana-app-prompt-generator/SKILL.md`（"Prompt生成后的生图流程"章节末尾）

- [ ] **Step 1: 在生图流程章节末尾追加错误处理说明**

在整个"Prompt生成后的生图流程"章节的最末尾（文件末尾，约第 279 行之后）追加：

```markdown

### 垫图上传失败处理

如果 `upload` 命令返回错误或无法获取 CDN URL：

1. 告知用户："参考图上传失败，无法使用垫图功能。"
2. 询问用户："是否继续生图（不使用参考图）？"
3. 如用户确认继续 → 跳过 Step 0，不传 `--attachments`，按正常流程生图
4. 如用户取消 → 停止，不调用 chat
```

- [ ] **Step 2: 验证修改正确**

确认错误处理小节出现在文件末尾，格式正确。

---

### Task 5: 端到端验证（手动测试用例）

**Files:**
- 参考: `docs/superpowers/specs/2026-04-21-reference-image-enhancement-design.md`（示例章节）

- [ ] **Step 1: 验证"仅元素约束"场景**

使用以下输入触发 skill：
```
应用名称：日程规划宝
一句话描述：让每一天都井井有条
应用类型：效率工具类
必须包含元素：日历格子、勾选标记
```

预期：生成的 prompt 末尾包含 `画面中必须包含：日历格子、勾选标记`，生图流程不传 `--attachments`。

- [ ] **Step 2: 验证"仅垫图"场景**

使用以下输入触发 skill：
```
应用名称：夜聊
一句话描述：深夜EMO党的树洞
应用类型：社交App
参考图：[任意本地图片路径]
```

预期：
1. 先执行 `upload --file [路径]` 获取 CDN URL
2. 生成的 prompt 末尾包含 `参考附图的整体风格、色调与构图氛围`
3. `chat` 命令包含 `--attachments "[CDN URL]"`

- [ ] **Step 3: 验证"垫图 + 元素约束"组合场景**

使用以下输入触发 skill：
```
应用名称：夜聊
一句话描述：深夜EMO党的树洞
应用类型：社交App
参考图：[任意本地图片路径]
必须包含元素：月亮、声音波形
```

预期：prompt 末尾依次出现：
```
参考附图的整体风格、色调与构图氛围，
画面中必须包含：月亮、声音波形
```
`chat` 命令包含 `--attachments`。

- [ ] **Step 4: 验证垫图上传失败降级**

将参考图路径设为不存在的文件，触发 skill。

预期：skill 告知上传失败，询问是否继续，用户确认后不带 `--attachments` 正常生图。
