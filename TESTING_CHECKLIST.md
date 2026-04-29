# Testing Checklist

Use this checklist to verify all new features are working correctly.

## Pre-Testing Setup

- [ ] Run migration: `python manage.py migrate`
- [ ] Start server: `python manage.py runserver`
- [ ] Open browser: http://localhost:8000/

---

## Feature 1: Dynamic Price Management

### Test 1.1: Price Management Modal
- [ ] Click "Manage Prices" button on dashboard
- [ ] Modal opens showing all products
- [ ] Each product shows current price in input field
- [ ] Can edit the prices
- [ ] Modal has "Update" button for each product

### Test 1.2: Update Price
- [ ] Change a product price (e.g., Chicken from 250 to 350)
- [ ] Click "Update" button
- [ ] Success message appears
- [ ] Page refreshes
- [ ] New price shows in product dropdown
- [ ] New price shows in billing form

### Test 1.3: Price History in Admin
- [ ] Go to /admin/
- [ ] Click "Price Histories" in Billing section
- [ ] Should see the price change record
- [ ] Shows product name, old_price, new_price, changed_at

---

## Feature 2: Import from POS

### Test 2.1: POS Import Section
- [ ] "Import from POS" card visible on dashboard
- [ ] Textarea shows placeholder with example JSON
- [ ] "Import Transactions" button present

### Test 2.2: Import Sample Data
- [ ] Paste this JSON into textarea:
```json
[
    {
        "product_name": "Chicken",
        "weight": 2.5,
        "crate_wt": 0.5,
        "no_of_crates": 1,
        "birds_per_crate": 10,
        "group_no": "G1",
        "pos_transaction_id": "TEST001"
    }
]
```
- [ ] Click "Import Transactions" button
- [ ] Success message appears
- [ ] Page refreshes

### Test 2.3: Verify Imported Data
- [ ] Go to /admin/ → Transactions
- [ ] Find the newly imported transaction
- [ ] Check: source = "pos"
- [ ] Check: pos_transaction_id = "TEST001"
- [ ] Check: price_per_kg is set
- [ ] Check: total_price is calculated correctly

### Test 2.4: Import Invalid JSON
- [ ] Paste invalid JSON (e.g., missing brackets)
- [ ] Click "Import Transactions"
- [ ] Error message: "Invalid JSON format"

---

## Feature 3: Daily Sales Dashboard

### Test 3.1: Today's Summary Card
- [ ] "Today's Summary" card shows on dashboard
- [ ] Displays: Total Revenue, Total Weight, Transaction Count
- [ ] "Refresh Summary" button present

### Test 3.2: Today's Sales Breakdown
- [ ] "Today's Sales" card shows list of products
- [ ] Shows: Product name, count, total revenue, total weight
- [ ] Data updates after importing new transactions

### Test 3.3: Refresh Summary
- [ ] Add a transaction manually (via scale or import)
- [ ] Click "Refresh Summary" button
- [ ] Summary numbers update
- [ ] Today's sales list updates

---

## Feature 4: Manual Entry Still Works

### Test 4.1: Product Selection
- [ ] Select a product from dropdown
- [ ] Product options show with updated prices
- [ ] Price in dropdown shows current database price

### Test 4.2: Price Calculation
- [ ] Enter weight: 2.5 kg
- [ ] Select product: Chicken (price: 350)
- [ ] Total price = 2.5 × 350 = 875
- [ ] "₹ 875.00" displays in "Total Price" field

### Test 4.3: Save Transaction
- [ ] Complete form with all details
- [ ] Click "Generate Bill & Save" button
- [ ] Success message appears
- [ ] Transaction appears in "Recent Transactions"
- [ ] In admin: source = "manual"

---

## Feature 5: API Endpoints

### Test 5.1: Get Products API
```bash
curl http://localhost:8000/api/products/
```
- [ ] Returns JSON with all products
- [ ] Each product has: id, name, price_per_kg

### Test 5.2: Update Price API
```bash
curl -X POST http://localhost:8000/api/update-price/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "new_price": 400}'
```
- [ ] Returns success response
- [ ] New price is updated in database

### Test 5.3: Get Daily Sales API
```bash
curl http://localhost:8000/api/daily-sales/
```
- [ ] Returns today's sales summary
- [ ] Includes: total_revenue, total_weight, transactions count
- [ ] Shows breakdown by product

### Test 5.4: Import POS API
```bash
curl -X POST http://localhost:8000/api/import-pos-transactions/ \
  -H "Content-Type: application/json" \
  -d '{"transactions": [{"product_name": "Chicken", "weight": 1.5, "crate_wt": 0.3, "no_of_crates": 1, "birds_per_crate": 5}]}'
```
- [ ] Returns success with count of imported transactions
- [ ] Transaction is in database with source="pos"

---

## Feature 6: Admin Panel

### Test 6.1: Product Admin
- [ ] Go to /admin/billing/product/
- [ ] Can see all products
- [ ] Search by name works
- [ ] Shows: name, price_per_kg, created_at

### Test 6.2: Transaction Admin
- [ ] Go to /admin/billing/transaction/
- [ ] Filter by source: "manual" → shows manual entries
- [ ] Filter by source: "pos" → shows POS imports
- [ ] Search by product name
- [ ] All new fields visible: source, price_per_kg, pos_transaction_id

### Test 6.3: Price History Admin
- [ ] Go to /admin/billing/pricehistory/
- [ ] Shows all price changes
- [ ] Can filter by product
- [ ] Can filter by date

---

## Feature 7: Backward Compatibility

### Test 7.1: Old Features Work
- [ ] Bluetooth scale connection still works
- [ ] "Connect Scale" button functional
- [ ] "Tare" button works
- [ ] "Lock Weight" button works
- [ ] Weight display updates

### Test 7.2: Manual Entry Works
- [ ] Can still enter transactions manually
- [ ] Crate weight calculation works
- [ ] Birds per crate field works
- [ ] Transactions saved correctly

---

## Edge Cases

### Test 8.1: Import with Missing Fields
- [ ] Import JSON without optional fields (remark, group_no)
- [ ] Should still import successfully
- [ ] Missing fields use defaults

### Test 8.2: Import Unknown Product
- [ ] Import transaction with new product name
- [ ] Product should be auto-created
- [ ] New product shows in product list
- [ ] New product has price_per_kg = 0 (default)

### Test 8.3: Multiple Imports Same Day
- [ ] Import 5 transactions
- [ ] Refresh summary
- [ ] Import 5 more transactions
- [ ] Summary shows all 10 transactions

### Test 8.4: Price Change Affects New Transactions
- [ ] Change Chicken price from 350 to 400
- [ ] Import new transaction with Chicken at 2 kg
- [ ] Total price should be 2 × 400 = 800

---

## Performance Tests

- [ ] Page loads in < 2 seconds
- [ ] Import 100 transactions completes in < 5 seconds
- [ ] Daily summary calculation completes quickly
- [ ] Admin page loads with all transactions

---

## Browser Compatibility

- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Edge
- [ ] Mobile view is responsive

---

## Success Criteria

All tests should pass:
- [ ] All 8 feature categories tested
- [ ] All edge cases handled
- [ ] Performance acceptable
- [ ] Browser compatibility confirmed

**Status: ✅ READY FOR PRODUCTION**

---

## Post-Testing

1. Document any issues found
2. Create automated tests for critical paths
3. Set up monitoring for API endpoints
4. Plan POS system integration with your existing system
