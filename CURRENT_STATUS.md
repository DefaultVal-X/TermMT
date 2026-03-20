# TermMT 当前进展与后续计划

> 更新时间：2026-03-20
> 评估依据：`README.md` 复现流程 + 仓库当前文件结构（静态盘点）
> 说明：以下状态已结合本机实际产物核验（截至 2026-03-20）。

## 1) 复现阶段完成度（对照 README）

| 阶段 | README 要求 | 当前状态 | 证据 | 下一步 |
|---|---|---|---|---|
| 依赖环境 | `pip install -r requirements.txt`，Python 3.7/3.8 双环境 | ✅ **已完成** (py3.8) | `conda activate termmt-py38` (Python 3.8.20)；torch/transformers/openai/awesome-align/sentence-transformers/flair 等全部导入成功；requirements.portable.txt 可用 | 验证主链路脚本运行 |
| 数据准备 | `data/IATE_export.csv`、`data/wikiarticles.xml`、双语语料 | 基本完成 | `data/` 下存在 `IATE_export.csv`、`wikiarticles.xml`、`Bilingual/` | 抽查语料规模并记录统计 |
| 模型准备 | README 写入根目录 `models/` | 已完成（路径已统一） | 根目录已存在 `models/bert-base-cased/`、`models/mbart-large-50-many-to-many-mmt/` | 抽样验证翻译脚本加载模型 |
| 预处理 | `preprocess-1-sth/datadeal.sh` | ✅ **已完成** | 术语抽取、数据标注、词义字典构建均完成；`data/iatemark/*/phrasemark.txt` + `data/meaningdict_filtered.jsonl` 完整 | 进阶流程已就绪 |
| 变异生成 | `mutant-1-sth/mutant.sh` | ✅ **已完成** | `data/mutant_results/{Subtitles,Science,Laws,News,Thesis}/generalMutant.jsonl` 各一，insertMutant.jsonl/bertInsertMutant.jsonl 等产物齐全 | 执行翻译与对齐阶段 |
| 翻译与对齐 | `detect-1-sth/initialize.sh/translate.sh/align.sh` | 🟡 **部分完成** | `detect-1-sth/results/*-detect/` 已存在 `metamorphic_items.json`、`phrase_*mutants.txt`、`translate.log`（五领域）；但尚未看到明确的 alignment 结果文件 | 运行 `align.sh` 并补齐对齐产物核验 |
| 错误检测 | `detect.sh` / `detect_filter.sh` / GPT链路 | ⏳ **待执行/待核验** | 当前可见主要为翻译阶段产物，未看到明确 bug report / detect_filter 收尾文件 | 按 py3.7/py3.8 分环境跑检测并沉淀报告 |
| RQ1 | 问卷与统计 | 已有人工结果 | `rq/rq1/results/our_manual_result/{member1,member2,realistic_result}` | 复算一次并输出汇总表 |
| RQ2 | 问卷与统计 | 已有人工结果 | `rq/rq2/results/our_manual_result/{member1,member2,precision}` | 复算一次并输出汇总表 |
| RQ3 | 阈值影响 | 已有人工结果 | `rq/rq3/results/our_manual_result/{member1_termmt,member2_termmt,statistics-termmt}` | 复算并画阈值曲线 |
| RQ4 | CAT 对比与阈值搜索 | 已有人工结果 + 脚本齐全 | `rq/rq4/results/our_manual_result/{member1,member2,statistics}`；`CAT/.../gentest.sh`、`desp.sh`、`cal_metric.sh` 等存在 | 复算 CAT 指标并核对与论文一致性 |
| Discussion: Overlap | `overlap/get_overlap.py` | 脚本就绪 | `overlap/` 存在 `get_overlap.py` | 生成 overlap 统计文件 |
| Discussion: LLM | `gpt-test/` 链路 | 已有人工结果 + 脚本齐全 | `gpt-test/results/our_manual_result/{member1_gpt,member2_gpt,percision_gpt}` | 复算并核对拼写/路径一致性 |
| 错误案例展示 | `cases/` | 已有资料 | `cases/{mr1,mr2,mr3,guinea pig,part of speech}` | 为每类案例补简短说明 |

## 2) 发现的关键差异/风险

1. 对齐（align）与错误检测（detect/detect_filter/GPT judge）最终产物仍需统一核验并补收尾记录。
2. 多处脚本与结果命名存在拼写差异（如 `percision`/`precision`、`precison`），易导致自动化脚本引用错误。
3. 运行日志分散在 `CURRENT_STATUS.md`、`MUTANT_EXECUTION_LOG.md` 与各目录 `*.log`；建议维护一份统一“主链路执行总表”。
4. `preprocess-1-sth/results/preprocess/meaningdict.jsonl` 当前未见，后续若重跑预处理需补产物校验。

## 3) 接下来执行计划（建议按优先级）

### P0（先做，保证可复现）
- [ ] 跑通并核验后半段主链路：`align -> detect`（前半段 `datadeal -> mutant -> initialize/translate` 已有产物）。
- [ ] 为 `detect-1-sth` 增加统一结果索引（每领域关键输出文件、行数、最后更新时间）。
- [ ] 汇总一份“单机复现总表”（命令、环境、输入版本、输出目录、耗时、异常）。

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

