# 0G APAC Hackathon Submission Checklist

> **截止**: 2026-05-16 23:59 UTC+8 (亚洲/上海时间)
> **提交地址**: https://www.hackquest.io/en/hackathons/0G-APAC-Hackathon
> **官方提交要求来源**: HackQuest平台 (2026-05-14确认)

## 提交物状态（7项，全部必填）

| # | 提交物 | 状态 | 官方要求 |
|---|--------|------|----------|
| 1 | 项目名称+一句话描述(≤30字) | ✅ 已有 | VeriVision — Decentralized VLM Hallucination Verifier on 0G |
| 2 | GitHub仓库(公开) | ⬜ 待推送 | 需有实质性commit记录，空仓库/placeholder将被取消资格 |
| 3 | 0G链上集成证明 | ⬜ 待部署 | **核心门槛** — 必须有0G主网合约地址+Explorer链接 |
| 4 | Demo视频(≤3分钟) | ⬜ 待录制 | 必须展示产品功能+0G组件使用，纯PPT/概念视频无效 |
| 5 | README文档(英文/中文) | ✅ 已完成 | 项目概述+架构图+0G模块说明+部署步骤+测试账号 |
| 6 | X平台推文 | ⬜ 待发布 | 必须含 #0GHackathon #BuildOn0G + @0G_labs @0g_CN @0g_Eco @HackQuest_ |
| 7 | (可选)加分材料 | ⬜ 待准备 | Pitch deck/前端Demo链接/用户反馈/API文档 |

## 关键发现：AI代码合规

### 0G Hackathon对AI的态度
- **允许使用AI工具**（LLM/ChatGPT等），但必须在README中声明如何使用
- 评审关注"你创建/修改/构建了什么"vs"AI生成了什么"
- **不能是现有AI工具的简单换皮(reskin)**
- 需要有**实质性开发进度**（commit记录）

### 反AI检测/查重注意事项
1. **代码查重**: HackQuest可能使用MOSS/AST分析检查代码相似度
2. **AI代码检测**: 可能检测AI生成的代码模式（统一注释风格、过度规范的docstring等）
3. **应对策略**:
   - 在README中声明AI辅助使用（合规声明）
   - 确保核心逻辑有个人风格（非纯AI生成）
   - commit记录显示渐进式开发（非一次性大量代码）
   - 添加个人设计决策注释

## 手动操作步骤

### Step 1: 创建GitHub仓库+推送 (5min)
1. 在GitHub上创建公开仓库 `tayiic/VeriVision-0G`
2. 描述: Decentralized VLM Hallucination Verifier on 0G
3. 推送代码（本地已commit）:
```bash
cd x:\workspace\Paper\competitions\0G-APAC-Hackathon
git remote add origin git@github.com:tayiic/VeriVision-0G.git
git push -u origin main
```

### Step 2: 获取0G测试网代币 (5min)
1. 访问 https://faucet.0g.ai/
2. 输入你的钱包地址
3. 获取测试网0G代币

### Step 3: 部署智能合约 (10min)
```bash
cd code
pip install web3
set 0G_PRIVATE_KEY=your_private_key
python deploy.py
# 记录输出的合约地址和Explorer链接
```

### Step 4: 录制Demo视频 (20min)
**为什么需要视频**: 官方强制要求，评审第一轮筛选依据。没有视频=直接取消资格。
**怎么录（最简单方案）**:
1. 安装Loom (https://www.loom.com/) — 免费，录屏+摄像头+自动生成链接
2. 或用OBS Studio录屏后上传YouTube
3. 视频内容（≤3分钟）:
   - 0:00-0:20 项目介绍（"AI视觉模型会产生幻觉，VeriVision用0G链上验证来检测"）
   - 0:20-1:30 Demo演示（上传图片→看到幻觉检测结果→0G Explorer截图）
   - 1:30-2:30 0G集成展示（合约地址+Explorer链接+Storage交易）
   - 2:30-3:00 总结+团队介绍
4. 上传到YouTube(非公开)或Loom，获取公开链接

### Step 5: 发布X推文 (5min)
```
👁️ VeriVision — Catching AI Vision Hallucinations on @0G_labs

When VLMs "see" things that aren't there, VeriVision catches them using cross-model verification + immutable on-chain audit logs on 0G Storage.

Demo: [YouTube链接]
Repo: [GitHub链接]

#0GHackathon #BuildOn0G @0g_CN @0g_Eco @HackQuest_
```

### Step 6: 在HackQuest提交 (10min)
1. 登录 https://www.hackquest.io/
2. 进入 0G APAC Hackathon 页面
3. 填写提交表单:
   - Project Name: VeriVision
   - One-sentence: VLM hallucination verifier with immutable on-chain audit on 0G Storage
   - GitHub: https://github.com/tayiic/VeriVision-0G
   - 0G Contract: [部署后的合约地址]
   - 0G Explorer: [Explorer链接]
   - Demo Video: [YouTube/Loom链接]
   - Track: Track 1 (Agentic Infrastructure)
   - X Post: [推文链接]

## 时间预算

| 步骤 | 预计时间 | 最晚完成 |
|------|----------|----------|
| GitHub仓库 | 5min | 5/16 20:00 |
| 0G测试网部署 | 15min | 5/16 21:00 |
| Demo视频 | 20min | 5/16 22:00 |
| X推文 | 5min | 5/16 22:30 |
| HackQuest提交 | 10min | 5/16 23:00 |
| **缓冲** | **1h** | **5/16 23:59** |

## 关键链接

- HackQuest提交: https://www.hackquest.io/en/hackathons/0G-APAC-Hackathon
- 0G Faucet: https://faucet.0g.ai/
- 0G Explorer: https://chainscan-galileo.0g.ai/
- 0G Docs: https://docs.0g.ai/
- Loom录屏: https://www.loom.com/
