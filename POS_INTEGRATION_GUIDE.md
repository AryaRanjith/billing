# POS Integration Guide

## Overview
This system now supports:
1. **Dynamic Price Management** - Update product prices through the UI
2. **POS System Integration** - Import daily sold items from your POS application
3. **Daily Sales Dashboard** - View today's sales summary by product
4. **Price History** - Track all price changes

---

## 1. Database Migration

Before using these features, run the migration:

```bash
python manage.py migrate
```

This creates the `PriceHistory` table and updates the `Transaction` table with new fields.

---

## 2. Price Management

### Via UI Dashboard

1. Click **"Manage Prices"** button on the dashboard
2. A modal opens showing all products with current prices
3. Enter the new price and click **"Update"** button
4. Price is updated immediately and a history record is created

### Via API

```bash
POST /api/update-price/
Content-Type: application/json

{
    "product_id": 1,
    "new_price": 350.00
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Price updated from 250 to 350",
    "product": {
        "id": 1,
        "name": "Chicken",
        "price_per_kg": 350.0
    }
}
```

---

## 3. POS Integration

### Import Transactions from POS System

#### Option 1: UI Dashboard

1. Navigate to **"Import from POS"** section on the dashboard
2. Paste JSON data from your POS system in the textarea
3. Click **"Import Transactions"** button

#### Option 2: API Endpoint

```bash
POST /api/import-pos-transactions/
Content-Type: application/json

{
    "transactions": [
        {
            "product_name": "Chicken",
            "weight": 2.5,
            "crate_wt": 0.5,
            "no_of_crates": 1,
            "birds_per_crate": 10,
            "group_no": "G1",
            "remark": "Fresh batch",
            "pos_transaction_id": "POS001"
        },
        {
            "product_name": "Fish (Rohu)",
            "weight": 1.8,
            "crate_wt": 0.3,
            "no_of_crates": 1,
            "birds_per_crate": 0,
            "group_no": "G2",
            "pos_transaction_id": "POS002"
        }
    ]
}
```

**Response:**
```json
{
    "status": "success",
    "message": "2 transactions imported",
    "transactions": [
        {
            "id": 5,
            "product": "Chicken",
            "weight": 2.5,
            "total_price": 875.0
        },
        {
            "id": 6,
            "product": "Fish (Rohu)",
            "weight": 1.8,
            "total_price": 540.0
        }
    ]
}
```

### JSON Format for POS Data

Each transaction object should have:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_name` | string | Yes | Name of the product |
| `weight` | float | Yes | Net weight in kg |
| `crate_wt` | float | No | Weight of crate (default: 0) |
| `no_of_crates` | int | No | Number of crates (default: 1) |
| `birds_per_crate` | int | No | Number of birds per crate (default: 0) |
| `group_no` | string | No | Group identification |
| `remark` | string | No | Any additional notes |
| `pos_transaction_id` | string | No | Reference ID from POS system |

---

## 4. Daily Sales Report

### Get Today's Sales Summary

```bash
GET /api/daily-sales/
```

**Response:**
```json
{
    "status": "success",
    "date": "2026-04-29",
    "total_revenue": 1850.50,
    "total_weight": 15.8,
    "transactions": 5,
    "daily_sales": [
        {
            "product": "Chicken",
            "price_per_kg": 350.0,
            "total_weight": 5.5,
            "count": 2,
            "total_revenue": 1925.0
        },
        {
            "product": "Fish (Rohu)",
            "price_per_kg": 300.0,
            "total_weight": 3.2,
            "count": 1,
            "total_revenue": 960.0
        }
    ]
}
```

### Get Sales for Specific Date

```bash
GET /api/daily-sales/?date=2026-04-28
```

Query Parameters:
- `date` (optional): YYYY-MM-DD format. Defaults to today if not provided.

---

## 5. Get All Products with Current Prices

```bash
GET /api/products/
```

**Response:**
```json
{
    "status": "success",
    "products": [
        {
            "id": 1,
            "name": "Chicken",
            "price_per_kg": "350.00"
        },
        {
            "id": 2,
            "name": "Mutton",
            "price_per_kg": "800.00"
        },
        {
            "id": 3,
            "name": "Fish (Rohu)",
            "price_per_kg": "300.00"
        },
        {
            "id": 4,
            "name": "Prawns",
            "price_per_kg": "600.00"
        }
    ]
}
```

---

## 6. Transaction Source Tracking

Every transaction now records its source:

- **`manual`**: Manually entered through the UI with weighing scale
- **`pos`**: Imported from the POS system

This helps distinguish between:
- Direct sales with weighing scale
- Inventory transfers or pre-packaged items from POS

---

## 7. Price History

View price changes in the admin panel:

1. Go to `/admin/`
2. Select **"Price Histories"** under Billing
3. See all price changes with timestamps

Each record shows:
- Product name
- Old price
- New price
- When the change occurred

---

## 8. Integration with Your POS System

### Exporting Data from POS

Your POS system should export transactions as JSON in this format:

```json
{
    "transactions": [
        {
            "product_name": "Chicken",
            "weight": 2.5,
            "crate_wt": 0.5,
            "no_of_crates": 1,
            "birds_per_crate": 10,
            "group_no": "G1",
            "pos_transaction_id": "20260429-001"
        }
    ]
}
```

### Scheduling Daily Imports

For automated import from POS at the end of each day:

1. Create a script that exports data from POS
2. Call the `/api/import-pos-transactions/` endpoint
3. Use a task scheduler (cron job or APScheduler) to run daily

Example cron job:
```bash
# Run at 11 PM daily
0 23 * * * curl -X POST http://localhost:8000/api/import-pos-transactions/ \
    -H "Content-Type: application/json" \
    -d @/path/to/pos_export.json
