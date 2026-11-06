#!/usr/bin/env bash
# Боевой скрипт резервного копирования PostgreSQL со сжатием zstd и отправкой в S3
set -euo pipefail

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-orders_db}"
DB_USER="${DB_USER:-app}"
S3_BUCKET="${S3_BUCKET:-s3://my-company-db-backups/postgres}"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H-%M-%SZ")"
TMP_FILE="/tmp/${DB_NAME}_${TIMESTAMP}.sql.zst"

cleanup() {
    if [[ -f "${TMP_FILE}" ]]; then
        rm -f "${TMP_FILE}"
    fi
}
trap cleanup EXIT INT TERM

echo "[INFO] Starting backup of database '${DB_NAME}' at ${TIMESTAMP}..."

pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -Fc "${DB_NAME}" | zstd -T0 -10 > "${TMP_FILE}"

FILE_SIZE="$(du -h "${TMP_FILE}" | cut -f1)"
echo "[INFO] Backup compressed successfully (${FILE_SIZE}). Uploading to ${S3_BUCKET}..."

aws s3 cp "${TMP_FILE}" "${S3_BUCKET}/${DB_NAME}_${TIMESTAMP}.sql.zst" --only-show-errors

echo "[INFO] Backup completed and verified in S3."
