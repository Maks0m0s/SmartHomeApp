from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import FormParser, MultiPartParser
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from rest_framework.response import Response
from main.forms import LoginForm, RegisterForm
from main.services.auth_service import register as register_service, update_account, delete_account
from rest_framework.decorators import action
from django.conf import settings


class AuthViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get', 'post'], url_path='login')
    def login(self, request):
        form_not_valid = False
        form = LoginForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                user = authenticate(
                    request,
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                if user:
                    login(request, user)

                    response = redirect('home')
                    return response
                else:
                    form.add_error(None, 'Invalid credentials')
            form_not_valid = True

        return Response({'form': form, 'form_not_valid': form_not_valid}, template_name='main/login.html')


    @action(detail=False, methods=['get', 'post'], url_path='register')
    def register(self, request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = register_service(form.cleaned_data)
                login(request, user)
                return redirect('home')
        else:
            form = RegisterForm()
        return Response({'form': form}, template_name='main/register.html')

    @action(detail=False, methods=['get'], url_path='logout')
    def logout(self, request):
        response = redirect('home')
        logout(request)
        return response

    @action(detail=False, methods=['post'], url_path='delete')
    def delete(self, request):
        response = redirect('home')
        delete_account(request)
        return response