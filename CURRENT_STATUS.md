# TermMT 当前进展与后续计划

> 更新时间：2026-03-15
> 评估依据：`README.md` 复现流程 + 仓库当前文件结构（静态盘点）
> 说明：以下“完成状态”表示**资源/脚本/结果文件是否存在**，不等价于“本机已成功完整跑通”。

## 1) 复现阶段完成度（对照 README）

| 阶段 | README 要求 | 当前状态 | 证据 | 下一步 |
|---|---|---|---|---|
| 依赖环境 | `pip install -r requirements.txt`，Python 3.7/3.8 双环境 | 进行中（py3.8 已可用） | 已创建 `.mamba/envs/termmt-py38`，关键包 `torch/transformers/openai/awesome-align` 可导入；新增 `requirements.portable.txt` | 补充环境快照（`pip freeze` / conda yaml），再验证主链路脚本运行 |
| 数据准备 | `data/IATE_export.csv`、`data/wikiarticles.xml`、双语语料 | 基本完成 | `data/` 下存在 `IATE_export.csv`、`wikiarticles.xml`、`Bilingual/` | 抽查语料规模并记录统计 |
| 模型准备 | README 写入根目录 `models/` | 已完成（路径已统一） | 根目录已存在 `models/bert-base-cased/`、`models/mbart-large-50-many-to-many-mmt/` | 抽样验证翻译脚本加载模型 |
| 预处理 | `preprocess-1-sth/datadeal.sh` | 部分完成（术语抽取与标注完成） | 已有 `preprocess-1-sth/results/preprocess/iateterms` 与 `iatemark`；并同步到 `data/iatemark`；`data/enwiktionary.jsonl` 已存在 | 重跑字典构建链路并确认 `meaningdict.jsonl` 产出 |
| 变异生成 | `mutant-1-sth/mutant.sh` | 脚本就绪 | 存在 `mutant-1-sth/mutant.sh` | 执行后登记 `results` 产物位置 |
| 翻译与对齐 | `detect-1-sth/initialize.sh/translate.sh/align.sh` | 脚本就绪 | `detect-1-sth/` 下脚本齐全 | 执行并记录中间文件与耗时 |
| 错误检测 | `detect.sh` / `detect_filter.sh` / GPT链路 | 脚本就绪 | `detect-1-sth/` 下检测脚本齐全；`scripts/translate/` 下 LLM 相关脚本齐全 | 按 py3.7/py3.8 分环境跑并保存报告 |
| RQ1 | 问卷与统计 | 已有人工结果 | `rq/rq1/results/our_manual_result/{member1,member2,realistic_result}` | 复算一次并输出汇总表 |
| RQ2 | 问卷与统计 | 已有人工结果 | `rq/rq2/results/our_manual_result/{member1,member2,precision}` | 复算一次并输出汇总表 |
| RQ3 | 阈值影响 | 已有人工结果 | `rq/rq3/results/our_manual_result/{member1_termmt,member2_termmt,statistics-termmt}` | 复算并画阈值曲线 |
| RQ4 | CAT 对比与阈值搜索 | 已有人工结果 + 脚本齐全 | `rq/rq4/results/our_manual_result/{member1,member2,statistics}`；`CAT/.../gentest.sh`、`desp.sh`、`cal_metric.sh` 等存在 | 复算 CAT 指标并核对与论文一致性 |
| Discussion: Overlap | `overlap/get_overlap.py` | 脚本就绪 | `overlap/` 存在 `get_overlap.py` | 生成 overlap 统计文件 |
| Discussion: LLM | `gpt-test/` 链路 | 已有人工结果 + 脚本齐全 | `gpt-test/results/our_manual_result/{member1_gpt,member2_gpt,percision_gpt}` | 复算并核对拼写/路径一致性 |
| 错误案例展示 | `cases/` | 已有资料 | `cases/{mr1,mr2,mr3,guinea pig,part of speech}` | 为每类案例补简短说明 |

## 2) 发现的关键差异/风险

