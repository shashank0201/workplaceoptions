from django.shortcuts import render
from django.views.generic import TemplateView
import re
import xlrd
from datetime import datetime
from django.http import HttpResponseRedirect

from .models import Person
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class PersonView(TemplateView):
    def get(self, request, *args, **kwargs):
    	return render(request,'home.html')

    def post(self, request, *args, **kwargs):
    	data = request.FILES.get('excel_file')
    	book = xlrd.open_workbook(data.name, file_contents=data.read())
    	first_sheet = book.sheet_by_index(0)
    	total_rows=first_sheet.nrows
    	for i in range(1,first_sheet.nrows):
    		name=first_sheet.row_values(i)[0]
    		email=first_sheet.row_values(i)[1]
    		phone=int(first_sheet.row_values(i)[2])
    		date_tuple = xlrd.xldate_as_tuple(first_sheet.row_values(i)[3], book.datemode)
    		date = datetime(*date_tuple).strftime('%Y-%m-%d')
    		email_validate = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    		# validate the email and phone number
    		if re.search(email_validate,email) and str(phone).isdigit() and len(str(phone))==10:
    			p=Person()
    			p.name=name
    			p.email=email
    			p.phone=phone
    			p.birth_date=date
    			p.save()
    	return HttpResponseRedirect("/person")


class SearchView(TemplateView):
	def get(self, request, *args, **kwargs):
		return HttpResponseRedirect("/person")


	def post(self, request, *args, **kwargs):
		template_name="home.html"
		email=request.POST.get('email')
		person_data=Person.objects.filter(email=email)
		if person_data:
			p_data=[]
			for i in person_data:
				p={}
				p['name'] = i.name
				p['email'] = i.email
				p['phone'] = i.phone
				curr_date = datetime.now().strftime("%Y-%m-%d")
				curr_date = datetime.strptime(curr_date, '%Y-%m-%d')
				birth_date = datetime.strptime(str(i.birth_date), '%Y-%m-%d')
				p['age'] = int(((curr_date-birth_date).days)/365)
				p_data.append(p)
			return render(request,template_name, {"excel_data":p_data})
		else:
			return HttpResponseRedirect("/search")
