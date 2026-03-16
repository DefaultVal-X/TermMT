# TermMT 虚拟环境配置完成总结 (2026-03-16)

> 备份生成时间：2026-03-16  
> 操作者：GitHub Copilot  
> 状态：✅ 虚拟环境与数据准备完成，已为变异生成阶段就绪

---

## 📋 虚拟环境配置进展

### 环境基础信息

| 项目 | 内容 | 状态 |
|------|------|------|
| **环境名称** | `termmt-py38` | ✅ |
| **Python 版本** | 3.8.20 | ✅ |
| **管理工具** | conda 24.9.2 | ✅ |
| **激活命令** | `conda activate termmt-py38` | ✅ |
| **位置** | `/home/cysds/.conda/envs/termmt-py38` | ✅ |


```

### 依赖验证结果

```bash
$ conda activate termmt-py38
$ python -c "import torch, transformers, openai, awesome_align, sentence_transformers, flair; print('✓ All dependencies imported successfully')"
✓ All dependencies imported successfully
```

---

## 📊 已解决的阻塞点

### 1. 虚拟环境创建 ✅
- **问题**: 原计划使用 micromamba，但系统中对应工具不完全可用
- **解决方案**: 使用系统 conda (24.9.2) 创建环境
- **结果**: 成功创建 `termmt-py38` (Python 3.8.20)

### 2. 依赖版本冲突 ✅
- **问题**: `sentence-transformers` 与 `huggingface-hub` 版本不兼容
- **错误信息**: `ImportError: cannot import name 'cached_download' from 'huggingface_hub'`
- **解决方案**: 升级 `sentence-transformers>=2.3.0`
- **结果**: 导入成功

### 3. 关键模型文件状态 ✅
- **模型**: `models/pos-english/pytorch_model.bin`
- **大小**: 238 MB
- **状态**: 已就位（此前为主要阻塞点）
- **作用**: 支持 POS 标注，变异生成脚本依赖

---

## 🗂️ 数据完整性验证

### 输入数据

#### 词典数据
- ✅ `data/enwiktionary.jsonl`
  - 大小: 2.8 GB
  - 行数: 8,503,103
  - 用途: Wiktionary 词典数据源

- ✅ `data/meaningdict_filtered.jsonl`
  - 大小: 1.6 MB
  - 格式: JSONL (JSON Lines)
  - 内容: 已过滤的词义表，包含：
    - `term`: 词条
    - `meanitems`: 词義列表（含词性、释义）
    - `alternative_forms`: 替代形式
    - `synonyms`: 同义词
    - `translations`: 翻译（中文）

#### 标注数据
- ✅ `data/iatemark/` - 五领域完整标注
  - `Subtitles/phrasemark.txt` (759 KB, 11,931 行)
  - `Science/phrasemark.txt` (5.5 MB, 48,075 行)
  - `Laws/phrasemark.txt` (11 MB, 49,451 行)
  - `News/phrasemark.txt` (18 MB, 98,183 行)
  - `Thesis/phrasemark.txt` (12 MB, 69,493 行)
  - **格式**: 英文原句 + 标记术语 + 中文翻译（每两行一组）

### 模型文件

| 模型 | 位置 | 状态 | 用途 |
|------|------|------|------|
| BERT Base | `models/bert-base-cased/` | ✅ | 嵌入与 NLP 任务 |
| BGE | `models/bge-base-en-v1.5/` | ✅ | 句子相似度计算 |
| mBART | `models/mbart-large-50-many-to-many-mmt/` | ✅ | 神经机器翻译 |
| POS Tagger | `models/pos-english/pytorch_model.bin` | ✅ | 词性标注 (238 MB) |

---

## ✅ 预处理阶段完成状态

| 子任务 | 状态 | 产物位置 |
|--------|------|---------|
| 术语抽取 | ✅ 完成 | `data/iatemark/*/phrasemark.txt` |
| 数据标注 | ✅ 完成 | `data/iatemark/*/phrasemark.txt` |
| 词义字典构建 | ✅ 完成 | `data/meaningdict_filtered.jsonl` |
| 词义字典过滤 | ✅ 完成 | `data/meaningdict_filtered.jsonl` |

---

## 🚀 后续执行步骤

### 第1步: 变异生成阶段 (P0 优先级)

**预计耗时**: 2-4 小时（取决于系统硬件）

#### 完整执行流程
```bash
# 激活环境
conda activate termmt-py38

# 进入目录
cd /home/cysds/TermMT/mutant-1-sth

# 执行脚本（处理所有5个领域）
bash mutant.sh
```

#### 单领域测试流程（推荐先运行）
```bash
conda activate termmt-py38
cd /home/cysds/TermMT/mutant-1-sth
python ../scripts/mutant/mutant.py \
  --meaningdict ../data/meaningdict_filtered.jsonl \
  --input_path ../data/iatemark \
  --output_path ./results \
  --term_level phrase \
  --tgtarea Subtitles
