# UMI 小红书 / 抖音 / GEO 方案制作 Skill

这是聚尤米 UMI 的小红书、抖音与 GEO 方案制作工作区整理版。

## 内容范围

- `.agents/skills/geo-sales-planner/`：GEO 销售方案 skill（流程、方法论、团队资料、需求确认模板、方案组件脚本）
- `AGENTS.md`、`CLAUDE.md`：智能体工作规范与项目配置
- `workspace/INDEX.md`：工作区资产索引
- `workspace/knowledge/sales_playbooks/`：GEO 多平台发布机制、小红书抖音 AI 协作流程、客户异议处理话术、团队销售资料
- `workspace/knowledge/case_assets/团队案例素材库_20260908/README.md`：团队案例素材说明（截图本身不上传）
- `workspace/scripts/generators/`、`workspace/scripts/scrapers/`：方案文档生成脚本与采集辅助脚本
- `workspace/archive/mslearn_labs/`：原项目 `Instructions/`、`Labfiles/` 学习资料归档

## 上传边界

本整理版不上传已制作的客户方案、诊断报告、提案、行动清单、演示文稿和 PDF/DOCX/HTML 成品。本地的 `workspace/projects/` 客户项目目录、`workspace/knowledge/design_templates/`，以及 `deliverables/`、`output/`、`tmp/` 和质检截图目录保持不变，但由 Git 忽略。

客户抓取导出（`workspace/archive/raw_captures/`）、团队案例截图（含微信群界面）、联系人截图、来源摘录和本机权限配置也不进入 Git 提交，避免泄露客户数据或本地环境信息。

完整边界记录见 `UPLOAD_INVENTORY.md`。

## 仓库名称

GitHub 仓库名使用 `umi-xiaohongshu-douyin-geo-scheme-skill`。用户给出的中文展示名为“umi小红书/抖音/GEO方案制作skill”；GitHub 仓库名不能包含 `/`，因此使用连字符规范化。

## 使用前检查

1. 复制 `.env.example` 为本地 `.env`，填写自己的环境变量。
2. 不要提交真实密钥、客户联系人、抓取原始数据或客户交付成品。
3. 运行脚本前，按脚本顶部说明安装对应的 Python 或 Node.js 依赖。
