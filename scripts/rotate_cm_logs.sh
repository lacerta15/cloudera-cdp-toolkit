#!/usr/bin/env bash
# Rotate and compress Cloudera Manager server logs
set -euo pipefail
LOG_DIR="/var/log/cloudera-scm-server"
MAX_SIZE_MB="${MAX_SIZE_MB:-500}"
KEEP_DAYS="${KEEP_DAYS:-14}"

[ ! -d "$LOG_DIR" ] && echo "Log dir not found: $LOG_DIR" && exit 0

echo "[$(date)] Starting CM log rotation"
# Compress logs older than 1 day
find "$LOG_DIR" -name "*.log.*" -not -name "*.gz" -mtime +1 -exec gzip -f {} \;
# Delete old compressed logs
find "$LOG_DIR" -name "*.gz" -mtime "+${KEEP_DAYS}" -delete
# Check current log size
SIZE=$(du -sm "$LOG_DIR" | cut -f1)
echo "Log directory size: ${SIZE}MB (limit: ${MAX_SIZE_MB}MB)"
[ "$SIZE" -gt "$MAX_SIZE_MB" ] && echo "[WARN] Log dir exceeds limit!"
echo "[$(date)] Rotation complete"
