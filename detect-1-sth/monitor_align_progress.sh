#!/usr/bin/env bash

set -u

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESULTS_DIR="$ROOT_DIR/results"
AREAS=(Subtitles Science Laws News Thesis)
MODELS=(google bing mbart)

line_count() {
    local f="$1"
    if [[ -f "$f" ]]; then
        wc -l < "$f"
    else
        echo 0
    fi
}

safe_pct() {
    local cur="$1"
    local total="$2"
    if [[ "$total" -le 0 ]]; then
        echo "0.0"
    else
        awk -v c="$cur" -v t="$total" 'BEGIN { printf "%.1f", (c*100.0)/t }'
    fi
}

while true; do
    clear
    echo "=== Alignment Realtime Progress ==="
    echo "Time: $(date '+%F %T')"
    echo "Results: $RESULTS_DIR"
    echo
    printf "%-10s %-7s %12s %12s %12s %10s\n" "Area" "Model" "origin" "info" "bert" "total%"
    printf "%-10s %-7s %12s %12s %12s %10s\n" "----------" "-------" "------------" "------------" "------------" "----------"

    grand_cur=0
    grand_total=0

    for area in "${AREAS[@]}"; do
        area_dir="$RESULTS_DIR/${area}-detect"
        origin_total=$(line_count "$area_dir/originSentences.txt")
        info_total=$(line_count "$area_dir/phrase_infoinsertmutants.txt")
        bert_total=$(line_count "$area_dir/phrase_bertinsertmutants.txt")
        row_total=$((origin_total + info_total + bert_total))

        for model in "${MODELS[@]}"; do
            align_dir="$area_dir/align_${model}"
            origin_cur=$(line_count "$align_dir/origin_align.txt")
            info_cur=$(line_count "$align_dir/phrase_infoinsertmutants_align.txt")
            bert_cur=$(line_count "$align_dir/phrase_bertinsertmutants_align.txt")
            row_cur=$((origin_cur + info_cur + bert_cur))
            pct=$(safe_pct "$row_cur" "$row_total")

            printf "%-10s %-7s %6d/%-5d %6d/%-5d %6d/%-5d %9s%%\n" \
                "$area" "$model" \
                "$origin_cur" "$origin_total" \
                "$info_cur" "$info_total" \
                "$bert_cur" "$bert_total" \
                "$pct"

            grand_cur=$((grand_cur + row_cur))
            grand_total=$((grand_total + row_total))
        done
    done

    overall_pct=$(safe_pct "$grand_cur" "$grand_total")
    echo
    echo "Overall: $grand_cur / $grand_total (${overall_pct}%)"
    echo "Press Ctrl+C to stop monitoring. Refresh every 2s."
    sleep 2
done
