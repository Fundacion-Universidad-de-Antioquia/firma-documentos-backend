import json
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from api.base.users.serializers import UserSerializer
from api.base.users.models import User

# Implements user login view and logout view with oauth2 returning token and refresh token
@api_view(http_method_names=['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    '''
    Login
    '''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print("Username: " + username)
        print("Password: " + password)
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                # Login user
                login(request, user)
                token = ''
                time_threshold = timezone.now()
                token_obj = AccessToken.objects.filter(user=user, expires__gt=time_threshold)
                if token_obj:
                    token = token_obj[0].token
                else:
                    # When the user is not active
                    if not Application.objects.filter(user=1).exists():
                        Application.objects.create(user_id=1, authorization_grant_type='password', client_type='confidential')
                    app_obj = Application.objects.filter(user=1)
                    if app_obj:
                        client_id = app_obj[0].client_id
                        client_secret = app_obj[0].client_secret
                        url = 'http://' + request.get_host() + '/o/token/'
                        data_dict = {
                            'grant_type': 'password',
                            'username': 'username',
                            'password': password,
                            'client_id': client_id,
                            'client_secret': client_secret
                        }
                        aa = request.post(url, data=data_dict)
                        data = json.loads(aa.text)
                        token = data.get('access_token', '')
                
                request.session['token'] = token
                return HttpResponseRedirect(reverse('index'))
            
            return Response({"error": "User not active"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "Invalid HTTP method"}, status=status.HTTP_400_BAD_REQUEST)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]    
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TokenRefresh(APIView):
    def post(self, request, format=None):
        data = request.data
        user_id = data['user_id']
        client_id = data['client_id']
        client_secret = data['client_secret']

        token_obj = RefreshToken.objects.filter(user_id=user_id).order_by('-id')
        refresh_token = ''
        if token_obj:
            refresh_token = token_obj[0].token
        
        url = 'http://' + request.get_host() + '/o/token/'
        data_dict = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
        }

        aa = request.post(url, data=data_dict)
        data = json.loads(aa.text)

        return Response(data, status=status.HTTP_201_CREATED)