```

---

## 9. Admin Panel Updates

New fields in Transaction admin:

- **source**: Manual or POS
- **price_per_kg**: Price at the time of transaction
- **pos_transaction_id**: Reference to POS system

Filter transactions by:
- Source (Manual/POS)
- Date range
- Product

---

## 10. Key Features

✅ **No Hardcoded Prices** - All prices stored in database
✅ **Dynamic Price Updates** - Change prices anytime from UI
✅ **Price History** - Audit trail of price changes
✅ **Automated POS Import** - Pull data directly from POS system
✅ **Daily Sales Dashboard** - Real-time sales by product
✅ **Source Tracking** - Know where each transaction came from
✅ **API-First Design** - Easy integration with other systems
✅ **Backward Compatible** - Manual entry still works

---

## 11. Example Workflow

### Day 1: Setup
1. Create products in database
2. Set initial prices via "Manage Prices"

### Day 2-N: Daily Operations

**Morning:**
1. Connect Bluetooth weighing scale
2. Manual entries for scale-based sales
3. Prices auto-loaded from database

**End of Day:**
1. Export transactions from POS system
2. Paste JSON in "Import from POS" section
3. Click "Import Transactions"
4. View "Today's Summary" dashboard
5. Update prices for next day if needed

---

## 12. Troubleshooting

### Transactions not importing
- Check JSON format is valid
- Ensure all required fields are present
- Check product names match exactly

### Prices not updating
- Clear browser cache
- Check CSRF token is correct (Django requires it)
- Verify API response for error messages

### Daily sales not showing
- Ensure transactions exist for today
- Check transactions have price_per_kg set
- Use "Refresh Summary" button

---

## 13. Database Models

### PriceHistory
```
- product (FK to Product)
- old_price
- new_price
- changed_at (datetime)
```

### Transaction (Updated)
```
- product (FK to Product)
- weight
- price_per_kg (NEW)
- source (NEW) - manual or pos
- pos_transaction_id (NEW)
- ... existing fields ...
```

---

## 14. API Summary Table

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/update-price/` | POST | Update product price |
| `/api/import-pos-transactions/` | POST | Import from POS |
| `/api/daily-sales/` | GET | Today's sales summary |
| `/api/products/` | GET | All products & prices |

---

## Support

For issues or questions, check:
1. Database migration completed successfully
2. Django CSRF token included in POST requests
3. JSON format is valid (use JSONLint if unsure)
4. Product names in POS data match database
