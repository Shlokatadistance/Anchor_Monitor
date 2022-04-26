from django.shortcuts import render
from django.http import HttpResponse
from .services import *
from django.views.generic import TemplateView


class anchor_view(TemplateView):
	#template_name = 'viewer.html'
	##def get_anchor_data(self,*args, **kwargs):
	#	context = anchor_data()
	#	return context

	def get(self,request):
		get_anchor_data = anchor_data()
		#print(get_anchor_data['Total Value Locked'])
		message = {
		"Total_Value_locked" : get_anchor_data['Total_Value_locked'],
		"Total_Yield_reserve" : get_anchor_data['Total_Yield_reserve'],
		"Total_Collateral" : get_anchor_data['Total_Collateral'],
		"Total_Deposit" : get_anchor_data['Total_Deposit'],
		}
		return render(request,'viewer.html',message)
class anchor_next_view(TemplateView):
	def get(self,request):
		get_next_data = page_2()
		message = {
		"ANC_Price_UST" : get_next_data['ANC_Price_UST'],
		"ANC_Buyback_72HR_UST" : get_next_data['ANC_Buyback_72HR_UST'],
		"ANC_Buyback_12Month_UST" : get_next_data['ANC_Buyback_12Month_UST'],
		"Deposit_APY" : get_next_data['Deposit_APY'],
		"Total_Borrow" : get_next_data['Total_Borrow'],
		"Borrow_APR" : get_next_data['Borrow_APR'],
		"Bonded_Luna_Price" : get_next_data['Bonded_Luna_Price'],
		"Bonded_Luna_Collateral" : get_next_data['Bonded_Luna_Collateral'],
		"Bonded_Luna_Total_Collateral_Value" : get_next_data['Bonded_Luna_Total_Collateral_Value'],
		"Bonded_Ether_Price" : get_next_data['Bonded_Ether_Price'],
		"Bonded_Ether_Collateral" : get_next_data['Bonded_Ether_Collateral'],
		"Bonded_Ether_Total_Collateral_Value" : get_next_data['Bonded_Ether_Total_Collateral_Value'],
		"USDTDAI_value" : get_next_data['USDTDAI'],
		"LUNAUSDT_value" : get_next_data['LUNAUSDT'],
		"ETHUSDT_value" : get_next_data['ETHUSDT'],
		"BETHETH_value" : get_next_data['BETHETH'],
		"Ratio_Luna" : float(''.join(filter(str.isdigit,get_next_data['Bonded_Luna_Total_Collateral_Value']))) / float(''.join(filter(str.isdigit,get_next_data['Bonded_Luna_Collateral']))),
		"Ratio_Ether" : float(''.join(filter(str.isdigit,get_next_data['Bonded_Ether_Total_Collateral_Value']))) / float(''.join(filter(str.isdigit,get_next_data['Bonded_Ether_Collateral']))),

		}

		return render(request,'next_viewer.html',message)

# Create your views here.
#get_anchor_data['Total Value locked']