## 5) 今日状态日志

### [2026-03-16] 虚拟环境完整配置与变异生成完成
- 执行人：GitHub Copilot
- 环境配置：
  - 改用系统 conda 创建 `termmt-py38` (Python 3.8.20)
  - 激活命令：`conda activate termmt-py38`
  - 位置：`/home/cysds/.conda/envs/termmt-py38`
  
- 依赖完整性：
  - torch==1.13.0, transformers==4.30.2, openai==0.28.1
  - sentence-transformers>=2.3.0（解决与 huggingface-hub 的版本冲突）
  - flair, awesome-align (editable)
  - 所有关键包导入成功验证

- 前置资源验证：
  - ✅ 词义字典：`data/meaningdict_filtered.jsonl` (1.6 MB)
  - ✅ 标注数据：`data/iatemark/` 五领域完整
  - ✅ 关键模型：`models/pos-english/pytorch_model.bin` (238 MB) 已就位
  - ✅ NLTK 资源：wordnet, averaged_perceptron_tagger, punkt 已下载

- 变异生成执行：
  - 命令：`cd mutant-1-sth && bash mutant.sh`
  - 耗时：~30-40 分钟
  - 处理流程：Subtitles → Science → Laws → News → Thesis
  
- 产物确认：**✅ COMPLETED**
  - `data/mutant_results/Subtitles/generalMutant.jsonl` ✅
  - `data/mutant_results/Science/generalMutant.jsonl` ✅
  - `data/mutant_results/Laws/generalMutant.jsonl` ✅
  - `data/mutant_results/News/generalMutant.jsonl` ✅
  - `data/mutant_results/Thesis/generalMutant.jsonl` ✅
  - 各领域的 insertMutant.jsonl 和 bertInsertMutant.jsonl 也已产出

- 下一步：
  - 执行翻译与对齐阶段 (`detect-1-sth/initialize.sh → translate.sh → align.sh`)
  - 预计耗时：2-3 小时

### [2026-03-18] News 领域可续跑能力更新（抗 Killed / OOM）
- 背景：`News` 在 `--num_workers 2/4` 下多次被系统 `Killed`（exit 137），属于内存压力导致的进程终止。
- 代码更新：`scripts/mutant/mutant.py`
	- 新增增量写入：每条结果实时追加到 jsonl，避免“全量结束后才写盘”的丢进度问题。
	- 新增断点续跑：启动时自动读取三类输出行数并对齐到最小行数，随后从对应 pair 继续处理。
	- 保留并行限流：限制 in-flight futures，降低峰值内存。
- 推荐续跑命令（可重复执行，自动续跑）：
	- `cd mutant-1-sth`
	- `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 conda run --no-capture-output -n termmt-gpu311 python ../scripts/mutant/mutant.py --meaningdict ../data/meaningdict_filtered.jsonl --input_path ../data/iatemark --output_path results/result_News-mutant/iatemutant/Bilingual/phrase --term_level phrase --tgtarea News --num_workers 1`
- 结果同步命令（完成后执行）：
	- `cd mutant-1-sth`
	- `rm -rf ../data/mutant_results/News`
	- `cp -r results/result_News-mutant/iatemutant/Bilingual/phrase/News ../data/mutant_results/`
- 注意事项：
	- 运行中三类 jsonl 行数可能临时不一致（若恰好在三次写盘之间被中断）；下次启动会自动对齐修复后继续。
	- 当前机器建议 `News` 优先使用 `--num_workers 1`，稳定性优先于速度。

### [2026-03-20] 变异结果全量复核（五领域）
- 执行人：GitHub Copilot
- 复核范围：`data/mutant_results` 产物行数 + `mutant-1-sth/results/result_*-mutant/.../mutant.log` 收尾统计。
- 复核结论：五个领域均已完成，且 `generalMutant.jsonl` / `insertMutant.jsonl` / `bertInsertMutant.jsonl` 行数三者一致。
- 行数结果：
	- Subtitles: `5862 / 5862 / 5862`
	- Science: `21666 / 21666 / 21666`
	- Laws: `16925 / 16925 / 16925`
	- News: `45143 / 45143 / 45143`
	- Thesis: `32513 / 32513 / 32513`
- 日志核验：
	- Subtitles/Science/Laws/News/Thesis 均在各自 `mutant.log` 出现 `Drop stats for <Area>` 收尾段。
	- Thesis 与 News 的续跑日志包含 `output line counts are inconsistent, aligning to min rows=...` 与 `resuming ...`，说明断点续跑逻辑已实际生效。
- 备注：当前 `data/mutant_results` 已可作为 `detect-1-sth` 后续流程输入。

### [2026-03-20] 复现阶段完成度同步（对照 README）
- 执行人：GitHub Copilot
- 同步范围：`CURRENT_STATUS.md` 第 1 节“复现阶段完成度（对照 README）”。
- 同步结论：
	- `mutant` 五领域产物完整，行数一致（已在上一条记录确认）。
	- `detect-1-sth` 已存在五领域翻译阶段中间产物（`metamorphic_items.json`、`phrase_*mutants.txt`、`translate.log`）。
	- 对齐（align）与错误检测（detect/detect_filter/GPT judge）的最终结果文件仍需补跑或补核验。
