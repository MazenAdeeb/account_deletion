from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import requests
from .utils import login_and_get_token   # <-- correct import


@csrf_exempt
def delete_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return HttpResponse('Email and password are required.', status=400)

        try:
            # Step 1: Login and get token
            token = login_and_get_token(email, password)

            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }

            # Step 2: Get user info to extract ID
            user_info_url = 'https://zahraa.cloider.com/api/accounts/user-info/'
            user_info_response = requests.get(user_info_url, headers=headers)
            user_info_response.raise_for_status()
            user_info = user_info_response.json()

            pk = user_info.get('id')
            if not pk:
                return HttpResponse('User ID not found.', status=400)

            # Step 3: Delete user by ID
            delete_url = f'https://zahraa.cloider.com/api/accounts/delete-account/{pk}/'
            delete_response = requests.delete(delete_url, headers=headers)
            delete_response.raise_for_status()

            return HttpResponse('Account deleted successfully.')

        except requests.RequestException as e:
            return HttpResponse(f'Error processing the request: {e}', status=500)

    return render(request, 'deletion_form.html')
