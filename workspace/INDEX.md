# 工作区全局资产索引 (Workspace Master Index)

> **Agent 快速导航指南**：接手任何任务时，请先查阅本文件定位已有客户资产、团队案例与脚本工具，严禁全盘盲搜。

## 一、 目录架构说明

| 目录路径 | 用途定位 | Agent 读写规范 |
| --- | --- | --- |
| `workspace/projects/<客户名>/` | 客户项目专属目录（含需求确认单、Markdown 源稿、PDF/DOCX 成品、专属构建脚本） | **主工作区**：优先读取对应客户的 `INDEX.md`，新项目在此新建同名文件夹 |
| `workspace/knowledge/case_assets/` | 团队正式案例素材库（春生、祥和、悦哉、牧云台及补充案例） | **只读引用**：按 `README.md` 口径引用，兼容原路径 `UMI项目整理/02_客户数据与素材/素材/团队案例素材库_20260908/` |
| `workspace/knowledge/sales_playbooks/` | 销售话术、异议处理、GEO 发布机制、团队案例册源稿 | **知识底座**：撰写话术、回复客户异议或构建方法论时优先检索 |
| `workspace/scripts/generators/` | 历史沉淀的 PDF/DOCX/PPT 生成脚本（Python / Node.js） | **复用参考**：制作新文档时优先参考已有版式脚本，不在根目录堆放新脚本 |
| `workspace/scripts/scrapers/` | 小红书/页面采集与解析辅助脚本 | **工具脚本**：调研采集时按需调用 |
| `workspace/archive/` | 历史原始抓取快照 (`raw_captures`) 与微软课程归档 (`mslearn_labs`) | **冷归档区**：默认不纳入常规检索，除非用户点名调取原始抓取 JSON |

## 二、 核心知识与话术库 (`workspace/knowledge/`)

### 2.1 销售话术与方法论 (`workspace/knowledge/sales_playbooks/`)
- `GEO产品_多平台发布机制详解.md`
- `小红书抖音AI协作工作流.md`
- `麓山宴签约案例_朋友圈获客文案.md`
- `客户异议处理_AI投毒与审核机制专业回复.md`
- `客户异议处理_如何通过公众号官网看案例_四维度回复.md`
- `客户异议处理_截图版话术_公众号官网问题.md`
- `客户异议处理_没有百度官网和小程序的专业回复话术.md`
- `团队销售资料/婚嫁行业_抖音小红书代运营与全案营销销售话术_团队阅读版_20260909.md`
- `团队销售资料/宴会场地小红书合作案例册_20260924.md`

### 2.2 团队案例素材库 (`workspace/knowledge/case_assets/团队案例素材库_20260908/`)
- 索引说明：`workspace/knowledge/case_assets/团队案例素材库_20260908/README.md`
- 正式案例：`01_春生`（三账号：漂亮饭号、婚宴号、个人号“一颗葡萄”）、`02_祥和`、`03_悦哉`、`04_牧云台`、`05_介个院子`（团建号）
- “一颗葡萄”已于 2026-11-03 确认为春生个人号，原 `05_补充案例_一颗葡萄_待确认` 目录已并入 `01_春生`

## 三、 客户项目清单 (`workspace/projects/`)

| 客户/项目名称 | 路径 | 源稿数 | 成品文档数 | 脚本数 | 素材数 |
| --- | --- | :---: | :---: | :---: | :---: |
| **_其他与通用方案** | `workspace/projects/_其他与通用方案/` | 1 | 2 | 0 | 1 |
| **三圣乡_余生** | `workspace/projects/三圣乡_余生/` | 1 | 3 | 0 | 0 |
| **东方莎莉花园** | `workspace/projects/东方莎莉花园/` | 1 | 2 | 0 | 0 |
| **东莞美集婚纱摄影** | `workspace/projects/东莞美集婚纱摄影/` | 1 | 1 | 0 | 0 |
| **介个院子** | `workspace/projects/介个院子/` | 5 | 3 | 2 | 8 |
| **佛山南海和华希尔顿逸林酒店** | `workspace/projects/佛山南海和华希尔顿逸林酒店/` | 1 | 1 | 0 | 1 |
| **卡萨四季庭院餐厅** | `workspace/projects/卡萨四季庭院餐厅/` | 1 | 5 | 0 | 0 |
| **厦门天鹅大酒店** | `workspace/projects/厦门天鹅大酒店/` | 0 | 1 | 0 | 0 |
| **可悦私房菜** | `workspace/projects/可悦私房菜/` | 0 | 3 | 0 | 0 |
| **成都企业绿植租赁** | `workspace/projects/成都企业绿植租赁/` | 0 | 2 | 0 | 0 |
| **成都阿姨来了** | `workspace/projects/成都阿姨来了/` | 1 | 1 | 0 | 0 |
| **新都喜遇言庭宴会中心** | `workspace/projects/新都喜遇言庭宴会中心/` | 2 | 5 | 0 | 0 |
| **春生** | `workspace/projects/春生/` | 4 | 8 | 1 | 24 |
| **柠檬花院** | `workspace/projects/柠檬花院/` | 3 | 1 | 1 | 5 |
| **沐楠雅居** | `workspace/projects/沐楠雅居/` | 1 | 2 | 0 | 0 |
| **牧云台** | `workspace/projects/牧云台/` | 0 | 4 | 0 | 0 |
| **玛瑞莎摄影** | `workspace/projects/玛瑞莎摄影/` | 3 | 1 | 0 | 0 |
| **福气东来酒店** | `workspace/projects/福气东来酒店/` | 0 | 1 | 0 | 0 |
| **羲和轩_拾光管家** | `workspace/projects/羲和轩_拾光管家/` | 1 | 1 | 0 | 0 |
| **莫奈花园** | `workspace/projects/莫奈花园/` | 1 | 1 | 1 | 8 |
| **见山欢喜** | `workspace/projects/见山欢喜/` | 1 | 1 | 1 | 0 |
| **言度奢石** | `workspace/projects/言度奢石/` | 0 | 5 | 0 | 0 |
| **豪联建材** | `workspace/projects/豪联建材/` | 1 | 2 | 0 | 0 |
| **迷迭香农庄** | `workspace/projects/迷迭香农庄/` | 1 | 2 | 0 | 0 |
| **那年花开南法庄园** | `workspace/projects/那年花开南法庄园/` | 1 | 1 | 0 | 0 |
| **都江堰明智上春假日酒店** | `workspace/projects/都江堰明智上春假日酒店/` | 0 | 1 | 0 | 0 |
| **雅禾婚礼** | `workspace/projects/雅禾婚礼/` | 1 | 2 | 0 | 0 |
| **青城山远山私汤民宿** | `workspace/projects/青城山远山私汤民宿/` | 2 | 1 | 1 | 0 |
| **青楹在乡野** | `workspace/projects/青楹在乡野/` | 3 | 1 | 2 | 5 |
| **鹿鸣湖畔** | `workspace/projects/鹿鸣湖畔/` | 4 | 2 | 2 | 5 |
| **麓山宴** | `workspace/projects/麓山宴/` | 0 | 1 | 0 | 0 |
