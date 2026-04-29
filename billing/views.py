from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product, Transaction, DailyStock
from django.utils import timezone
from django.db.models import Sum
import json
from datetime import datetime, date

def dashboard(request):
    today = timezone.now().date()
    
    # Get or Create current day's stock entry
    stock, created = DailyStock.objects.get_or_create(
        date=today,
        defaults={'kg_bought': 0, 'cost_price_total': 0, 'sale_price_per_kg': 0}
    )

    # Daily Stats
    transactions_today = Transaction.objects.filter(timestamp__date=today)
    total_kg_sold_today = transactions_today.aggregate(Sum('weight'))['weight__sum'] or 0
    total_revenue_today = transactions_today.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Stock remaining
    stock_remaining = stock.kg_bought - total_kg_sold_today

    # Profit Calculation (Daily)
    # Cost of goods sold = (cost_price_total / kg_bought) * kg_sold
    if stock.kg_bought > 0:
        cost_per_kg = stock.cost_price_total / stock.kg_bought
        cost_of_sold_chicken = cost_per_kg * total_kg_sold_today
        daily_profit = total_revenue_today - cost_of_sold_chicken + stock.manual_profit_adjustment
    else:
        daily_profit = 0

    # Monthly Stats
    first_day_of_month = today.replace(day=1)
    transactions_month = Transaction.objects.filter(timestamp__date__gte=first_day_of_month)
    total_revenue_month = transactions_month.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Calculate Monthly Profit (sum of daily profits)
    stocks_month = DailyStock.objects.filter(date__gte=first_day_of_month)
    monthly_profit = 0
    for s in stocks_month:
        s_transactions = Transaction.objects.filter(timestamp__date=s.date)
        s_sold = s_transactions.aggregate(Sum('weight'))['weight__sum'] or 0
        s_revenue = s_transactions.aggregate(Sum('total_price'))['total_price__sum'] or 0
        if s.kg_bought > 0:
            s_cost_per_kg = s.cost_price_total / s.kg_bought
            s_cost_of_sold = s_cost_per_kg * s_sold
            monthly_profit += (s_revenue - s_cost_of_sold + s.manual_profit_adjustment)
        else:
            monthly_profit += (s_revenue + s.manual_profit_adjustment)

    # 6-Month History Logic
    history = []
    for i in range(6):
        month_date = today.replace(day=1)
        # Handle month subtraction correctly
        month_to_calc = (month_date.month - i - 1) % 12 + 1
        year_to_calc = month_date.year + (month_date.month - i - 1) // 12
        
        target_month_start = date(year_to_calc, month_to_calc, 1)
        if month_to_calc == 12:
            target_month_end = date(year_to_calc + 1, 1, 1)
        else:
            target_month_end = date(year_to_calc, month_to_calc + 1, 1)

        month_stocks = DailyStock.objects.filter(date__gte=target_month_start, date__lt=target_month_end)
        m_profit = 0
        for s in month_stocks:
            s_transactions = Transaction.objects.filter(timestamp__date=s.date)
            s_sold = s_transactions.aggregate(Sum('weight'))['weight__sum'] or 0
            s_revenue = s_transactions.aggregate(Sum('total_price'))['total_price__sum'] or 0
            if s.kg_bought > 0:
                s_cost_per_kg = s.cost_price_total / s.kg_bought
                s_cost_of_sold = s_cost_per_kg * s_sold
                m_profit += (s_revenue - s_cost_of_sold + s.manual_profit_adjustment)
            else:
                m_profit += (s_revenue + s.manual_profit_adjustment)
        
        history.append({
            'month': target_month_start.strftime('%B %Y'),
            'profit': m_profit
        })

    products = Product.objects.all()
    if not products:
        Product.objects.create(name="Chicken")
        products = Product.objects.all()

    context = {
        'stock': stock,
        'total_kg_sold_today': total_kg_sold_today,
        'total_revenue_today': total_revenue_today,
        'stock_remaining': stock_remaining,
        'daily_profit': daily_profit,
        'monthly_profit': monthly_profit,
        'history': history,
        'products': products,
        'transactions': transactions_today.order_by('-timestamp')[:5]
    }
    return render(request, 'billing/dashboard.html', context)

def update_stock(request):
    if request.method == 'POST':
        today = timezone.now().date()
        stock, created = DailyStock.objects.get_or_create(date=today)
        stock.kg_bought = request.POST.get('kg_bought', 0)
        stock.cost_price_total = request.POST.get('cost_price_total', 0)
        stock.sale_price_per_kg = request.POST.get('sale_price_per_kg', 0)
        stock.save()
        return redirect('dashboard')
    return redirect('dashboard')

def save_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            weight = data.get('weight')
            total_price = data.get('total_price')
            price_per_kg = data.get('price_per_kg')

            if not product_id:
                return JsonResponse({'status': 'error', 'message': 'No product selected'}, status=400)

            product = Product.objects.get(id=product_id)
            transaction = Transaction.objects.create(
                product=product,
                weight=weight,
                price_per_kg=price_per_kg,
                total_price=total_price,
                crate_wt=data.get('crate_wt', 0),
                no_of_crates=data.get('no_of_crates', 1),
                birds_per_crate=data.get('birds_per_crate', 0),
                remark=data.get('remark', ''),
                group_no=data.get('group_no', '')
            )
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def report(request):
    transactions = Transaction.objects.all().order_by('-timestamp')
    return render(request, 'billing/report.html', {'transactions': transactions})
