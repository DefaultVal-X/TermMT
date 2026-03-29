# TermMT 当前进展与后续计划

> 更新时间：2026-03-29
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
| 翻译与对齐 | `detect-1-sth/initialize.sh/translate.sh/align.sh` | 🟡 **已完成（除 Thesis bing）** | 四领域（Subtitles/Science/Laws/News）已生成 `metamorphic_items_aligned_{bing,google,mbart}.json(.jsonl)`；`Thesis` 的 `bing` 仍缺失 | 补齐 Thesis 的 bing 翻译/对齐，或明确“跳过 Thesis bing”的复现口径 |
| 错误检测 | `detect.sh` / `detect_filter.sh` / GPT链路 | 🟡 **已完成（四领域三模型）** | `detect-1-sth/results/{Subtitles,Science,Laws,News}-detect/error_{bing,google,mbart}` 及 `metamorphic_items_final_*.json` 已生成 | 执行 `detect_filter.sh` 与 GPT 链路；决定 Thesis 是否补齐 |
| RQ1 | 问卷与统计 | 已有人工结果 | `rq/rq1/results/our_manual_result/{member1,member2,realistic_result}` | 复算一次并输出汇总表 |
| RQ2 | 问卷与统计 | 已有人工结果 | `rq/rq2/results/our_manual_result/{member1,member2,precision}` | 复算一次并输出汇总表 |
| RQ3 | 阈值影响 | 已有人工结果 | `rq/rq3/results/our_manual_result/{member1_termmt,member2_termmt,statistics-termmt}` | 复算并画阈值曲线 |
| RQ4 | CAT 对比与阈值搜索 | 已有人工结果 + 脚本齐全 | `rq/rq4/results/our_manual_result/{member1,member2,statistics}`；`CAT/.../gentest.sh`、`desp.sh`、`cal_metric.sh` 等存在 | 复算 CAT 指标并核对与论文一致性 |
| Discussion: Overlap | `overlap/get_overlap.py` | 脚本就绪 | `overlap/` 存在 `get_overlap.py` | 生成 overlap 统计文件 |
| Discussion: LLM | `gpt-test/` 链路 | 已有人工结果 + 脚本齐全 | `gpt-test/results/our_manual_result/{member1_gpt,member2_gpt,percision_gpt}` | 复算并核对拼写/路径一致性 |
| 错误案例展示 | `cases/` | 已有资料 | `cases/{mr1,mr2,mr3,guinea pig,part of speech}` | 为每类案例补简短说明 |

## 2) 发现的关键差异/风险

1. 对齐与 detect 已覆盖四领域三模型，但 `Thesis` 的 bing 仍缺（翻译/对齐/检测链路未闭环），且 `detect_filter` / GPT judge 尚未统一收尾。
2. 翻译阶段当前阻断点为 Bing 鉴权失败（`401 Unauthorized` / `401001`）；结合近期现象，疑似订阅额度耗尽或密钥与资源不匹配，导致 `Thesis` 的 Bing 翻译与对齐未完成。
3. 多处脚本与结果命名存在拼写差异（如 `percision`/`precision`、`precison`），易导致自动化脚本引用错误。
4. 运行日志分散在 `CURRENT_STATUS.md`、`MUTANT_EXECUTION_LOG.md` 与各目录 `*.log`；建议维护一份统一“主链路执行总表”。
5. `preprocess-1-sth/results/preprocess/meaningdict.jsonl` 当前未见，后续若重跑预处理需补产物校验。

## 3) 接下来执行计划（建议按优先级）

### P0（先做，保证可复现）
- [ ] 跑通并核验后半段主链路：`align -> detect -> detect_filter/GPT`（当前仅缺 `bing/Thesis`）。
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

### [2026-03-22] 翻译 API 可用性复核（Bing + Google）
- 执行人：GitHub Copilot
- 复核方式：加载 `.env` 后，直接调用 `scripts/translate/bing_translate.py` 与 `scripts/translate/google_trans.py` 发起真实翻译请求。
- 复核结果：
  - Bing API: ✅ 可用（示例返回 `你好，世界`）
  - Google API: ✅ 可用（示例返回 `你好世界`）
- 代码状态：`scripts/translate/google_trans.py` 已改为 API Key + HTTP 请求模式，不再依赖 `google.cloud.translate.Client()` 凭据链。
- 当前建议：
  - 翻译阶段可继续使用 `mbart + bing` 或 `mbart + bing + google`。
  - 对齐阶段仍需先补齐 awesome-align 模型目录（`awesome-align/models/model_without_co`）再全量执行 `align.sh`。

