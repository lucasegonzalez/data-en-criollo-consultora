#!/bin/bash
# backup.sh — Daily backup of SQLite + config to Backblaze B2
set -euo pipefail

# Config
BACKUP_DIR="/tmp/consultora-backup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
B2_BUCKET="${B2_BUCKET:-consultora-backups}"
B2_APP_KEY_ID="${B2_APP_KEY_ID}"
B2_APP_KEY="${B2_APP_KEY}"

echo "=== Backup started: $TIMESTAMP ==="

# Create temp directory
mkdir -p "$BACKUP_DIR"

# Backup SQLite database
if [ -f "./data/consultora.db" ]; then
    cp "./data/consultora.db" "$BACKUP_DIR/consultora_$TIMESTAMP.db"
    echo "✅ SQLite backed up"
else
    echo "⚠️ No database file found"
fi

# Backup env file (sanitized — remove secrets)
if [ -f ".env" ]; then
    cp ".env" "$BACKUP_DIR/.env_$TIMESTAMP"
    echo "✅ .env backed up"
fi

# Backup docker-compose and traefik config
cp "docker-compose.yml" "$BACKUP_DIR/"
cp -r "traefik" "$BACKUP_DIR/traefik"
echo "✅ Config files backed up"

# If B2 tools are installed, upload
if command -v b2 &> /dev/null && [ -n "$B2_APP_KEY_ID" ]; then
    b2 authorize-account "$B2_APP_KEY_ID" "$B2_APP_KEY" > /dev/null 2>&1
    b2 upload-file "$B2_BUCKET" "$BACKUP_DIR" "consultora_$TIMESTAMP.tar.gz" > /dev/null 2>&1
    echo "✅ Uploaded to Backblaze B2"
else
    echo "⚠️ B2 not configured — backup saved to $BACKUP_DIR"
fi

# Cleanup
rm -rf "$BACKUP_DIR"
echo "=== Backup complete ==="
