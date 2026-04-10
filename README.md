# shuttle-bus

无界学城穿梭巴士实时查询技能。获取一号线、二号线顺时针（2C）、二号线逆时针（2A）的车辆实时 GPS 位置，估算到站时间，包含时刻表、完整线路和站点 POI 参考。

## 功能

- 从官方后台获取实时车辆位置（无需账号）
- 显示每辆车当前所在站点、行驶方向和速度
- 根据剩余站数估算到站时间（每站约 2.5 分钟）
- 内含时刻表、线路站序和各站周边信息

## 使用方式

### 方式一：Claude Code 插件

```bash
git clone https://github.com/a4001234567/shuttle-bus-skill
claude plugins marketplace add ./shuttle-bus-skill
claude plugin install shuttle-bus
```

安装后直接向 Claude 提问即可，例如：
- "下一班到清华信息楼的车还有多久？"
- "现在哪里有车？"
- "19:15 前能不能坐车到教学楼C栋？"

插件调用系统 `python3`，仅使用标准库，无需额外安装依赖。

### 方式二：独立 SKILL.md（适用于其他 AI 工具）

将仓库根目录的 `SKILL.md` 复制到你的 Agent 上下文或技能目录中。该文件完全自包含，底部内嵌了完整的 Python 数据获取脚本，无需额外文件。

适用于 Cursor、Windsurf、Continue 等支持加载 Markdown 技能/系统提示的工具。

## 数据来源

实时数据来自 `predict.ipubtrans.com`，即官方校园巴士小程序的同一后台。脚本自动匿名登录，无需账号或 API 密钥。

## 目录结构

```
shuttle-bus-skill/
  SKILL.md                   ← 独立版（内嵌脚本，适用于任意 AI 工具）
  README.md
  .claude-plugin/
    plugin.json              ← Claude Code 插件清单
  skills/
    shuttle-bus/
      SKILL.md               ← Claude Code 插件版（使用 {baseDir} 变量）
  scripts/
    fetch.py                 ← 数据获取脚本（插件版使用）
```

## 环境要求

- Python 3.6+（仅标准库：`urllib`、`json`、`sys`）
- 可访问 `predict.ipubtrans.com`