### [2026-03-22] 翻译阶段状态更正（Bing 401，疑似额度/订阅问题）
- 执行人：GitHub Copilot
- 触发背景：按 `README.md` 与 `CURRENT_STATUS.md` 路径重跑 `detect-1-sth` 翻译后，News/Thesis 等领域在 Bing 路线失败。
- 实际现象：
  - 初始错误表现为 `KeyError: 0`（已通过增强 `scripts/translate/bing_translate.py` 响应解析修复）。
  - 修复后错误收敛为明确的 `HTTPError: 401 Unauthorized`，错误码 `401001`。
  - 结合当前账户状态，判断为“Bing Translator 额度耗尽或订阅/密钥不匹配”导致的鉴权失败。
- 当前结论：
  - Bing API: ❌ 当前不可用（被 401 阻塞）。
  - Google API: ✅ 可用（API Key 模式实测成功）。
- 后续动作：
  - 更新 `.env` 中 `BING_TRANSLATOR_KEY`（必要时补 `BING_TRANSLATOR_REGION`）后优先重测 News。
  - Bing 恢复前，可先用 `mbart + google` 路线推进翻译与后续对齐。
#### 下次直接续跑命令（仅跑未完成项）

```bash
cd /home/cysds/TermMT/detect-1-sth
set -a && source ../.env && set +a

for area in News Thesis; do
  for trans_file in originSentences.txt phrase_infoinsertmutants.txt phrase_bertinsertmutants.txt; do
    echo "[bing-resume] area=$area file=$trans_file"
    conda run --no-capture-output -n termmt-py38 \
      python ../scripts/translate/translate.py \
      --area "$area" --time detect --model bing --trans_file "$trans_file"
  done
done
```

- 说明：当前 `translate.py` 对 bing 任务是“按任务重跑”语义，不是逐行断点续传；上面命令已经把范围缩小到未完成组合，能最快恢复到可继续状态。


- 目录现状要点：
  - `google` 子目录目前仅在 `Subtitles`、`Science` 存在。
  - `mbart` 在多个领域仅有 `*_mbart.json`，缺少对应 `*_translations.txt`，说明任务可能在“导出 txt/csv 前”被中断。

#### 推荐续跑顺序（从最短路径恢复）
1. 先补齐 Google：`Science/phrase_bertinsertmutants` + `Laws/News/Thesis` 全部三文件。
2. 再补齐 mBART：优先跑 `Science/Laws/Thesis` 三领域三文件，其次补 `News` 的两项缺口。
3. Bing 在密钥恢复后只跑 `News + Thesis` 六项（上一节已有命令）。

#### Google 续跑命令（建议）

```bash
cd /home/cysds/TermMT/detect-1-sth
set -a && source ../.env && set +a

for area in Science Laws News Thesis; do
  for trans_file in originSentences.txt phrase_infoinsertmutants.txt phrase_bertinsertmutants.txt; do
    # Science 的前两项已完成，重复执行会复用已有结果并补齐缺失项
    echo "[google-resume] area=$area file=$trans_file"
    /home/cysds/.conda/envs/termmt-py38/bin/python ../scripts/translate/translate.py \
      --area "$area" --time detect --model google --trans_file "$trans_file"
  done
done
```

#### mBART 续跑命令（建议）

```bash
cd /home/cysds/TermMT/detect-1-sth
set -a && source ../.env && set +a

for area in Science Laws News Thesis; do
  for trans_file in originSentences.txt phrase_infoinsertmutants.txt phrase_bertinsertmutants.txt; do
    echo "[mbart-resume] area=$area file=$trans_file"
    /home/cysds/.conda/envs/termmt-py38/bin/python ../scripts/translate/translate.py \
      --area "$area" --time detect --model mbart --trans_file "$trans_file"
  done
done
```


### [2026-03-27] 三模型翻译进度同步（最新）
- 执行人：GitHub Copilot
- 统计口径：逐项对比 `detect-1-sth/results/<Area>-detect/<file>.txt` 输入行数与 `translation/<model>/<file>_translations.txt` 输出行数。
- 汇总结论：
  - `bing`: `14/15` 完成，剩余 `32512` 行。
  - `google`: `15/15` 完成，剩余 `0` 行。
  - `mbart`: `15/15` 完成，剩余 `0` 行。
- 当前唯一未完成项（Bing）：
  - `Area=Thesis`
  - `File=phrase_infoinsertmutants.txt`
  - `input=32513`, `output=1`, `remaining=32512`
