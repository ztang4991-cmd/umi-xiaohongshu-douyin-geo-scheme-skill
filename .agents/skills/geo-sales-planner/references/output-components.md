# 结构化输出组件规范

提案要让客户 5 分钟看懂结论、30 分钟看懂逻辑。所以正文默认用组件表达，只有组件放不下的解释才写段落。

渲染器：`scripts/proposal_kit/build.py`（Markdown → HTML → PDF）。完整可运行示例：`scripts/proposal_kit/example.md`。

## 硬规则

1. 每个内容页至少 1 个结构化组件（组件、表格或清单），最多 4 个，避免挤爆版面。
2. 正文段落不超过 3 行；超过就拆成卡片、步骤或表格。
3. 每个数字都要写清来源和日期：`[公开抽样·日期]`、`[OTA公开快照·日期]`、`[客户提供·待核实]` 等（定义见 team-profile.md“证据等级约定”）。
4. 封面固定：一句话链路（如“被搜到 → 被咨询 → 被预订 → 被入住”）+ 4 个数据卡。
5. 出现“比较、流程、时间、选择”就用对应组件，不用段落描述。
6. 占位或估算数字必须标“示例”或“待确认”，不写成事实。
7. 构建时溢出检查不通过（内容被裁切）就拆页或删减，不缩小字号硬塞。

## 组件目录

源稿里用 ```` ```组件名 ```` 代码块写 JSON。字符串支持行内 Markdown（`**加粗**`）和证据标签。

| 组件 | 表达什么 | 必填字段 | 默认章节 |
| --- | --- | --- | --- |
| `cover` | 封面：标题、链路、4 个数据卡 | `title`、`chain`、`stats[{value,label}]` | 封面 |
| `outline` | 提案大纲：每章一句话结论 | `items[{no,title,point}]` | 00 大纲 |
| `kpi` | 关键数字卡 | `items[{value,label,note}]`，可选 `cols` | 01 / 09 |
| `cards` | 理由、证据、风险、意图分类 | `items[{title,body,tag,level}]`；`level` 取 fact / infer / verify / risk | 01 / 02 / 06 / 10 |
| `decision` | 今天要定的事 + 店方提供清单 | `title`、`body`、`checklist[]` | 01 |
| `steps` | 编号动作（如“账号先改这 4 处”） | `items[{title,body}]` | 02 / 06 |
| `compare` | 少说什么 → 多拍什么 | `from{label,items[]}`、`to{label,items[]}` | 04 |
| `hbar` | 横向条形图（距离、占比、数量） | `items[{label,value}]`、`unit`，可选 `max` | 03 |
| `funnel` | 转化漏斗 + 每段口径定义 | `stages[]`，可选 `defs[{term,def}]`、`highlight` | 09 |
| `journey` | 客户决策路径 | `steps[]` | 05 |
| `timeline` | 90 天甘特节奏 + 节点 | `phases[{label,start,end}]`、`milestones[{day,label}]`，可选 `lanes` | 08 |
| `calendar` | 周内容计划网格 | `weeks[{week,items[{title,format,source}]}]` | 07 |
| `checkpoints` | 第 30/60/90 天：看什么、定什么 | `items[{day,look,decide}]` | 09 |
| `rules` | 继续 / 调整 / 暂停扩量规则 | `items[{key,label,body}]`；`key` 取 go / adjust / stop | 09 |
| `tiers` | 合作档位 A/B/C | `items[{name,fit,scope,exclude,fee,recommended}]` | 10 |
| `formula` | 决策公式 / 测算链 | `terms[]`、`result`，可选 `note` | 01 / 09 |
| `case` | 团队案例截图网格 | `items[{title,image,caption}]` | 11 |

原生 Markdown 也会被样式化：表格（分工矩阵、A/B 测试、竞对清单）、`>` 引用（洞察提示框）、`- [ ]` 清单（确认项）。

## 版式语法

- 每个 `# ` 一级标题开一页；标题写成 `# 03 10公里内的竞对`，编号和标题会分开排版。
- 含 `cover` 组件的页是封面，不显示页眉。
- 并排两栏：

```text
:::cols
左栏内容
:::col
右栏内容
:::
```

- 源稿开头用 front matter 写页眉信息：`client`、`title`、`date`、`disclaimer`。

## 章节 → 组件对照

| 章节 | 默认组件 |
| --- | --- |
| 封面 | `cover` |
| 00 提案大纲 | `outline` |
| 01 合作建议 | `kpi` + `cards` + `decision` |
| 02 账号现状诊断 | 表格（笔记互动快照）+ `cards`（缺什么信息）+ `steps`（先改哪几处） |
| 03 竞对分布 | `hbar`（距离）+ 表格（线上切入点）+ 口径说明 |
| 04 竞对线上动作 | `cards`（看到的动作）+ `compare`（应对） |
| 05 客群与决策路径 | 表格（人群/场景/证据/切入）+ `journey` |
| 06 搜索布局 | `cards`（五类搜索意图）+ `steps`（一篇笔记怎么写） |
| 07 内容计划 | `calendar` |
| 08 双方分工与节奏 | `timeline` + 表格（分工矩阵） |
| 09 效果衡量 | `funnel` + `checkpoints` + `rules` + 表格（A/B 测试） |
| 10 合作档位 | `tiers` + `cards`（风险，`level: risk`） |
| 11 团队案例 | `case` |
| 12 确认清单 | `- [ ]` 清单 |

## 反模式

- 页面只有大段文字，或只有装饰图没有数据。
- 用 `funnel` 画不是先后转化关系的东西。
- `timeline` 为了显得忙而排满，第 2、3 阶段写死具体选题（应按上一阶段数据调整）。
- 引用评分、点评量、粉丝数却不写日期。
- 把 A/B/C 档位写成价格表；报价面谈确认，提案只写范围和费用组成。
