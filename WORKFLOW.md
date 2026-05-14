# 0G APAC Hackathon — VeriVision 项目工作流

> **可复用模板**: 下次参加Web3/AI黑客松时，复制此文件改项目名即可
> **通用方法论**: `competitions/WORKFLOW.md`
> **知识库**: `KalyceBrain/wiki/topics/Web3-AI黑客松竞赛方法论与AI工作流.md`

## 项目快照

| 属性 | 值 |
|------|-----|
| 项目名 | VeriVision |
| 一句话 | VLM幻觉检测器 + 0G链上不可篡改审计 |
| 赛道 | Track 1 (Agentic Infrastructure) + Track 4 (Web 4.0) |
| 截止 | 2026-05-16 23:59 UTC+8 |
| 奖金 | $150K总池 / $45K冠军 |
| 技术栈 | Python + Web3.py + Solidity + Gradio + 0G Storage/Chain |
| 状态 | 🟡 开发完成，待提交 |

## FSM 状态机

```
DISCOVER → REGISTER → SELECT → ARCHITECT → DEVELOP → TEST → DEMO → SUBMIT → RETROSPECT
                                        ✓         ✓       ✓      ⬜      ⬜       ⬜
```

当前: **DEMO** 阶段

## 阶段执行记录

### Phase 0-1: 发现+报名 ✅
- 日期: 2026-05-09
- 产出: KalyceBrain竞赛跟踪页

### Phase 2: 选题 ✅
- 日期: 2026-05-10
- 决策: VLM幻觉检测 + 0G链上验证
- 理由: 与论文VDA-MCD框架双向增益，技术壁垒高，差异化强
- 产出: 无独立文档（在README中体现）

### Phase 3: 架构 ✅
- 日期: 2026-05-11
- 架构: VLM-A描述 → VLM-B验证 → 幻觉报告 → 0G Storage存证 → 链上合约记录
- 产出: [README.md](../README.md) 架构图

### Phase 4: 开发 ✅
- 日期: 2026-05-12 ~ 05-13
- 产出:
  - [verivision.py](../code/verivision.py) — 核心检测+0G集成
  - [VeriVisionRegistry.sol](../contracts/VeriVisionRegistry.sol) — 链上合约
  - [gradio_app.py](../code/gradio_app.py) — Web UI
  - [deploy.py](../code/deploy.py) — 合约部署脚本
- commit: v001 (初始), v002 (AI声明+清单更新)

### Phase 5: 测试 ✅
- 日期: 2026-05-13
- 状态: 核心链路可运行，Gradio UI可启动

### Phase 6: Demo ⬜ ← 当前
- 目标:
  - [ ] Loom录制3分钟Demo视频
  - [ ] 视频上传获取公开链接
- 依赖: 无（代码已就绪）
- Demo模式: `VERIVISION_DEMO=1 python gradio_app.py` (无需API密钥)

