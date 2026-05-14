# 0G APAC Hackathon Submission Checklist

> **截止**: 2026-05-16 23:59 UTC+8 (亚洲/上海时间)
> **提交地址**: https://www.hackquest.io/en/hackathons/0G-APAC-Hackathon

## 提交物状态

| # | 提交物 | 状态 | 说明 |
|---|--------|------|------|
| 1 | GitHub仓库链接 | ⬜ 待创建 | 需创建公开仓库 tayiic/VeriVision-0G |
| 2 | 0G主网合约地址 | ⬜ 待部署 | 部署VeriVisionRegistry到Galileo测试网 |
| 3 | Demo视频(≤3分钟) | ⬜ 待录制 | YouTube/Loom公开链接 |
| 4 | README.md | ✅ 已完成 | 项目介绍+架构+使用说明 |
| 5 | X平台推文 | ⬜ 待发布 | #0GHackathon #BuildOn0G + @0G_labs |

## 手动操作步骤

### Step 1: 创建GitHub仓库 (5min)
```bash
# 在GitHub上创建公开仓库
# 仓库名: VeriVision-0G
# 描述: Decentralized VLM Hallucination Verifier on 0G
# 然后推送代码:
cd x:\workspace\Paper\competitions\0G-APAC-Hackathon
git init
git remote add origin git@github.com:tayiic/VeriVision-0G.git
git add .
git commit -m "v001: VeriVision - Decentralized VLM Hallucination Verifier"
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
export 0G_PRIVATE_KEY=your_private_key
python deploy.py
# 记录输出的合约地址和Explorer链接
```

### Step 4: 录制Demo视频 (30min)
1. 按照 docs/demo-video-script.md 的脚本
2. 使用OBS/Loom录屏
3. 上传到YouTube(非公开)或Loom
4. 更新README中的视频链接

### Step 5: 发布X推文 (5min)
推文内容:
```
👁️ VeriVision — Catching AI Vision Hallucinations on @0G_labs

When VLMs "see" things that aren't there, VeriVision catches them using cross-model verification + immutable on-chain audit logs on 0G Storage.

Demo: [YouTube链接]
Repo: [GitHub链接]

#0GHackathon #BuildOn0G @HackQuestHQ
```

### Step 6: 在HackQuest提交 (10min)
1. 登录 https://www.hackquest.io/
2. 进入 0G APAC Hackathon 页面
3. 填写提交表单:
   - Project Name: VeriVision
   - GitHub: https://github.com/tayiic/VeriVision-0G
   - 0G Contract: [部署后的合约地址]
   - Demo Video: [YouTube/Loom链接]
   - Track: Track 1 (Agentic Infrastructure) + Track 4 (Web 4.0)
   - Description: VLM hallucination detection with immutable on-chain verification on 0G

## 时间预算

| 步骤 | 预计时间 | 最晚完成 |
|------|----------|----------|
| GitHub仓库 | 5min | 5/16 20:00 |
| 0G测试网部署 | 15min | 5/16 21:00 |
| Demo视频 | 30min | 5/16 22:00 |
| X推文 | 5min | 5/16 22:30 |
| HackQuest提交 | 10min | 5/16 23:00 |
| **缓冲** | **1h** | **5/16 23:59** |

## 关键链接

- HackQuest提交: https://www.hackquest.io/en/hackathons/0G-APAC-Hackathon
- 0G Faucet: https://faucet.0g.ai/
- 0G Explorer: https://chainscan-galileo.0g.ai/
- 0G Docs: https://docs.0g.ai/