1. （已解决）模型目录已在根目录 `models/` 下就位；需补充一次脚本侧加载验证记录。
2. 仓库根目录未发现 `output/`（README/旧结构中可能提及）。
3. 多处脚本与结果命名存在拼写差异（如 `percision`/`precision`、`precison`），易导致后续自动化脚本引用错误。
4. 当前缺少“可复现运行日志”（命令、时间、输入版本、输出路径）的统一记录文件。
5. `data/enwiktionary.jsonl` 已全量生成（`8503103` 行，约 `2.8G`）；但尚未看到重跑后生成的 `preprocess-1-sth/results/preprocess/meaningdict.jsonl`。

## 3) 接下来执行计划（建议按优先级）

### P0（先做，保证可复现）
- [ ] 统一模型路径：确认脚本读取位置，决定“迁移模型目录”或“更新 README/脚本参数”。
- [ ] 新建运行日志模板（命令、环境、输入数据版本、输出目录、耗时、异常）。
- [ ] 跑通主链路最小闭环：`datadeal -> mutant -> initialize/translate -> align -> detect`，并登记输出路径。

### P1（结果核验）
- [ ] 分别在 `rq1~rq4` 目录复算统计脚本，生成一份总表（便于与论文数字对照）。
- [ ] 跑 `overlap/get_overlap.py` 与 `gpt-test` 流程中的统计脚本，补齐讨论部分证据。

### P2（维护性）
- [ ] 统一 `precision/percision/precison` 命名或至少在 README 增加“别名说明”。
- [ ] 在 README 增加“目录现状说明”（如 `data/models`）避免新成员踩坑。

## 4) 状态维护模板（后续直接追加）

建议每次执行后在本文末尾追加：

```markdown
### [YYYY-MM-DD] 运行记录
- 执行人：
- 环境：Python 版本 / 关键依赖版本
- 执行命令：
- 输入数据：
- 输出路径：
- 结果摘要：
- 问题与修复：
- 下一步：
```

### [2026-03-15] 数据准备阶段复核与整理
- 已确认：`data/IATE_export.csv`、`data/wikiarticles.xml`、`data/meaningdict_filtered.jsonl` 均存在。
- 已确认：双语语料 `data/Bilingual` 五个领域齐全，行数为 `Subtitles 600000`、`Science 540000`、`Laws 440000`、`News 900000`、`Thesis 600000`。
- 已整理：将 `preprocess-1-sth/results/preprocess/iatemark/*` 同步到 `data/iatemark/*`。
- 已复核：`data/iatemark/*/phrasemark.txt` 行数为 `11931/48075/49451/98183/69493`（按 Subtitles/Science/Laws/News/Thesis）。
- （更新）`data/enwiktionary.jsonl` 已补齐；当前阻塞已转为“下游字典/变异链路待重跑并产出结果文件”。

### [2026-03-15] 补齐 Wiktionary 转换链路
- 执行人：Copilot（自动执行）
- 修改文件：
	- `scripts/dictdeal/xml_to_enwiktionary_jsonl.py`（新增）
	- `preprocess-1-sth/datadeal.sh`（缺失 `enwiktionary.jsonl` 时自动从 `wikiarticles.xml` 生成）
	- `README.md`（补充中间文件生成说明）
- 自测命令：
	- `micromamba run -p .mamba/envs/termmt-py38 python scripts/dictdeal/xml_to_enwiktionary_jsonl.py --input_xml data/wikiarticles.xml --output_jsonl data/enwiktionary.sample.jsonl --max_pages 200`
- 自测结果：
	- 解析 200 页，写出 173 条 JSONL；每行结构包含 `title` 与 `text`，与 `dealjson.py` 读取字段一致。
- 下一步：
	- （更新）`data/enwiktionary.jsonl` 已全量生成；下一步为重跑 `preprocess-1-sth/datadeal.sh` 字典构建链路并确认 `meaningdict.jsonl`。

## 5) 今日状态日志

### [2026-03-14] 初次盘点
- 已完成：按 README 建立阶段清单并完成仓库静态核查。
- 已确认：数据文件、主流程脚本、RQ 人工结果目录、CAT 与 GPT 讨论脚本基本齐全。
- 待确认：主链路是否在当前机器可一键跑通；各阶段输出是否与论文一致。

