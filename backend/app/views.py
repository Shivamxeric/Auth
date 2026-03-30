from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Auth
import json

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from django.contrib.auth.hashers import make_password, check_password


# ================= REGISTER =================
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return JsonResponse({
                    "status": "failed",
                    "message": "All fields are required"
                })

            if Auth.objects.filter(email=email).exists():
                return JsonResponse({
                    "status": "failed",
                    "message": "Email already exists"
                })

            if Auth.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": "failed",
                    "message": "Username already exists"
                })

            Auth.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )

            return JsonResponse({
                "status": "success",
                "message": "User registered successfully"
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })

    return JsonResponse({
        "status": "failed",
        "message": "Invalid request"
    })


# ================= LOGIN =================
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({
                    "status": "failed",
                    "message": "All fields are required"
                })

            try:
                user = Auth.objects.get(email=email)

                if not check_password(password, user.password):
                    return JsonResponse({
                        "status": "failed",
                        "message": "Invalid credentials"
                    })

                refresh = RefreshToken.for_user(user)

                return JsonResponse({
                    "status": "success",
                    "message": "Login successful",
                    "token": str(refresh.access_token)
                })

            except Auth.DoesNotExist:
                return JsonResponse({
                    "status": "failed",
                    "message": "Invalid credentials"
                })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })

    return JsonResponse({
        "status": "failed",
        "message": "Invalid request"
    })


# ================= LOGOUT =================
@csrf_exempt
def logout(request):
    return JsonResponse({
        "status": "success",
        "message": "Logout successful (delete token from frontend)"
    })


# ================= HOME (PROTECTED) =================
@csrf_exempt
def home(request):
    auth = JWTAuthentication()

    try:
        user_auth = auth.authenticate(request)

        if user_auth is None:
            return JsonResponse({
                "status": "failed",
                "message": "Authentication required"
            })

        user, token = user_auth

        return JsonResponse({
            "status": "success",
            "message": f"Welcome {user.username} 🎉"
        })

    except InvalidToken:
        return JsonResponse({
            "status": "failed",
            "message": "Invalid token"
        })
