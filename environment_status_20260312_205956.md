# TermMT 环境维护记录

- 记录时间：2026-03-12 20:59:56
- 记录目录：`/home/williamxu/nuaa_project/TermMT`
- 记录目的：维护当前可复现环境与安装状态

## 1) 环境现状结论

当前在 WSL/Linux 下，**可用主环境已就绪**，可用于 README 中 Python 3.7 流程（非 GPT 分支）。

已确认：
- 原 Windows Conda 环境（如 `E:\anaconda3\envs\termmt`）在 WSL 中直接运行会出现 DLL 兼容问题，不作为当前执行环境。
- 已改为 Linux 侧新建环境并完成依赖安装。

## 2) 当前可用虚拟环境

- 环境管理器：`micromamba`
- `micromamba` 路径：`/home/williamxu/.local/bin/micromamba`
- 根目录：`/home/williamxu/.micromamba`
- 环境路径：`/home/williamxu/.micromamba/envs/termmt-linux`
- Python 版本：`3.7.12`

说明：README 标注测试版本为 `Python 3.7.16`，当前 Linux 侧创建到 `3.7.12`，已通过关键依赖导入验证，可正常使用。

## 3) 依赖安装状态

- 基于仓库 `requirements.txt` 完成安装。
- 安装时为适配 Linux，使用了临时处理后的依赖文件：`/tmp/termmt_requirements_linux.txt`。
- 该临时文件处理策略：
  - 去除 `@ file:///...` 这类指向本地 conda 构建路径的条目写法；
  - 保留对应包的固定版本；
  - 跳过 `mkl-fft` / `mkl-random` / `mkl-service`（Linux + pip 下非必须，且常见兼容问题来源）。

安装结果：成功。

## 4) 关键包验证结果

已在 `termmt-linux` 环境内成功导入并打印版本：

- `torch 1.13.0+cu117`
- `transformers 4.30.2`
- `flair 0.12.2`
- `sentence_transformers`
- `pandas`
- `nltk`
- `googletrans`

Python 版本校验输出：`3.7.12`。

## 5) 后续使用方式（建议）

执行命令时，建议统一使用以下前缀：

```bash
export MAMBA_ROOT_PREFIX=/home/williamxu/.micromamba
/home/williamxu/.local/bin/micromamba run -p /home/williamxu/.micromamba/envs/termmt-linux <command>
```

示例：

```bash
export MAMBA_ROOT_PREFIX=/home/williamxu/.micromamba
/home/williamxu/.local/bin/micromamba run -p /home/williamxu/.micromamba/envs/termmt-linux python --version
```

## 6) 与 README 的对应关系

- README 主流程（`datadeal.sh`、`mutant.sh`、`detect.sh` 等 Python 3.7 方向）可基于当前环境继续推进。
- README 中 GPT 相关脚本说明需要 Python 3.8（并提到 `openai==0.28.1`），当前尚未单独创建 3.8 环境。

## 7) 待办建议

- [ ] 如需运行 GPT 分支，新增一个 `Python 3.8` 环境并单独安装相关依赖。
- [ ] 下载并放置 README 要求的数据集（`data/`）与模型（`models/`）。
- [ ] 完成后按 README 顺序执行预处理、变异、翻译、对齐与检测流程。
