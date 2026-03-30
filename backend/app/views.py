import email

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

            # Validation
            if not username or not email or not password:
                return JsonResponse({
                    "status": "failed",
                    "message": "All fields are required"
                })            

            # Check duplicates
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

            # Create user
            Auth.objects.create(
                username=username,
                email=email,
                password=make_password(password)   # ✅ HASH
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

    return JsonResponse({"message": "Invalid request"})


# ================= LOGIN =================
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            email = data.get('email')
            password = data.get('password')

            # Validation
            if not email or not password:
                return JsonResponse({
                    "status": "failed",
                    "message": "All fields are required"
                })

            try:
                user = Auth.objects.get(email=email)
                if not user.check_password(password):
                    return JsonResponse({
                        "status": "failed",
                        "message": "Invalid credentials"
                    })
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return JsonResponse({
                "status": "success",
                "message": "Login successful",
                "token": access_token
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

    return JsonResponse({"message": "Invalid request"})


# ================= LOGOUT =================
@csrf_exempt
def logout(request):
    return JsonResponse({
        "status": "success",
        "message": "Logout successful (client should delete token)"
    })

# ================= HOME (PROTECTED) =================
from rest_framework_simplejwt.tokens import AccessToken

@csrf_exempt
def home(request):
    try:
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return JsonResponse({
                "status": "failed",
                "message": "No token provided"
            })

        token = auth_header.split(" ")[1]

        decoded = AccessToken(token)

        user_id = decoded['user_id']

        user = Auth.objects.get(id=user_id)

        return JsonResponse({
            "status": "success",
            "message": f"Welcome {user.username} 🎉"
        })

    except Exception as e:
        return JsonResponse({
            "status": "failed",
            "message": "Invalid token"
        })
