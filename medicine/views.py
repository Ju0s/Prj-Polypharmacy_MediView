from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse

def search(request):
    query = request.GET.get('q')
    search_by = request.GET.get('search_by', '제품명')
    results = []

    if query:
        if search_by == '제품명':
            results = 제품.objects.filter(제품명__icontains=query).select_related('업체코드')
        elif search_by == '주성분코드':
            results = 제품.objects.filter(주성분코드__icontains=query).select_related('업체코드')
        elif search_by == '업체명':
            results = 제품.objects.filter(업체코드__업체명__icontains(query)).select_related('업체코드')

    context = {
        'query': query,
        'search_by': search_by,
        'results': results,
    }
    return render(request, 'medicine/search_results.html', context)

def get_contraindications(request, 제품코드):
    제품_instance = 제품.objects.get(제품코드=제품코드)
    contraindications = 제품_금기정보.objects.filter(제품코드=제품코드).select_related('금기코드')
    data = []
    for ci in contraindications:
        detail_info = []
        if ci.금기코드.금기코드 == 3:
            detail_info = list(노인주의상세정보.objects.filter(제품코드=제품코드).values())
        elif ci.금기코드.금기코드 == 4:
            detail_info = list(임부금기상세정보.objects.filter(제품코드=제품코드).values())
        elif ci.금기코드.금기코드 == 5:
            detail_info = list(병용금기상세정보.objects.filter(제품코드=제품코드).values('제품코드', '상대제품코드', '상세정보'))
        elif ci.금기코드.금기코드 == 6:
            detail_info = list(연령별금기상세정보.objects.filter(제품코드=제품코드).values())
        elif ci.금기코드.금기코드 == 7:
            detail_info = list(투여기간상세정보.objects.filter(제품코드=제품코드).values())
        elif ci.금기코드.금기코드 == 8:
            detail_info = list(용량주의상세정보.objects.filter(제품코드=제품코드).values())
        elif ci.금기코드.금기코드 == 9:
            detail_info = list(효능군중복상세정보.objects.filter(제품코드=제품코드).values())
        data.append({
            '제품코드': ci.제품코드.제품코드,
            '제품명': 제품_instance.제품명,
            '금기코드': ci.금기코드.금기코드,
            '금기유형': ci.금기코드.금기유형,
            '상대제품코드': [item['상대제품코드'] for item in detail_info] if ci.금기코드.금기코드 == 5 else None,
            '상세정보': detail_info or [{'상세정보': '상세정보 없음'}],
        })
    return JsonResponse(data, safe=False)