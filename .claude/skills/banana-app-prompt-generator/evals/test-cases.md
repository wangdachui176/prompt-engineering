# 测试用例1：日程规划宝

## 输入信息
- 应用名称：日程规划宝
- 一句话描述：让每一天都井井有条
- 应用类型：效率工具类
- 简介：帮助用户规划日程、管理任务、提升效率的智能日历应用

## 需要生成的场景
- App图标
- 启动页/首屏

---

## 按照skill执行

### 1. 提取关键信息

**应用核心功能：**
- 日程规划
- 任务管理
- 效率提升
- 智能日历

**功能亮点：**
- 井井有条的状态
- 时间可视化
- 任务完成感
- 规划未来的感觉

**视觉元素：**
- 日历
- 勾选标记
- 进度条
- 时间线
- 清晰的格子/布局

**品牌调性：**
- 专业
- 清晰
- 有序
- 高效

### 2. 生成的Prompt

**App图标：**
```
Clean minimalist calendar icon with checkmark symbol, organized grid layout representing schedule, professional blue and white color palette, sleek vector design, modern app icon aesthetic, time management visual metaphor, recognizable at small sizes, productivity-focused design

Negative: blurry, low quality, photorealistic, text, cluttered, gradient overflow, outdated design, cartoon style
```

**启动页：**
```
Welcoming productivity illustration, person viewing a beautifully organized calendar with completed tasks highlighted, soft morning light through window, warm yet professional atmosphere, generous whitespace, clean composition showing achievement and planning, modern flat illustration style with subtle depth, trust-inspiring tech aesthetic, onboarding storytelling visual

Negative: blurry, low quality, text, cluttered, generic stock photo, outdated illustration style, amateurish design
```

---

## 测试用例2：夜聊

## 输入信息
- 应用名称：夜聊
- 一句话描述：深夜EMO党的树洞
- 应用类型：社交App
- 简介：年轻人深夜语音聊天的社交平台

### 提取关键信息

**应用核心功能：**
- 深夜语音聊天
- 情感倾诉
- 社交陪伴

**功能亮点：**
- 深夜场景
- 树洞/倾听
- 年轻人社交
- 语音为主

**视觉元素：**
- 月亮/夜景
- 声音波形
- 人物轮廓
- 温暖的光
- 耳机/语音气泡

**品牌调性：**
- 温暖
- 私密
- 深夜感
- 年轻

### 生成的Prompt

**App图标：**
```
Minimalist moon and sound wave icon, night sky gradient background in deep blue and purple, warm amber glow representing late-night warmth, headphones or voice bubble element, sleek modern app icon, youthful and welcoming aesthetic, recognizable at small sizes

Negative: blurry, low quality, photorealistic, text, cluttered, daytime imagery, outdated design
```

**启动页：**
```
Cozy late-night scene illustration, young person wearing headphones in warm amber lighting, floating sound waves and connection lines, intimate and private atmosphere, emotional support visual metaphor, onboarding moment showing connection, modern digital illustration style with soft glow effects, purple and amber color palette

Negative: blurry, low quality, text, daytime scene, cluttered, generic stock photo, cold colors
```

**宣传海报：**
```
Cinematic late-night atmosphere, emotional connection visual, silhouettes of people talking with glowing connection lines, warm amber and deep purple tones, moon in background, dreamy and intimate mood, high-impact marketing composition, social connection metaphor, professional promotional illustration

Negative: blurry, low quality, watermark, cluttered, daytime, amateurish design
```

---

## 测试用例3：FitDaily

## 输入信息
- 应用名称：FitDaily
- 一句话描述：每天运动一点点
- 应用类型：健身App
- 简介：记录运动、制定计划、社交打卡

### 提取关键信息

**应用核心功能：**
- 运动记录
- 计划制定
- 社交打卡

**功能亮点：**
- 每日坚持
- 打卡成就感
- 运动可视化
- 社区激励

**视觉元素：**
- 运动姿态
- 进度/成就
- 流汗/努力
- 阳光/活力
- 勾选/完成

**品牌调性：**
- 活力
- 健康
- 积极
- 每日坚持

### 生成的Prompt

**App图标：**
```
Dynamic fitness icon with checkmark and motion lines, energetic orange and white color palette, person in athletic pose, achievement badge visual, modern flat design with energy, recognizable at small sizes, motivation-focused aesthetic

Negative: blurry, low quality, photorealistic, text, sedentary imagery, outdated design, dull colors
```

**启动页：**
```
Inspiring fitness illustration, person completing a workout with visible achievement, morning sunlight and energetic atmosphere, floating progress elements and celebration, clean composition with movement, vibrant orange and white color scheme, modern health illustration style, motivational onboarding moment

Negative: blurry, low quality, text, sedentary person, cluttered, generic stock photo, outdated illustration style
```

**宣传海报：**
```
High-energy fitness marketing visual, dynamic athlete in action pose, dramatic sunlight and motion blur, achievement and progress celebration, bold orange and dynamic composition, emotional motivation appeal, professional sports photography aesthetic, transformative journey visual

Negative: blurry, low quality, watermark, sedentary imagery, amateurish design, dull colors
```

---

## 测试结果评估

### 测试用例1（日程规划宝）
- ✅ 正确识别了效率工具的视觉语言（日历、勾选、网格）
- ✅ 使用了专业的蓝色调
- ✅ 负面提示词恰当

### 测试用例2（夜聊）
- ✅ 正确提取了"深夜"、"树洞"、"语音"等元素
- ✅ 使用了紫色和琥珀色的夜间配色
- ✅ 视觉隐喻恰当（月亮、声音波）

### 测试用例3（FitDaily）
- ✅ 正确识别了运动健身的活力元素
- ✅ 使用了橙色作为品牌色
- ✅ 体现了"每日"和"打卡"的概念

## 需要优化的地方

1. **负面提示词可以更精准** - 部分场景的negative可以增加更多场景相关的词
2. **可以增加更多风格变体** - 目前每个场景只生成一个版本
3. **场景可以更丰富** - 比如可以增加"功能介绍图"的场景
