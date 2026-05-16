# 0G APAC Hackathon — 最终提交操作清单

> ⏰ 截止: 2026-05-16 23:59 UTC+8 | 每一步都有详细指引

## 提交物状态总览

| # | 提交物 | 状态 | 需手动? | 预计时间 |
|---|--------|------|---------|----------|
| 1 | 项目名+描述 | ✅ | 否 | 0min |
| 2 | GitHub仓库(公开) | ✅ 已推 | 否 | 0min |
| 3 | 0G链上合约 | ⬜ | **是** | 12min |
| 4 | Demo视频(≤3min) | ⬜ | **是** | 20min |
| 5 | README文档 | ✅ | 否 | 0min |
| 6 | X推文 | ⬜ | **是** | 3min |
| 7 | HackQuest提交 | ⬜ | **是** | 10min |

---

## Step 1: 部署0G合约 (12min)

### 1a. 准备钱包 (3min)
- 打开MetaMask → 确认已添加0G Galileo测试网
- 网络参数:
  ```
  RPC URL:   https://evmrpc-testnet.0g.ai
  Chain ID:  16602
  货币符号:   0G
  区块浏览器: https://chainscan-galileo.0g.ai
  ```
- 钱包地址: `0xaA3b0911cE24121235A6c016338f7cec9B0C8045`

### 1b. 确认测试币 (2min)
- 打开 https://faucet.0g.ai/
- 粘贴钱包地址 → 领取
- 确认余额 > 0.01 0G

### 1c. 执行部署 (5min)
```powershell
cd "x:\workspace\Paper\competitions\0G-APAC-Hackathon\code"
$env:0G_PRIVATE_KEY="你的私钥_不带0x前缀"
python deploy.py
```

预期输出:
```
Deployer: 0xaA3b0911cE24121235A6c016338f7cec9B0C8045
Balance: xxx.xxxx 0G
TX Hash: 0xabcd1234...
Contract Address: 0x1234567890abcdef...
Explorer: https://chainscan-galileo.0g.ai/address/0x1234567890abcdef
```

### 1d. 验证+截图 (2min)
- 打开Explorer链接 → 确认状态Success
- **截图保存** (Demo视频和提交用)
- 记录合约地址 → 填入HackQuest提交表

---

## Step 2: 录制Demo视频 (20min)

### 准备工作
- 安装Loom (https://www.loom.com/) 或用OBS
- 打开3个浏览器Tab:
  1. Gradio UI: `VERIVISION_DEMO=1 python gradio_app.py` → http://localhost:7860
  2. 0G Explorer: https://chainscan-galileo.0g.ai/address/{合约地址}
  3. GitHub: https://github.com/tayiic/VeriVision-0G

### 录制流程 (按demo-video-script.md)
1. **0:00-0:20 Hook** — "AI vision models lie. VeriVision catches them."
2. **0:20-0:50 Problem** — 展示VLM幻觉示例
3. **0:50-1:40 Solution** — Gradio UI上传图片→看结果
4. **1:40-2:20 0G Integration** — 展示TX hash + Explorer
5. **2:20-2:45 Smart Contract** — 展示合约+getHallucinationRate
6. **2:45-3:00 CTA** — Logo + #0GHackathon #BuildOn0G

### 上传
- Loom上传 → 获取公开链接
- 或YouTube上传(设为Unlisted) → 获取链接

---

## Step 3: 发布X推文 (3min)

### 推文内容(复制即用)

**英文版**:
```
🚀 VeriVision — Decentralized VLM Hallucination Verifier on @0G_labs

AI vision models hallucinate 30-40% of the time. VeriVision catches them using cross-model verification + immutable on-chain audit logs.

✅ VLM-A describes → VLM-B verifies
✅ Results stored on 0G Storage (immutable)
✅ Smart contract on 0G Galileo testnet

Built for #0GHackathon #BuildOn0G

🔗 GitHub: https://github.com/tayiic/VeriVision-0G
🎥 Demo: [视频链接]

@0g_CN @0g_Eco @HackQuest_
```

**中文版(备用)**:
```
🚀 VeriVision — 基于0G的去中心化VLM幻觉检测器

AI视觉模型30-40%的时间在"说谎"。VeriVision用跨模型验证+链上不可篡改审计来捕捉幻觉。

✅ VLM-A描述 → VLM-B质疑验证
✅ 结果存储在0G Storage（不可篡改）
✅ 智能合约部署在0G Galileo测试网

#0GHackathon #BuildOn0G

🔗 https://github.com/tayiic/VeriVision-0G
🎥 [视频链接]

@0g_CN @0g_Eco @HackQuest_
```

### 发布步骤
1. 登录X (Twitter)
2. 粘贴推文内容
3. 替换[视频链接]为实际链接
4. 发布
5. 复制推文链接 → 填入HackQuest提交表

---

## Step 4: HackQuest最终提交 (10min)

### 提交地址
https://www.hackquest.io/en/hackathons/0G-APAC-Hackathon

### 填写内容

| 字段 | 值 |
|------|-----|
| 项目名称 | VeriVision |
| 一句话描述 | Decentralized VLM Hallucination Verifier with 0G Storage & Chain |
| GitHub仓库 | https://github.com/tayiic/VeriVision-0G |
| 合约地址 | (Step 1部署后填入) |
| Explorer链接 | https://chainscan-galileo.0g.ai/address/{合约地址} |
| Demo视频 | (Step 2录制后填入链接) |
| X推文链接 | (Step 3发布后填入链接) |
| 赛道 | Track 1 (Agentic Infrastructure) + Track 4 (Web 4.0) |
| AI使用声明 | 已在README中声明 |

---

## 完成后检查

- [ ] 合约在Explorer上可见且状态Success
- [ ] Demo视频可正常播放
- [ ] 推文已发布且包含正确标签
- [ ] HackQuest提交表所有字段已填写
- [ ] 提交确认页面截图保存

## 紧急联系

- 0G Discord: https://discord.gg/0g
- HackQuest支持: 通过官网联系