### [2026-03-14] 环境配置进展
- 执行人：Copilot（自动执行）
- 环境：系统仅有 `python3.12`，且缺失 `pip3` / `python3.12-venv`；`sudo` 需要密码，无法直接安装系统包。
- 处理方案：
	- 使用 `get-pip.py --user --break-system-packages` 安装用户态 `pip`。
	- 使用 `virtualenv` 创建 `.venv312`（用于可安装性验证）。
	- 用户态安装 `micromamba`，创建 `.mamba/envs/termmt-py38`（Python 3.8.20 + pip）。
	- 因原 `requirements.txt` 含 `@ file:///...` 本机不存在路径，新增可移植依赖清单 `requirements.portable.txt`。
- 已验证：
	- `micromamba run -p .mamba/envs/termmt-py38 python -c "import torch, transformers, openai, awesome_align"` 通过。
	- 关键版本：`torch 1.13.0+cu117`、`transformers 4.30.2`、`openai 0.28.1`。
- 已归档：
	- 环境导出：`env/termmt-py38.yml`
	- 依赖冻结：`env/termmt-py38-freeze.txt`
- 当前可用命令：
	- 激活：`~/.local/bin/micromamba activate /mnt/e/vv/nuaa/nuaa_project/TermMT/.mamba/envs/termmt-py38`
	- 单次运行：`~/.local/bin/micromamba run -p /mnt/e/vv/nuaa/nuaa_project/TermMT/.mamba/envs/termmt-py38 <command>`
- 风险与备注：
	- 原始 `requirements.txt` 不是纯可移植锁定文件（含本地构建路径），跨机器会失败。
	- 目前先保证 py3.8 核心运行依赖可用；后续需决定是否维护官方 `requirements-portable`。
- 下一步：按 README 开始跑主链路最小闭环并继续写入本文件。

### [2026-03-15] 预处理执行记录（datadeal）
- 执行命令：`cd preprocess-1-sth && micromamba run -p .mamba/envs/termmt-py38 bash datadeal.sh`
- 运行耗时：`ELAPSED=36:16.84`（脚本返回 `EXIT=0`）
- 运行前修复：
	- `preprocess-1-sth/datadeal.sh` 中目录创建改为 `mkdir -p`（避免父目录不存在时报错）。
	- `scripts/dictdeal/dealjson.py` 删除不存在且未使用的 `parse_wikitext` 导入。
- 已产物：
	- `preprocess-1-sth/results/preprocess/iateterms/iate_phrase_term.txt`（181KB）
	- `preprocess-1-sth/results/preprocess/iatemark/*/phrasemark.txt`
	- 行数统计：`Subtitles 11931`、`Science 48075`、`Laws 49451`、`News 98183`、`Thesis 69493`
	- 同步目录：`data/iatemark/`（含各领域标注结果）
- 未完成/阻塞：
	- 字典构建链路失败：`dealjson.py` 报错缺少 `../data/enwiktionary.jsonl`。
	- 因上一步失败，`results/preprocess/meaningdict.jsonl` 未生成，`filterate.py` 随后失败。
- 结论：
	- 预处理中的“术语提取+句子标注”已完成；“从 Wiktionary 构建 meaning dictionary”未完成。
- 下一步：
	- （更新）`data/enwiktionary.jsonl` 已就绪，待重跑 `datadeal.sh` 并确认 `results/preprocess/meaningdict.jsonl` 产出。

### [2026-03-15] enwiktionary 后续现状复核（补记）
- 已确认：`data/enwiktionary.jsonl` 已生成，行数 `8503103`，文件大小约 `2.8G`。
- 已确认：根目录 `models/` 已存在，包含 `bert-base-cased/` 与 `mbart-large-50-many-to-many-mmt/`。
- 已确认：`mutant-1-sth/results/` 已创建五个领域目录（`Subtitles/Science/Laws/News/Thesis` 对应目录结构已在）。
- 当前阻塞：`data/mutant_results/` 仍为空，未发现 `*/generalMutant.jsonl`，因此 `detect-1-sth/initialize.sh` 的输入尚未就绪。
- 文档待回填项：将“缺少 enwiktionary”相关旧结论统一改为“已补齐，待重跑并产出 meaningdict/mutant 输入”。
