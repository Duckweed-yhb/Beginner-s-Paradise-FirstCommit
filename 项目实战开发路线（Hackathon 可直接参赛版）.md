# 项目实战开发路线（Hackathon可直接参赛版）
> 项目全称：FocusStudy — 轻量化学生专注学习管理系统
> 项目定位：从完整版三端大项目独立拆分的最小MVP
>
> 拆分优势：
> 1. 100%独立可参赛，功能完整、逻辑闭环，符合黑客松提交标准
> 2. 所有代码可无缝迁移进最终三端完整版大项目
> 3. 轻量化、无冗余、新手友好、学习点充足，完美适配本次比赛评分规则（学习成长权重最高）

## 技术栈（精简适配版）
- 前端：Vue3 + Vite + Element Plus + ECharts
- 后端：Python FastAPI（轻量化极简服务）
- 存储：本地JSON + localStorage（无需复杂数据库，降低门槛）

> 整体开发周期：13天（剩余充足时间打磨+录视频+写文档）

## 阶段一：项目初始化与架构搭建（1~2天）
### 核心任务
1. 创建独立GitHub公开仓库（比赛专用）
2. 初始化Vue3前端项目、FastAPI后端项目
3. 规划项目目录、统一代码规范
4. 定义核心数据结构：学习任务、专注记录、时长统计

### 阶段产出
可运行空白项目架构，目录清晰，具备开发基础。

## 阶段二：核心前端功能开发（3~6天）
> 只做比赛核心功能，砍掉所有冗余模块

### 开发内容
#### 1. 学习任务管理模块
- 新增学习任务：科目、任务名称、截止时间、优先级
- 任务列表展示、完成/未完成状态切换
- 任务删除、修改

#### 2. 番茄专注计时器（核心亮点）
- 自定义专注时长、休息时长
- 开始/暂停/重置计时
- 计时结束提醒
- 自动绑定当前学习任务，记录专注数据

#### 3. 数据可视化统计页面
- 每日/每周专注时长统计
- 各科目学习占比图表展示
- 学习完成率展示

### 阶段产出
前端全部核心功能可独立运行，数据本地保存。

## 阶段三：轻量化后端接口开发（7~9天）
### 开发内容
1. FastAPI实现任务数据读写接口
2. 专注时长数据统计、汇总计算接口
3. 图表数据封装接口，向前端提供可视化数据

### 阶段产出
后端接口全部调试完成，前后端可正常联调。

## 阶段四：项目闭环优化 & 参赛材料准备（10~13天）
### 开发与准备内容
1. 功能全量测试、Bug修复
2. 页面UI美化、交互优化
3. 编写完整英文README（适配Devpost提交）
4. 录制3~5分钟Demo演示视频（比赛核心评分项）
5. 整理技术栈说明、项目亮点、学习收获

### 最终完整交付物（完全满足比赛提交要求）
1. 可运行前后端完整项目
2. 公开GitHub源码仓库（全程有提交记录，证明比赛期间开发）
3. 完整README运行部署文档
4. 3~5分钟项目演示视频
5. 项目介绍、技术说明、学习成长总结

# 项目拆分核心优势（适配本次比赛）
## 1. 完美匹配评分机制
比赛最高分权重是**学习成长30%**，本项目从零开发、涉及前端开发、数据可视化、前后端联调、数据逻辑处理，学习点极多，非常容易拿高分。

## 2. 完全符合比赛规则
所有核心逻辑为比赛周期内开发，无老旧成品复用风险，合规参赛。

## 3. 无缝对接超大三端项目
本次参赛的计时器、任务管理、数据统计模块，直接复制粘贴即可并入完整版大项目，不做无用功，比赛结束直接继续迭代全套九大模块。

## 4. 新手友好、稳拿奖、不翻车
功能聚焦、逻辑清晰、演示简单、文档好写，非常适配Beginner友好型黑客松，极易获得评委好感。

# 可直接用于Devpost的项目简介（备用）
**Elevator Pitch（一句话简介）**
> A lightweight student focus study management system with pomodoro timer, task management and learning data visualization to help students improve learning efficiency.

**项目简介**
> FocusStudy is a minimal but complete learning assistant system designed for students. It integrates task management, customizable pomodoro focus timer, and learning data statistics visualization. All data is saved locally and supports real‑time statistics of daily and weekly learning duration. This project helps students arrange study plans scientifically and improve self‑discipline, and it is also a reusable core module of the full‑stack three‑terminal personal toolbox project.
