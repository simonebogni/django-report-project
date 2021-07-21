from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
from .utils import get_customer_from_id, get_salesman_from_id
import pandas as pd
# Create your views here.

def home_view(request):
    sales_df = None
    positions_df = None
    form = SalesSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        sales_qs = Sale.objects.filter(created_at__date__lte=date_to, created_at__date__gte=date_from)
        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())
            # override customer_id and salesman_id to show the names
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman'}, axis=1, inplace=True)
            positions_data = []
            for sale in sales_qs:
                for position in sale.get_positions():
                    sales_list = position.get_sales()
                    print(sales_list)
                    for pos_sale in sales_list:
                        obj = {
                            'position_id': position.id,
                            'sales_id': pos_sale.id,
                            'product': position.product.name,
                            'quantity': position.quantity,
                            'price': position.price,
                        }
                        positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)

            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
        
    context = {
        'form': form,
        'sales_df': sales_df,
        'positions_df': positions_df
    }
    return render(request, 'sales/home.html', context)

class SaleListView(ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'