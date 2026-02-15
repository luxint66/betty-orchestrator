#!/bin/bash
# Cron-based hedge scanning and notification system

cd /home/luxinterior/.openclaw/workspace

# Configuration
SCAN_SCRIPT="/home/luxinterior/.openclaw/workspace/hedge_test"
BOT_SCRIPT="/home/luxinterior/.openclaw/workspace/notify_hedges.sh"  # Will create
LOCK_FILE="/tmp/hedge_scan.lock"
LOG_FILE="/tmp/hedge_scan.log"
MAX_SCAN_AGE_HOURS=24  # How old scan data can be before refreshing

# Scanning parameters
SCAN_LIMIT=50  # Markets to scan
MIN_COVERAGE=0.85  # Minimum coverage to report
TIER_FILTER=2  # Maximum tier to include

# Telegram configuration (if you want notifications)
TELEGRAM_BOT_TOKEN=""  # Set this if you want notifications
TELEGRAM_CHAT_ID=""  # Your chat ID for private notifications

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$1" >> "$LOG_FILE"
}

scan_hedge_markets() {
    # Check if another scan is running
    if [ -f "$LOCK_FILE" ]; then
        lock_age=$(($(date +%s) - $(date +%s -r "$LOCK_FILE")))
        lock_age_min=$((lock_age / 60))
        
        if [ $lock_age_min -lt 10 ]; then
            echo "⚠️  Recent scan already running (age: ${lock_age_min}m). Skipping."
            log_message "Scan skipped: Recent scan in progress"
            return 1
    fi

    # Create lock
    echo "$(date '+%s')" > "$LOCK_FILE"

    # Run hedge scan
    log_message "Starting hedge scan: limit=$SCAN_LIMIT, min_coverage=$MIN_COVERAGE, tier_filter=$TIER_FILTER"

    SCAN_OUTPUT=$($SCAN_SCRIPT scan \
        --limit $SCAN_LIMIT \
        --min-coverage $MIN_COVERAGE \
        --tier $TIER_FILTER \
        2>&1)

    EXIT_CODE=$?
    echo "Exit code: $EXIT_CODE" >> "$LOG_FILE"

    # Check for hedges found
    if echo "$SCAN_OUTPUT" | grep -q "hedges logged:"; then
        HEDGES_FOUND=$(echo "$SCAN_OUTPUT" | grep -o "hedges logged: [0-9]*")
        log_message "✅ Scan complete: $HEDGES_FOUND hedges logged"
        
        # Send notification if configured
        if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
            log_message "Sending Telegram notification..."
            NOTIFICATION="🦞 **Hedge Alert!**

Found $HEDGES_FOUND new hedge opportunities:

$(echo "$SCAN_OUTPUT" | grep -A 20 "hedges logged:" | tail -20)

Use \`/hedge_db $SCAN_LIMIT\` to see all hedges."

View dashboard: http://107.174.92.36:8501"
"

            # Send notification via Telegram bot (would need to implement)
            # For now, just log the notification
            echo "$NOTIFICATION" >> "$TELEGRAM_LOG"
        fi
    else
        log_message "✅ Scan complete: No hedges found meeting criteria"

    # Update last scan time
    echo "$(date '+%s')" > "/tmp/last_hedge_scan"

    # Remove lock
    rm -f "$LOCK_FILE"

    return $EXIT_CODE
}

check_scan_freshness() {
    # Check how old the last scan was
    if [ -f "/tmp/last_hedge_scan" ]; then
        last_scan=$(cat /tmp/last_hedge_scan)
        age=$(($(date +%s) - $(date +%s -r "$last_scan")))
        age_hours=$((age / 3600))
        
        if [ $age_hours -ge $MAX_SCAN_AGE_HOURS ]; then
            log_message "Last scan is ${age_hours}h old. Running fresh scan."
            return 0
        else
            log_message "Last scan is ${age_hours}h old. Using existing data."
            return 1
    fi
    
    log_message "No previous scan found. Starting fresh scan."
    return 0
}

run_scheduled_scan() {
    log_message "=== Scheduled Scan ==="

    # Check if we need a fresh scan
    if ! check_scan_freshness; then
        return 0
    fi

    # Run the scan
    scan_hedge_markets
}

show_status() {
    log_message "=== Hedge Scan Status ==="

    # Check last scan
    if [ -f "/tmp/last_hedge_scan" ]; then
        last_scan=$(cat /tmp/last_hedge_scan)
        age=$(($(date +%s) - $(date +%s -r "$last_scan")))
        age_hours=$((age / 3600))
        log_message "Last scan: $(date -d "$last_scan" '+%Y-%m-%d %H:%M') (${age_hours}h ago)"
    else
        log_message "No previous scans"
    fi

    # Check if scan is currently running
    if [ -f "$LOCK_FILE" ]; then
        lock_age=$(($(date +%s) - $(date +%s -r "$LOCK_FILE")))
        lock_age_min=$((lock_age / 60))
        if [ $lock_age_min -lt 5 ]; then
            log_message "Status: Scanning in progress (${lock_age_min}m ago)"
        else
            log_message "Status: Idle (last lock: ${lock_age_min}m ago)"
    else
        log_message "Status: Idle (no lock file)"
    fi

    # Show recent logs
    if [ -f "$LOG_FILE" ]; then
        log_message "Recent logs (last 10 lines):"
        tail -10 "$LOG_FILE"
    fi
}

# =============================================================================
# Main
# =============================================================================

case "$1" in
    scan)
        run_scheduled_scan
        ;;
    status)
        show_status
        ;;
    force)
        log_message "Forcing fresh scan (ignoring freshness check)..."
        rm -f "/tmp/last_hedge_scan"
        run_scheduled_scan
        ;;
    test)
        echo "Test mode: Dry run with scan_limit=5"
        SCAN_LIMIT=5
        run_scheduled_scan
        ;;
    logs)
        if [ -f "$LOG_FILE" ]; then
            cat "$LOG_FILE"
        else
            echo "No log file found"
        fi
        ;;
    *)
        echo "Usage: $0 {scan|status|force|test|logs}"
        echo ""
        echo "Commands:"
        echo "  scan    - Run scheduled hedge scan"
        echo "  status  - Show scan status"
        echo "  force   - Force fresh scan (ignore freshness)"
        echo "  test    - Test scan (limit=5)"
        echo "  logs    - Show scan logs"
        echo ""
        echo "Configuration (edit this script):"
        echo "  SCAN_LIMIT=$SCAN_LIMIT"
        echo "  MIN_COVERAGE=$MIN_COVERAGE"
        echo "  TIER_FILTER=$TIER_FILTER"
        echo "  MAX_SCAN_AGE_HOURS=$MAX_SCAN_AGE_HOURS"
        echo ""
        echo "Telegram Notification (if enabled):"
        echo "  TELEGRAM_BOT_TOKEN='$TELEGRAM_BOT_TOKEN'"
        echo "  TELEGRAM_CHAT_ID='$TELEGRAM_CHAT_ID'"
        exit 1
        ;;
esac
