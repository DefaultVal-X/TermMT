# TermMT 变异生成执行记录 (2026-03-16)

## 执行摘要

| 项目 | 内容 |
|------|------|
| **执行时间** | 2026-03-16 18:08:00 CST |
| **执行人** | GitHub Copilot |
| **执行命令** | `bash mutant.sh` |
| **工作目录** | `/home/cysds/TermMT/mutant-1-sth` |
| **环境** | termmt-py38 (Python 3.8.20) |
| **状态** | ⏳ **进行中** |

---

## 前置准备完成

### 环境验证
- ✅ conda 虚拟环境激活: `termmt-py38`
- ✅ Python 版本: 3.8.20
- ✅ 关键依赖导入成功

### 数据准备
- ✅ 输入数据: `data/iatemark/` (五领域标注数据)
- ✅ 词义字典: `data/meaningdict_filtered.jsonl` (1.6 MB)
- ✅ POS 模型: `models/pos-english/pytorch_model.bin` (238 MB)

### NLTK 资源下载
- ✅ wordnet (已下载)
- ✅ averaged_perceptron_tagger (已下载)
- ✅ punkt (已下载)

---

## 执行流程

### 脚本: mutant.sh
```bash
cd /home/cysds/TermMT/mutant-1-sth
bash mutant.sh
```

**脚本处理五个领域的顺序**:
1. Subtitles (11,931 句对)
2. Science (48,075 句对)
3. Laws (49,451 句对)
4. News (98,183 句对)
5. Thesis (69,493 句对)

**总计**: 276,133 句对

---

## 当前进度

### [18:08:52] 启动 Subtitles 处理
- 状态: ✅ 进行中
- 预期产物: 
  - `results/result_Subtitles-mutant/iatemutant/Bilingual/phrase/Subtitles/generaMutant.jsonl`
  - `results/result_Subtitles-mutant/iatemutant/Bilingual/phrase/Subtitles/insertMutant.jsonl`
  - `results/result_Subtitles-mutant/iatemutant/Bilingual/phrase/Subtitles/bertInsertMutant.jsonl`

---

## 后续处理

### 待处理域
- Science (48,075 句对) - 预计需要 20+ 分钟
- Laws (49,451 句对) - 预计需要 20+ 分钟
- News (98,183 句对) - 预计需要 30+ 分钟
- Thesis (69,493 句对) - 预计需要 25+ 分钟

### 总预计耗时
**2.5-4 小时**（取决于手硬件和系统负载）

---

## 日志文件位置

- 完整日志: `/home/cysds/TermMT/mutant-1-sth/mutant_full.log`
- 单领域日志: `./results/result_[DOMAIN]-mutant/iatemutant/Bilingual/phrase/mutant.log`

---

## 监控命令

### 查看实时进度
```bash
tail -f /home/cysds/TermMT/mutant-1-sth/mutant_full.log
```

### 检查产物
```bash
find /home/cysds/TermMT/data/mutant_results -name "*.jsonl" | wc -l
```

### 检查进程
```bash
ps aux | grep mutant | grep -v grep
```

---

## 预期最后步骤

### Step 1: 确认产出完整
所有 5 个领域各产出 3 个 jsonl 文件：
```
data/mutant_results/Subtitles/generalMutant.jsonl
data/mutant_results/Subtitles/insertMutant.jsonl
data/mutant_results/Subtitles/bertInsertMutant.jsonl
... (Science, Laws, News, Thesis 各一套)
```

### Step 2: 验证数据
```bash
find data/mutant_results -name "generalMutant.jsonl" -exec wc -l {} \;
```

### Step 3: 进入翻译与对齐阶段
```bash
cd detect-1-sth
bash initialize.sh && bash translate.sh && bash align.sh
```

---

## 关键注意事项

⚠️ **重要**：
1. 脚本在后台运行，使用 `tail -f mutant_full.log` 监控
2. 预计完成时间: ~21:30-22:30 (取决于系统性能)
3. 最后一个领域完成后，结果会自动复制到 `data/mutant_results/`
4. 不要中断进程，否则当前领域的处理会丢失

---

## 实时监控

**启动时间**: 2026-03-16 18:08:52 CST
**监控脚本**: `/home/cysds/TermMT/check_mutant_progress.sh`

运行 `bash check_mutant_progress.sh` 查看当前状态
