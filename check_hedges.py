#!/usr/bin/env python3
"""Quick check of active hedges."""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from testing.database import HedgeDB

with HedgeDB() as db:
    h = db.get_active_hedges()
    print(f'Active hedges: {len(h)}')
    if h:
        total_cost = sum(x.total_real_cost for x in h)
        avg_coverage = sum(x.coverage for x in h) / len(h)
        print(f'Total cost: ${total_cost:.2f}')
        print(f'Avg coverage: {avg_coverage*100:.1f}%')
        for x in h:
            print(f'  ID: {x.id}, Coverage: {x.coverage*100:.1f}%, Tier: {x.tier}, Cost: ${x.total_real_cost:.2f}')
    else:
        print('No active hedges in database')

    # Last scan
    try:
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT scan_timestamp, markets_scanned, hedges_found
            FROM scans
            ORDER BY id DESC
            LIMIT 1
        """)
        scan = cursor.fetchone()
        if scan:
            scan_time = datetime.fromisoformat(scan[0].replace('Z', '+00:00'))
            time_ago = datetime.now(scan_time.tzinfo) - scan_time
            hours_ago = time_ago.total_seconds() / 3600
            print(f'\nLast scan: {scan_time.strftime("%Y-%m-%d %H:%M")} ({hours_ago:.1f}h ago)')
            print(f'Markets: {scan[1]}, Hedges found: {scan[2]}')
    except:
        pass
