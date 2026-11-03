# 上传清单

盘点日期：2026-09-06

## 已纳入上传副本

- 方案生成和排版辅助脚本（Python / JavaScript）
- GEO 方法论、销售话术和 AI 协作流程 Markdown
- 原项目 `Instructions/`、`Labfiles/`、`.github/` 资料
- 可公开复用的示例配置、示例数据和课程媒体

## 明确排除

- 根目录以及 `deliverables/`、`output/` 中已经制作完成的客户方案
- PDF、DOCX、PPTX、HTML 等客户交付成品及其渲染版本
- `tmp/`、`_qa_report/`、`_qa_rosemary/` 等临时和质检产物
- `xhs_yh_capture/`、`xiyu_research/` 等客户抓取原始资料
- 联系人截图、来源摘录和本地权限配置
- `.env`、访问令牌、密钥和其他机器专属配置

## 当前副本状态

本地整理副本初始复制 144 个文件，约 6.7 MB。客户抓取/联系人文件仍可能存在于整理副本的物理目录中，但已由 `.gitignore` 排除，不会进入 Git 提交；原工作区文件不删除、不移动。

## 2026-11-03 工作区重组同步

- 根目录脚本迁入 `workspace/scripts/generators/`、`workspace/scripts/scrapers/`
- 话术与方法论 Markdown 迁入 `workspace/knowledge/sales_playbooks/`
- `Instructions/`、`Labfiles/` 迁入 `workspace/archive/mslearn_labs/`
- 新增 skill 参考文件（需求确认模板、输出组件说明）和 `proposal_kit/` 方案组件脚本
- 继续排除：`workspace/projects/`（客户方案源稿与成品）、`workspace/archive/raw_captures/`（原始抓取）、`workspace/knowledge/case_assets/` 下的截图、`workspace/knowledge/design_templates/`（PDF 成品），以及春生备婚素材 zip（405MB，超过 GitHub 单文件 100MB 上限）

## 上传前复核

```powershell
git status --short --ignored
git diff --cached --name-only
```

确认提交列表中没有客户交付成品、原始抓取数据、联系人材料和真实凭据后，再执行推送。
