from django.http import QueryDict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q, Sum
from .forms import UserForm, CompanyForm
from .models import UserModel, Company, DataTransferModel, DateTimeModel
from .tasks import generate_users, generate_transfers
from .services import IndexService


class IndexView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, *args, **kwargs):
        self.service = IndexService()
        super(IndexView, self).__init__(*args, **kwargs)

    def get(self, request):
        data = {
            'users_list': self.service.get_user_list(),
            'companies_list': self.service.get_company_list(),
            'transfer_months': DateTimeModel.get_years_months_list(),
            'user_form': UserForm(),
            'company_form': CompanyForm(),
        }
        return render(request, 'app/index.html', data)

    def post(self, request):
        if request.POST.get('data') == 'user':
            form = UserForm(request.POST)
            if form.is_valid():
                obj = form.save()
                return Response({"status": True,
                                 "user": self.service.user_obj_to_json(obj), }, content_type="application/json")
            return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)
        elif request.POST.get('data') == 'company':
            form = CompanyForm(request.POST)
            if form.is_valid():
                obj = form.save()
                return Response({"status": True,
                                 "company": self.service.company_obj_to_json(obj), }, content_type="application/json")
            return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if request.method == 'PATCH':
            data = QueryDict(request.body)
            if data['data'] == 'update_user':
                obj = self.service.update_user(data)
                return Response({"status": True, "user": self.service.user_obj_to_json(obj)})
            elif data['data'] == 'update_company':
                obj = self.service.update_company(data)
                return Response({"status": True, "company": self.service.company_obj_to_json(obj)})

        return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)


class RemoveItem(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        if request.POST.get('data') == 'user':
            obj = UserModel.objects.get(id=request.POST.get('id'))
        elif request.POST.get('data') == 'company':
            obj = Company.objects.get(id=request.POST.get('id'))
        else:
            return Response({'status': False}, content_type="application/json")
        obj.delete()
        return Response({'status': True}, content_type="application/json")


class AbusersView(APIView):

    def post(self, request):
        if request.POST.get('data') == 'date_filter':
            year = request.POST.get('year')
            month = request.POST.get('month')
            transfer_data = DataTransferModel.objects.get_data__by_time(month=month, year=year)

            companies: list = Company.objects.values('id', 'name', 'quota', 'size')
            report: dict = {}  # key - company_id; value - sum of converted bytes
            for company in companies:
                _bytes = transfer_data.filter(company_id=company['id']).aggregate(Sum('transferred_bytes'))
                to_human_bytes = DataTransferModel.objects.humanbytes(_bytes['transferred_bytes__sum'])
                transferred_data = {'transferred_size': to_human_bytes, 'company': company}
                report[company['id']] = transferred_data
            return Response({'status': True, 'transfer_data': self.transfers_obj_to_json(transfer_data),
                             'report_data': report},
                            content_type="application/json")

    def transfers_obj_to_json(self, data):
        result = []
        for transfer_obj in data:
            result.append(self.transfer_obj_to_json(transfer_obj))
        return result

    def transfer_obj_to_json(self, obj):
        data = {
            'id': obj.id,
            'user': obj.user.user,
            'time': obj.time.timestamp,
            'resource': obj.resource.domain,
            'size': obj.size,
            'size_type': obj.size_type
        }
        return data


class AutoGenerate(APIView):

    def post(self, request):
        generate = request.POST.get('data')
        amount = request.POST.get('amount')
        if generate == 'companies':
            pass
        elif generate == 'users':
            generate_users.delay(amount)
        elif generate == 'transfers':
            generate_transfers.delay()
        return Response({'status': True,
                         'message': 'Your task is being processed, Please update the page..'},
                        content_type="application/json")


def custom_handler404(request, exception):
    context = {}
    response = render(request, 'app/error_404.html', context=context)
    response.status_code = 404
    return response


def custom_handler500(request):
    context = {}
    response = render(request, 'app/error_500.html', context=context)
    response.status_code = 500
    return response