```

#### 验证产物
```bash
# 应输出 5（表示五个领域均产出结果）
find data/mutant_results -name "generalMutant.jsonl" | wc -l
```

### 第2步: 翻译与词对齐阶段 (P1 优先级)

```bash
conda activate termmt-py38
cd /home/cysds/TermMT/detect-1-sth

bash initialize.sh  # 初始化
bash translate.sh   # 翻译
bash align.sh       # 对齐
```

### 第3步: 错误检测阶段 (P2 优先级)

```bash
conda activate termmt-py38
cd /home/cysds/TermMT/detect-1-sth

bash detect.sh         # 错误检测
bash detect_filter.sh  # 过滤检测
```

---

## 🔧 快速命令参考

### 环境管理
```bash
# 激活环境
conda activate termmt-py38

# 验证 Python 版本
python --version  # 应输出 3.8.20

# 验证依赖导入
python -c "import torch, transformers"

# 查看环境详情
conda info --envs
```

### 运行与调试
```bash
# 进入变异生成目录
cd mutant-1-sth

# 查看 mutant.sh 内容
cat mutant.sh

# 运行单个领域
python ../scripts/mutant/mutant.py \
  --meaningdict ../data/meaningdict_filtered.jsonl \
  --input_path ../data/iatemark \
  --output_path ./test_run \
  --term_level phrase \
  --tgtarea Subtitles

# 查看运行日志
tail -f results/result_Subtitles-mutant/mutant.log

# 检查产物
ls -lh data/mutant_results/
find data/mutant_results -name "*.jsonl" | head -10
```

### 数据验证
```bash
# 查看词典格式
head -1 data/meaningdict_filtered.jsonl | python -m json.tool

# 查看标注数据
head -2 data/iatemark/Subtitles/phrasemark.txt

# 统计数据量
wc -l data/iatemark/*/phrasemark.txt
```

---

## 📈 进度规划表

| 阶段 | 当前状态 | 完成标志 | 预计耗时 |
|------|---------|---------|---------|
| **依赖环境** | ✅ 已完成 | `conda activate termmt-py38` 可用 | - |
| **数据准备** | ✅ 已完成 | 数据文件齐全 | - |
| **预处理** | ✅ 已完成 | 词义字典产出 | - |
| **变异生成** | ⏳ 准备就绪 | 5 个 generalMutant.jsonl 产出 | 2-4h |
| **翻译对齐** | ⏳ 待执行 | 翻译与对齐结果产出 | 2-3h |
| **错误检测** | ⏳ 待执行 | 检测报告产出 | 1-2h |

---

## ⚠️ 重要注意事项

### 1. 环境激活
- ⚠️ **每次打开新终端都需要重新激活环境**
  ```bash
  conda activate termmt-py38
  ```

### 2. 工作目录
- 某些脚本需在特定目录运行：
  - `mutant.sh` 需在 `mutant-1-sth/` 目录运行
  - `initialize.sh` 等需在 `detect-1-sth/` 目录运行

### 3. 模型路径
- 所有脚本使用相对路径 `../models/`
- 确保不移动 `models/` 目录和脚本的相对位置

### 4. 磁盘空间
- 检查可用磁盘空间（变异生成可能产生大量中间文件）
  ```bash
  df -h /home
  ```

---

## 📝 执行记录模板

完成各阶段后，请记录进度：

```markdown
### [YYYY-MM-DD] 变异生成执行记录
- 执行人: [姓名]
- 环境: termmt-py38 (Python 3.8.20)
- 执行命令: bash mutant.sh
- 开始时间: [YYYY-MM-DD HH:MM:SS]
- 结束时间: [YYYY-MM-DD HH:MM:SS]
- 总耗时: [XX 小时 XX 分钟]
- 产物验证: find data/mutant_results -name "generalMutant.jsonl" | wc -l
- 结果数字: [应为 5]
- 遇到的问题: [如有]
- 修复方法: [如有]
- 下一步: 执行翻译与对齐阶段
```

---

## 🎯 关键要点总结

✅ **已完成**:
- Python 3.8 虚拟环境建立
- 所有 Python 依赖安装完成
- 五大领域标注数据完整
- 词义字典构建完成
- 所有必需模型文件已就位

⏳ **待完成**:
1. 变异生成 (Mutation Generation)
2. 翻译与对齐 (Translation & Alignment)
3. 错误检测 (Error Detection)
4. RQ 验证与统计

🚀 **立即可执行**:
```bash
conda activate termmt-py38
cd mutant-1-sth
bash mutant.sh  # 或先运行单领域测试
```

---

**备注**: 本配置已在 Linux 系统 (Python 3.8.20 via conda) 下验证成功。
