#!/bin/bash
# 变异生成进度监控脚本

echo "=========================================="
echo "TermMT 变异生成进度监控 (2026-03-16)"
echo "=========================================="
echo ""
echo "启动时间: $(date)"
echo "监控日志: /home/cysds/TermMT/mutant-1-sth/mutant_full.log"
echo ""

DOMAINS=("Subtitles" "Science" "Laws" "News" "Thesis")
LOG_FILE="/home/cysds/TermMT/mutant-1-sth/mutant_full.log"
RESULT_DIR="/home/cysds/TermMT/data/mutant_results"

# 监控函数
check_progress() {
    echo "---[$(date '+%Y-%m-%d %H:%M:%S')]---"
    
    # 检查进程
    if pgrep -f "mutant.py" > /dev/null; then
        echo "✓ 脚本运行中..."
        ps aux | grep mutant.py | grep -v grep | head -1 | awk '{print "  进程ID: " $2 ", CPU: " $3 "%, 内存: " $4 "%"}'
    else
        echo "✗ 脚本未运行"
    fi
    
    echo ""
    
    # 检查各领域进度
    for domain in "${DOMAINS[@]}"; do
        if grep -q "start processing $domain" "$LOG_FILE"; then
            if grep -q "start processing $domain" "$LOG_FILE"; then
                last_progress=$(grep "processing $domain" "$LOG_FILE" | tail -1)
                echo "  $domain: $last_progress"
            fi
        fi
    done
    
    echo ""
    
    # 检查产物
    echo "已产出的结果文件:"
    find "$RESULT_DIR" -name "*.jsonl" 2>/dev/null | while read f; do
        lines=$(wc -l < "$f")
        echo "  $(basename $(dirname $f)): $lines 条记录"
    done
    
    if [ ! -d "$RESULT_DIR" ] || [ -z "$(find $RESULT_DIR -name '*.jsonl' 2>/dev/null)" ]; then
        echo "  (暂无产物)"
    fi
    
    echo ""
}

# 持续监控
check_progress
