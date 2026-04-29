# Quick Start Guide - POS Integration Features

## 5 Minutes Setup

### Step 1: Run Migration
```bash
python manage.py migrate
```

### Step 2: Start the Server
```bash
python manage.py runserver
```

### Step 3: Access Dashboard
Go to: http://localhost:8000/

---

## Using the Features

### Feature 1: Update Product Prices (No Hardcoding!)

**Before:** Prices were hardcoded in seed_data.py

**Now:**
1. Click **"Manage Prices"** button on dashboard
2. Update prices in the modal
3. Click **"Update"** button
4. Prices change immediately in the system

✅ Prices are now in the database, not hardcoded!

---

### Feature 2: Import Daily Sales from POS

**Before:** Had to manually enter each item

**Now:**
1. Export data from your POS system as JSON
2. Paste into **"Import from POS"** section
3. Click **"Import Transactions"** button
4. All items are automatically added!

#### Example POS Export JSON:
```json
[
    {
        "product_name": "Chicken",
        "weight": 2.5,
        "crate_wt": 0.5,
        "no_of_crates": 1,
        "birds_per_crate": 10,
        "group_no": "G1"
    },
    {
        "product_name": "Fish (Rohu)",
        "weight": 1.8,
        "crate_wt": 0.3,
        "no_of_crates": 1,
        "birds_per_crate": 0,
        "group_no": "G2"
    }
]
```

✅ No more manual data entry for POS items!

---

### Feature 3: View Today's Sales Summary

The dashboard now shows:
- **Total Revenue** (auto-calculated from all transactions)
- **Total Weight** (sum of all weights sold)
- **Transaction Count** (manual + imported from POS)

Includes breakdown by product!

---

## Daily Workflow

### Start of Day
1. Products already in database with prices
2. If prices changed, click "Manage Prices" and update

### During Day
1. Manual scale entries work as before
2. At end of day, import POS transactions

### End of Day
1. Check "Today's Summary" dashboard
2. Review all sales in "Today's Sales" section
3. Prepare for next day

---

## Key Changes Summary

| What | Before | After |
|------|--------|-------|
| **Prices** | Hardcoded in seed_data.py | Database + UI updates |
| **Daily Sales** | Manual entry | Import from POS system |
| **Price History** | No tracking | Auto-tracked with timestamps |
| **Sales View** | Only manual entries | Manual + POS combined |

---

## New API Endpoints

All available at `/api/`:

1. **`/api/update-price/`** (POST)
   - Change product prices
   
2. **`/api/import-pos-transactions/`** (POST)
   - Import batch transactions from POS
   
3. **`/api/daily-sales/`** (GET)
   - Get today's sales summary
   
4. **`/api/products/`** (GET)
   - Get all products with current prices

---

## Troubleshooting Checklist

- [ ] Did you run `python manage.py migrate`?
- [ ] Is the server running?
- [ ] Is the dashboard loading correctly?
- [ ] Can you see the "Manage Prices" button?
- [ ] Can you see the "Import from POS" section?

If yes to all → Everything is working! 🎉

---

## Next Steps

1. **Update today's prices** via "Manage Prices"
2. **Test POS import** with the example JSON above
3. **Check daily summary** refreshes correctly
4. **View admin panel** at /admin/ to see transactions by source

---

## File Locations

- **Dashboard:** http://localhost:8000/
- **Admin Panel:** http://localhost:8000/admin/
- **Report:** http://localhost:8000/report/
- **API Docs:** See POS_INTEGRATION_GUIDE.md

---

## Support

Full documentation: See `POS_INTEGRATION_GUIDE.md`

Questions?
- Check the guide for detailed API examples
- Review the example JSON format
- Verify database migration completed