- 续跑命令（仅剩余 1 项）：

```bash
cd /home/cysds/TermMT/detect-1-sth
set -a && source ../.env && set +a

/home/cysds/.conda/envs/termmt-py38/bin/python ../scripts/translate/translate.py \
  --area Thesis --time detect --model bing --trans_file phrase_infoinsertmutants.txt
```

- 下一步：等待该单项跑完后，再次对账确认 `bing` 达到 `15/15`。

### [2026-03-27] 对齐与模型准备阶段推进
- 执行人：GitHub Copilot
- 完成动作：
  - ✅ BGE 向量模型下载完成：`models/bge-base-zh-v1.5/` （~500 MB）
  - ✅ awesome-align 对齐模型下载完成：`awesome-align/models/model_without_co/`（已下载 ZIP 并解压）
  
- 对齐阶段诊断：
  - 执行命令：`cd detect-1-sth && bash align.sh`
  - 执行结果：**Exit Code 1**（多次重试均失败）
  - 已采取措施：
    - 验证 jieba 库已正常安装（ImportCheck passed）
    - 验证模型文件目录已就位（awesome-align/models/model_without_co/）
    - 移除 `--no-capture-output`，准备捕获完整错误日志
  - 当前阻塞：align.sh 内部脚本执行失败原因未明，需查看完整错误堆栈
  
- 问题排查与修复：
  - **根本原因**：
    1. align.sh 直接执行 python，未激活 conda 环境 → **已修复** ✅
    2. awesome-align 使用 GPU (CUDA)，PyTorch 版本不兼容 RTX 5060 Ti → **已修复** ✅
    3. trans_align.py 的子进程调用 run_align.py 时也没有通过 conda 环境 → **已修复** ✅
  
  - **修复方案**与实施：
    1. 修改 align.sh：`python` → `conda run -n termmt-py38 python` ✅
    2. 修改 trans_align.py：get_align_file() 中添加 `--no_cuda` 参数 ✅
    3. 修改 trans_align.py：子进程调用改为 `conda run -n termmt-py38 python` + `--no_cuda` ✅
  
  - **执行状态**：
    - 第一次修复尝试：CUDA 错误 ❌
    - 第二次修复尝试（当前）：使用正确的 conda 环境 + CPU 对齐 🔄（后台运行中）
    - Terminal ID：7c978925-ba3b-41a6-9aa6-6d102626b6af
    - **预计耗时**：1～3 小时（15 个任务，CPU 对齐较慢）
  
- 监控进度指标：
  - 检查 各领域 `align_*/origin_align.txt` 文件是否非空
  - 确保每个领域的三个模型都生成了对齐结果
  
- 下一步（优先级）：
  1. 待对齐完成后，验证五个领域产物完整性
  2. 启动检测阶段（detect.sh / detect_filter.sh）

### [2026-03-28] 对齐产物落盘核验（最新）
- 执行人：Codex
- 核验方式：检查 `detect-1-sth/results/*-detect/align_*` 目录中 `origin_align.txt` 是否存在且非空。
- 核验结论（google）：五领域全部完成（Subtitles/Science/Laws/News/Thesis）。
- 核验结论（mbart）：五领域全部完成（Subtitles/Science/Laws/News/Thesis）。
- 核验结论（bing）：除 `Thesis` 外其余四领域已完成，`Thesis/align_bing` 仍缺失。
- 关键文件示例（均在 2026-03-27~2026-03-28 生成）：`detect-1-sth/results/News-detect/align_bing/origin_align.txt`；`detect-1-sth/results/Thesis-detect/align_google/origin_align.txt`；`detect-1-sth/results/Thesis-detect/align_mbart/origin_align.txt`
- 下一步：补齐 Bing 的 `Thesis/phrase_infoinsertmutants` 翻译后执行 `align.sh` 仅补 `Thesis/align_bing`；对齐全量完成后立即进入 `detect.sh` / `detect_filter.sh`。

### [2026-03-29] detect 阶段完成（四领域三模型）
- 执行人：Codex
- 覆盖范围：`Subtitles/Science/Laws/News` × `bing/google/mbart`
- 产物确认：
  - `detect-1-sth/results/<Area>-detect/error_{bing,google,mbart}/` 已生成
  - `metamorphic_items_final_{bing,google,mbart}.json` 已生成
- 当前缺口：`Thesis` 的 `bing` 仍未完成（翻译缺失导致 align/detect 不完整）
- 下一步：执行 `detect_filter.sh` + GPT judge；决定 Thesis 是否补齐或明确跳过口径