### Phase 7: 提交 ⬜
- 提交物清单（7项必填）:
  - [x] 项目名+一句话描述
  - [ ] GitHub公开仓库 (tayiic/VeriVision-0G)
  - [ ] 0G链上合约地址 + Explorer链接
  - [ ] Demo视频(≤3min, YouTube/Loom)
  - [x] README文档(英文)
  - [ ] X推文(#0GHackathon #BuildOn0G @0G_labs @0g_CN @0g_Eco @HackQuest_)
  - [x] AI使用声明(已在README中)
- 提交地址: https://www.hackquest.io/en/hackathons/0G-APAC-Hackathon

### Phase 8: 复盘 ⬜
- 待赛后执行

## 提交时间线

```
5/14 今天  ──── 准备提交材料（本文件+清单）
5/15 明天  ──── Loom录视频 + 0G部署 + GitHub推送
5/16 截止日 ──── X推文 + HackQuest最终提交 (23:59 UTC+8)
```

## 手动操作清单（AI无法自动完成）

| # | 操作 | 工具 | 状态 | 预计时间 |
|---|------|------|------|----------|
| 1 | GitHub创建仓库 + 推送代码 | git push | ✅ 已完成 | 5min |
| 2 | **0G合约部署** (详见下方) | MetaMask + deploy.py | ⬜ 待执行 | 12min |
| 3 | Loom录制3分钟Demo视频 | loom.com | ⬜ 待执行 | 20min |
| 4 | 发布X推文 | x.com | ⬜ 待执行 | 3min |
| 5 | HackQuest填写提交表 | hackquest.io | ⬜ 待执行 | 10min |

---

## Step 2: 0G合约部署（详细流程）

### 2a. 准备钱包 (3min)

**推荐工具**: MetaMask 浏览器扩展

> MetaMask选择: Chrome和Firefox都支持。**Chrome的DApp兼容性略好**（大部分DeFi/DApp优先适配Chrome），但Firefox隐私保护更强。实际使用差异不大，选你常用的浏览器即可。

**操作步骤**:
1. 安装MetaMask: https://metamask.io/
2. 创建/导入钱包（⚠️ 用新账户，不要用主网钱包）
3. 在MetaMask中**手动添加0G Galileo测试网络**:

```
网络名称:    0G Galileo Testnet
RPC URL:     https://evmrpc-testnet.0g.ai
Chain ID:    10062
货币符号:     0G
区块浏览器:   https://chainscan-galileo.0g.ai
```

4. 切换到该网络，复制钱包地址 `0x...`

### 2b. 获取测试代币 (2min)

1. 打开 https://faucet.0g.ai/
2. 粘贴钱包地址 → 领取测试币（免费）
3. 部署一次约需 0.001-0.01 0G gas费

### 2c. 部署合约 (5min)

**方法A — 命令行部署（推荐）**:
```powershell
cd "x:\workspace\Paper\competitions\0G-APAC-Hackathon\code"
$env:0G_PRIVATE_KEY="你的私钥_不带0x前缀"
python deploy.py
```

**预期输出**:
```
Deployer: 0xYourAddress...
Balance: xxx.xxxx 0G
TX Hash: 0xabcd1234...
Contract Address: 0x1234567890abcdef...
Explorer: https://chainscan-galileo.0g.ai/address/0x1234567890abcdef
Deployment info saved to code/deploy_info.json
```

**方法B — Remix备用方案**（如果命令行有问题）:
1. 打开 https://remix.ethereum.org/
2. 新建文件 `VeriVisionRegistry.sol`，粘贴 contracts/ 目录下的内容
3. Solidity Compiler → Compile
4. Deploy & Run Transactions → Environment选 "Injected Provider - MetaMask"
5. 点击 Deploy → MetaMask确认交易

### 2d. 验证+记录 (2min)

1. 打开 https://chainscan-galileo.0g.ai/ 搜索合约地址
2. 确认状态为 Success
3. **截图保存**（Demo视频用）
4. 记录以下信息:

| 字段 | 值 | HackQuest必填? |
|------|-----|---------------|
| Contract Address | `0x...` | ✅ 是 |
| Explorer URL | `https://chainscan-galileo.0g.ai/address/0x...` | ✅ 是 |
| Deploy TX Hash | `0x...` | 备查 |

### 安全提醒 🔴

- **只用测试网专用钱包**，不要用主网私钥
- 建议新建一个MetaMask账户专门用于测试
- 部署完成后可废弃该测试账户

### 当前部署信息

| 字段 | 值 |
|------|-----|
| 钱包地址 | `0xaA3b0911cE24121235A6c016338f7cec9B0C8045` |
| Chain ID | **10062** |
| 状态 | ✅ 测试币已领取，待部署 |

## 合规检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| AI使用声明 | ✅ | README中已声明 |
| 代码原创性 | ✅ | 核心逻辑自主设计 |
| 0G集成深度 | ✅ | Storage + Chain双组件 |
| 非换皮(reskin) | ✅ | 原创架构+原创合约逻辑 |
| commit记录 | ✅ | v001+v002渐进式 |

## 关键链接

- 官方: https://www.hackquest.io/en/hackathons/0G-APAC-Hackathon
- 0G Faucet: https://faucet.0g.ai/
- 0G Explorer: https://chainscan-galileo.0g.ai/
- 0G Docs: https://docs.0g.ai/
- Loom: https://www.loom.com/
