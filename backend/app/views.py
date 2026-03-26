from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Auth
import json


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
                password=password
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
                user = Auth.objects.get(email=email, password=password)

                # Create session
                request.session['user'] = email

                return JsonResponse({
                    "status": "success",
                    "message": "Login successful"
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
    request.session.flush()

    return JsonResponse({
        "status": "success",
        "message": "Logged out successfully"
    })


# ================= HOME (PROTECTED) =================
@csrf_exempt
def home(request):
    user = request.session.get('user')

    if not user:
        return JsonResponse({
            "status": "failed",
            "message": "Unauthorized"
        })

    return JsonResponse({
        "status": "success",
        "message": f"Welcome {user}"
    })