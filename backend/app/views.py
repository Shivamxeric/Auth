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
