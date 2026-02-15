#!/usr/bin/env python3
"""
Generate hedge bot status report.

Shows:
- Active hedges count and details
- Last scan information
- Dashboard link
- System status
"""

import sys
from pathlib import Path
from datetime import datetime
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "polyclaw"))

from testing.database import HedgeDB, init_db

def get_dashboard_url():
    """Return dashboard URL."""
    return "http://107.174.92.36:8501"

def check_services():
    """Check if services are running."""
    import subprocess

    services = {
        'Discord Bot': lambda: subprocess.run(['pgrep', '-f', 'discord_hedge_bot.py'],
                                                capture_output=True).returncode == 0,
        'Dashboard': lambda: subprocess.run(['pgrep', '-f', 'streamlit.*dashboard.py'],
                                              capture_output=True).returncode == 0,
    }

    status = {}
    for name, check in services.items():
        try:
            status[name] = '✅ Running' if check() else '❌ Stopped'
        except:
            status[name] = '❓ Unknown'

    return status

def get_last_scan_info():
    """Get last scan information."""
    try:
        with HedgeDB() as db:
            cursor = db.conn.cursor()
            cursor.execute("""
                SELECT scan_timestamp, markets_scanned, hedges_found
                FROM scans
                ORDER BY id DESC
                LIMIT 1
            """)
            scan = cursor.fetchone()

            if scan:
                return {
                    'time': scan[0],
                    'markets_scanned': scan[1],
                    'hedges_found': scan[2]
                }
    except Exception as e:
        print(f"Error getting scan info: {e}")
    return None

def generate_report():
    """Generate status report."""
    print("=" * 60)
    print("🦞 HEDGE BOT STATUS REPORT")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()

    # Check services
    print("📡 SERVICES")
    print("-" * 40)
    services = check_services()
    for name, status in services.items():
        print(f"  {name}: {status}")
    print()

    # Active hedges
    print("📊 ACTIVE HEDGES")
    print("-" * 40)
    try:
        with HedgeDB() as db:
            hedges = db.get_active_hedges()
            print(f"  Total active: {len(hedges)}")

            if hedges:
                total_cost = sum(h.total_real_cost for h in hedges)
                avg_coverage = sum(h.coverage for h in hedges) / len(hedges) if hedges else 0

                print(f"  Total cost: ${total_cost:.2f}")
                print(f"  Avg coverage: {avg_coverage*100:.1f}%")
                print(f"  Tier breakdown:")

                tier_counts = {}
                for h in hedges:
                    tier_counts[h.tier] = tier_counts.get(h.tier, 0) + 1

                for tier, count in sorted(tier_counts.items()):
                    print(f"    Tier {tier}: {count}")
            else:
                print("  No active hedges")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print()

    # Last scan
    print("🔍 LAST SCAN")
    print("-" * 40)
    scan_info = get_last_scan_info()
    if scan_info:
        scan_time = datetime.fromisoformat(scan_info['time'].replace('Z', '+00:00'))
        time_ago = datetime.now(scan_time.tzinfo) - scan_time
        hours_ago = time_ago.total_seconds() / 3600

        print(f"  Time: {scan_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Age: {hours_ago:.1f} hours ago")
        print(f"  Markets scanned: {scan_info['markets_scanned']}")
        print(f"  Hedges found: {scan_info['hedges_found']}")
    else:
        print("  No scan history found")
    print()

    # Dashboard
    print("📈 DASHBOARD")
    print("-" * 40)
    print(f"  URL: {get_dashboard_url()}")
    print()

    # Log location
    print("📝 LOGS")
    print("-" * 40)
    print("  Latest monitor: logs/hedge_monitor_$(date +%Y%m%d).log")
    print("  Cron monitor:    logs/cron_hedge_monitor.log")
    print()

    print("=" * 60)
    print("Run 'python3 hedge_status_report.py' to refresh this report")
    print("=" * 60)

if __name__ == "__main__":
    generate_report()
