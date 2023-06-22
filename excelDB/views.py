from django.shortcuts import render
from .excel_db import ExcelDB

# Create your views here.
def excel(request):
    excel_db = ExcelDB()

    # 엑셀에서 데이터 읽기
    records = excel_db.read_data()
    context = {'records': records}
    return render(request, 'excelDB/excel.html', context)