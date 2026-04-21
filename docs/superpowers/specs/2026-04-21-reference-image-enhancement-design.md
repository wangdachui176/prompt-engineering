# 垫图增强功能设计文档

**日期：** 2026-04-21  
**状态：** 待审查  
**关联 Skill：** `banana-app-prompt-generator`、`lovart-api`

---

## 背景

`banana-app-prompt-generator` 目前只接受文字输入（应用名称、描述、类型等），生成 prompt 后调用 lovart-api 生图。

用户需要两种新能力：
1. **风格垫图**：上传参考图，生成的图片参考该图的风格/色调/构图
2. **元素约束**：用文字指定画面中必须出现的特定元素

---

## 设计目标

- 在现有 `banana-app-prompt-generator` skill 流程中，新增可选的垫图和元素约束输入
- 垫图风格分析交由 Lovart Agent 处理（利用其 vision 能力），不做手动提取
- Prompt 构建结果对用户透明可见
- 生图流程与现有流程保持一致

---

## 输入规范

在原有输入基础上，新增两个可选字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `参考图` | 本地文件路径 | 风格垫图，可选 |
| `必须包含元素` | 文字描述 | 如"必须有月亮"、"必须用红色主色调"，可选 |

两个字段均为可选，可单独使用，也可组合使用。

---

## 流程设计

### 完整流程（垫图 + 元素约束均存在时）

```
Step 1: 垫图上传
  → python3 agent_skill.py upload --file /path/to/ref.png
  → 得到 CDN URL（后续 chat 时作为 --attachments 传入）

Step 2: Prompt 构建
  → 执行原有 banana-app-prompt-generator 逻辑，生成基础 prompt
  → 追加风格参考说明（如有垫图）：
      末尾加入："参考附图的整体风格、色调与构图氛围"
  → 追加元素约束（如有元素描述）：
      末尾加入："画面中必须包含：[用户描述]"
  → 向用户展示完整 prompt，等待确认或修改

Step 3: 调用 Lovart 生图
  → config --json  →  检查 active_project
  → threads --json  →  检查可复用 thread
  → chat --prompt "[完整prompt]" \
         --attachments "[CDN_URL]" \   ← 仅有垫图时才加此参数
         --prefer-models '{"IMAGE":["对应模型"]}' \
         --json --download
  → 将 downloaded[].local_path 作为附件发送给用户
  → 附上画布链接
```

### 仅有元素约束（无垫图）

跳过 Step 1，Step 3 不传 `--attachments`，其余不变。

### 仅有垫图（无元素约束）

Step 2 不追加元素约束语句，其余不变。

---

## Prompt 构建规则

### 风格参考语句（有垫图时追加）

在 prompt 末尾追加，即梦和 Banana 版本均适用：

```
参考附图的整体风格、色调与构图氛围
```

### 元素约束语句（有元素描述时追加）

在 prompt 末尾追加，置于风格参考语句之后（如两者同时存在）：

```
画面中必须包含：[用户输入的元素描述]
```

### 追加位置

两条语句均追加在 prompt 正文末尾，在负面提示词之前（当前规范无负面提示词，直接追加在末尾）。

---

## 对现有 Skill 的修改范围

仅修改 `banana-app-prompt-generator` 的 SKILL.md，具体改动：

1. **输入信息分析**部分：新增"参考图"和"必须包含元素"两个可选输入字段说明
2. **Prompt 构建原则**部分：新增"垫图与元素约束注入规则"小节
3. **生图标准流程**部分：新增垫图上传步骤（Step 0），以及 `--attachments` 参数的条件使用说明

`lovart-api` skill 无需修改，其 `upload` 和 `--attachments` 能力已存在。

---

## 示例

### 输入

```
应用名称：夜聊
一句话描述：深夜EMO党的树洞
应用类型：社交App
参考图：/Users/me/ref-style.png
必须包含元素：月亮、声音波形
```

### Step 1 输出（上传垫图）

```bash
python3 agent_skill.py upload --file /Users/me/ref-style.png
# → {"url": "https://assets-persist.lovart.ai/img/xxx/ref-style.png"}
```

### Step 2 输出（完整 Prompt，以 App 图标为例）

即梦版本：
```
极简月亮与声音波形图标，深夜天空渐变背景，深蓝与紫色配色，温暖琥珀色发光，
细线矢量风格，扁平化设计带轻微立体感，现代App图标美学，小尺寸下辨识度极高，
参考附图的整体风格、色调与构图氛围，
画面中必须包含：月亮、声音波形
```

### Step 3 调用

```bash
python3 agent_skill.py chat \
  --prompt "[上方完整prompt]" \
  --attachments "https://assets-persist.lovart.ai/img/xxx/ref-style.png" \
  --prefer-models '{"IMAGE":["generate_image_nano_banana_pro"]}' \
  --json --download
```

---

## 边界情况

| 情况 | 处理方式 |
|------|---------|
| 垫图上传失败 | 告知用户上传失败，询问是否继续（不带垫图生图） |
| 元素描述与应用风格冲突 | 保留用户描述，在 prompt 中同时保留，由 Lovart Agent 平衡 |
| 用户想修改 prompt | Step 2 展示 prompt 后等待用户确认，用户可直接回复修改内容 |
| 多场景批量生图时有垫图 | 同一 CDN URL 复用于所有场景的 --attachments |
