# 商店应用物料 · AI绘图Prompt生成系统

基于 OpenCode + Lovart API 的 App 营销物料自动生成工具。
输入应用信息，自动生成即梦/Banana Pro 绘图 Prompt，并完成生图。

---

## 快速开始

### 1. 环境准备

```bash
# 复制环境变量模板
cp .env.example .env

# 填入你的 Lovart API Key
# LOVART_ACCESS_KEY=ak_xxx
# LOVART_SECRET_KEY=sk_xxx
```

### 2. 一键安装

```bash
python setup.py
```

安装内容：
- 检查 Python 版本（需要 3.8+）
- 设置环境变量
- 初始化 Lovart 项目配置
- 创建 output/ 目录结构

### 3. 在 OpenCode 中使用

打开 OpenCode，直接输入应用信息：

```
应用名称：xxx
分类：游戏-开放世界-冒险
简介：xxx
```

系统自动完成：信息补全 → Prompt生成 → 质量自检 → 生图选择 → 生图输出

### 4. 批量生图（可选）

编辑 `run_lovart.py` 中的 `TASKS`，运行：

```bash
python run_lovart.py
```

---

## 项目结构

```
商店应用物料/
├── README.md                        # 本文件
├── .env.example                     # 环境变量模板
├── .env                             # 本地环境变量（不提交）
├── setup.py                         # 一键安装脚本
├── run_lovart.py                    # 批量生图执行脚本
├── 流程图.svg                        # 系统流程图
│
├── .claude/
│   ├── settings.json                # OpenCode 权限配置
│   └── skills/
│       ├── ai-drawing-prompt/       # 底层平台规范（即梦+Banana）
│       │   └── skill.md
│       ├── banana-app-prompt-generator/  # 主 skill（应用物料生成）
│       │   ├── SKILL.md
│       │   └── evals/
│       │       └── evals.json       # 评测用例
│       └── lovart-api/              # Lovart API 调用封装
│           ├── SKILL.md
│           └── agent_skill.py       # API 客户端
│
├── input/                           # 输入素材（参考图、Logo等）
└── output/                          # 生成图片输出目录
    └── {应用名}/                    # 按应用名分目录
```

---

## 核心能力

### 信息补全机制
信息不足时自动推断，不追问用户：
- **充足**（名称+分类+简介）→ 直接生成
- **一般**（名称+分类）→ 名称语义+分类惯例补全
- **稀少**（只有名称或分类）→ 双引擎推断
- **极少**（一句模糊描述）→ 生成3个风格方向供选

### 单场景生成
| 场景 | 主体占比 | 构图策略 |
|-----|---------|---------|
| 宣传海报 | 多档可选：15-20%（小）、45-60%（中）、75-90%（大） | 8种构图可选：叙事留白式/对角线动态式/中心稳重式/S曲线探索式/宏大仰视式/低角冲击式/中心爆发式/天空主导式 |

### 质量自检
7维度自动评分（满分35分，低于25分自动修正）：
主体清晰度 / 光线描述 / 构图完整性 / 风格一致性 / 构图场景策略 / 品牌色落地 / 可生成性

### 内容安全约束
禁止：真人/写实人像、低龄/幼稚风、暴力血腥、负面情绪、模糊失焦、构图不完整

---

## 支持的生图模型

| 模型 | 参数值 | 适用场景 |
|-----|-------|---------|
| 即梦 | `generate_image_jimeng` | 中文语义理解强，风格还原度高 |
| Nano Banana Pro | `generate_image_nano_banana_pro` | 细节丰富，高质量插画 |
| Midjourney | `generate_image_midjourney` | 艺术感强，构图精致 |
| Seedream | `generate_image_seedream_3_0` | 写实风格，光影细腻 |

---

## 环境要求

- Python 3.8+
- OpenCode（Claude CLI）
- Lovart 账号及 API Key
