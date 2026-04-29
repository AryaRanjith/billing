#!/usr/bin/env python
"""
Example POS Data Export Script
==============================

This script demonstrates how to export transaction data from a POS system
and format it for import into the Billing System.

Usage:
    python pos_export.py > pos_data.json
    # Then paste the output into the UI or send to API

Author: POS Integration Team
"""

import json
from datetime import datetime, timedelta
import random


def generate_sample_pos_data():
    """
    Generate sample POS data for demonstration
    
    In a real system, this would query your POS database
    """
    products = ['Chicken', 'Mutton', 'Fish (Rohu)', 'Prawns']
    groups = ['G1', 'G2', 'G3', 'G4', 'G5']
    
    transactions = []
    
    # Generate 10-20 random transactions for today
    num_transactions = random.randint(10, 20)
    
    for i in range(num_transactions):
        product = random.choice(products)
        weight = round(random.uniform(0.5, 5.0), 3)
        crate_wt = round(random.uniform(0.2, 0.8), 3)
        no_of_crates = random.randint(1, 3)
        birds_per_crate = random.randint(5, 15) if product == 'Chicken' else 0
        
        transaction = {
            'product_name': product,
            'weight': weight,
            'crate_wt': crate_wt,
            'no_of_crates': no_of_crates,
            'birds_per_crate': birds_per_crate,
            'group_no': random.choice(groups),
            'remark': f'Batch {i+1}' if random.random() > 0.7 else '',
            'pos_transaction_id': f'POS{datetime.now().strftime("%Y%m%d")}{str(i+1).zfill(3)}'
        }
        transactions.append(transaction)
    
    return transactions


def export_today_transactions(database_connection=None):
    """
    Export today's transactions from POS database
    
    Args:
        database_connection: Your POS database connection
    
    Returns:
        List of transaction dictionaries
    """
    
    # Example: If using SQLite (adjust for your POS database)
    # import sqlite3
    # conn = sqlite3.connect('pos_database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM transactions WHERE date = TODAY()")
    # rows = cursor.fetchall()
    # ... process rows and return as list of dicts
    
    # For this example, we'll generate sample data
    return generate_sample_pos_data()


def export_date_range_transactions(start_date, end_date, database_connection=None):
    """
    Export transactions for a specific date range
    
    Args:
        start_date: datetime object for start
        end_date: datetime object for end
        database_connection: Your POS database connection
    
    Returns:
        List of transaction dictionaries
    """
    
    # Similar to above, but filtered by date range
    # This is a placeholder - adjust to your POS system
    return generate_sample_pos_data()


def format_for_import(transactions):
    """
    Format transactions for import into Billing System
    
    Args:
        transactions: List of transaction dictionaries
    
    Returns:
        Formatted JSON string ready for import
    """
    
    return json.dumps({
        'transactions': transactions
    }, indent=2)


def main():
    """
    Main export function
    
    This can be called by:
    1. Command line: python pos_export.py
    2. Scheduler (cron, APScheduler, etc.)
    3. Another script
    """
    
    # Export today's transactions
    transactions = export_today_transactions()
    
    # Format for import
    json_output = format_for_import(transactions)
    
    # Print to stdout (can be redirected to file)
    print(json_output)
    
    # Or save to file
    # with open(f'pos_export_{datetime.now().strftime("%Y%m%d")}.json', 'w') as f:
    #     f.write(json_output)


if __name__ == '__main__':
    main()


# ============================================================================
# INTEGRATION EXAMPLES
# ============================================================================

"""
Example 1: Export and Save to File
-----------------------------------

    from pos_export import export_today_transactions, format_for_import
    
    transactions = export_today_transactions()
    json_data = format_for_import(transactions)
    
    with open('pos_data.json', 'w') as f:
        f.write(json_data)


Example 2: Export and Send to Billing System API
-------------------------------------------------

    import requests
    import json
    from pos_export import export_today_transactions
    
    transactions = export_today_transactions()
    
    response = requests.post(
        'http://localhost:8000/api/import-pos-transactions/',
        json={'transactions': transactions},
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        print(f"✓ Imported {len(transactions)} transactions")
    else:
        print(f"✗ Error: {response.text}")


Example 3: Scheduled Daily Export
----------------------------------

    Create a file: schedule_pos_export.py
    
    from apscheduler.schedulers.background import BackgroundScheduler
    from pos_export import export_today_transactions, format_for_import
    import requests
    
    def daily_export():
        transactions = export_today_transactions()
        response = requests.post(
            'http://localhost:8000/api/import-pos-transactions/',
            json={'transactions': transactions}
        )
        print(f"Daily export completed: {response.status_code}")
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_export, 'cron', hour=23, minute=30)  # 11:30 PM daily
    scheduler.start()


Example 4: Cron Job (Linux/Mac)
-------------------------------

    # Add to crontab: crontab -e
    
    # Export at 11 PM daily and save to file
    0 23 * * * cd /path/to/billing && python pos_export.py > pos_data.json
    
    # Export and auto-import at 11 PM daily
    0 23 * * * cd /path/to/billing && python -c "
        import requests
        from pos_export import export_today_transactions
        r = requests.post('http://localhost:8000/api/import-pos-transactions/',
                         json={'transactions': export_today_transactions()})
    "


Example 5: Windows Task Scheduler
--------------------------------

    Create a batch file: pos_export.bat
    
    @echo off
    cd C:\path\to\billing
    python pos_export.py > pos_data.json
    curl -X POST http://localhost:8000/api/import-pos-transactions/ ^
         -H "Content-Type: application/json" ^
         -d @pos_data.json
    
    Then create a scheduled task to run pos_export.bat daily at 11 PM


Example 6: Direct SQL Query (if using your POS SQLite database)
--------------------------------------------------------------

    import sqlite3
    from datetime import datetime
    
    def export_from_sqlite(db_path):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        today = datetime.now().date()
        cursor.execute('''
            SELECT product_name, weight, crate_wt, no_of_crates, 
                   birds_per_crate, group_no, transaction_id
            FROM transactions
            WHERE DATE(timestamp) = ?
        ''', (today,))
        
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return transactions
    
    # Usage
    transactions = export_from_sqlite('/path/to/pos.db')
    json_data = format_for_import(transactions)
    print(json_data)

"""
