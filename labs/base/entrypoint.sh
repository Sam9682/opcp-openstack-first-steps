#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Validate required environment variables for OpenStack credentials.
# ------------------------------------------------------------------
REQUIRED_VARS=(OS_AUTH_URL OS_USERNAME OS_PASSWORD OS_PROJECT_NAME OS_DOMAIN_NAME)

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var:-}" ]; then
        echo "ERROR: Required environment variable $var is not set." >&2
        exit 1
    fi
done

# ------------------------------------------------------------------
# Test connectivity to the OpenStack endpoint.
# ------------------------------------------------------------------
ENDPOINT="${OS_AUTH_URL}"

echo "Testing connectivity to OpenStack endpoint: ${ENDPOINT} ..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 "${ENDPOINT}" 2>/dev/null) || true

if [ -z "${HTTP_CODE}" ] || [ "${HTTP_CODE}" = "000" ]; then
    echo "ERROR: Cannot reach OpenStack endpoint at ${ENDPOINT}: connection failed" >&2
    exit 1
fi

echo "OpenStack endpoint reachable (HTTP ${HTTP_CODE})."

# ------------------------------------------------------------------
# Launch the lab runner.
# ------------------------------------------------------------------
exec python3 -m labs.core.runner "$@"
