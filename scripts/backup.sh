#!/bin/bash
# opcp-introduction Backup Script (PostgreSQL)

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/opcp-introduction_backup_$DATE.sql.gz"

mkdir -p "$BACKUP_DIR"

# Resolve the PostgreSQL container for this project
DB_CONTAINER=$(env HTTPS_PORT=6184 HTTP_PORT=6185 HTTPS_PORT1=6186 HTTP_PORT1=6187 HTTPS_PORT2=6188 HTTP_PORT2=6189 HTTPS_PORT3=6190 HTTP_PORT3=6191 HTTPS_PORT4=6192 HTTP_PORT4=6193 HTTPS_PORT5=6194 HTTP_PORT5=6195 USER_ID=1 docker-compose -p "opcp-introduction-1-6184" -f docker-compose.yml ps -q postgres 2>/dev/null || env HTTPS_PORT=6184 HTTP_PORT=6185 HTTPS_PORT1=6186 HTTP_PORT1=6187 HTTPS_PORT2=6188 HTTP_PORT2=6189 HTTPS_PORT3=6190 HTTP_PORT3=6191 HTTPS_PORT4=6192 HTTP_PORT4=6193 HTTPS_PORT5=6194 HTTP_PORT5=6195 USER_ID=1 docker-compose -p "opcp-introduction-1-6184" -f docker-compose.yml ps -q db 2>/dev/null)

# Resolve credentials (fall back to .env.prod when available)
DB_NAME="${POSTGRES_DB:-opcp-introduction}"
DB_USER="${POSTGRES_USER:-opcp-introduction}"
if [[ -f .env.prod ]]; then
    source .env.prod 2>/dev/null || true
    DB_NAME="${POSTGRES_DB:-$DB_NAME}"
    DB_USER="${POSTGRES_USER:-$DB_USER}"
fi

echo "Creating backup: $BACKUP_FILE"
docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

if [[ $? -eq 0 && -s "$BACKUP_FILE" ]]; then
    echo "Backup created successfully: $BACKUP_FILE"

    # Keep only last 7 backups
    ls -t "$BACKUP_DIR"/opcp-introduction_backup_*.sql.gz | tail -n +8 | xargs -r rm
    echo "Old backups cleaned up"
else
    echo "Backup failed!"
    exit 1
fi