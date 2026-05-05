from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dataDB import users_col
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from bson import ObjectId   
from django.shortcuts import render


def register(request):
    return render(request, 'accounts/reg.html')

def login(request):
    return render(request, 'accounts/log.html')

@api_view(['POST'])
def register_user(request):
    """Register a new user, employee, or admin."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        
        # Check if username exists
        if users_col.find_one({"username": data['username']}):
            return Response({"error": "Username already exists"}, status=400)
        
        # Hash the password before saving
        data['password'] = make_password(data['password'])
        
        result = users_col.insert_one(data)
        return Response({"msg": "User created", "id": str(result.inserted_id)}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    """Simple login to verify credentials and return role."""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = users_col.find_one({"username": username})
    
    if user and check_password(password, user['password']):
        return Response({
            "msg": "Login successful",
            "username": user['username'],
            "role": user['role'], # Frontend uses this to show/hide buttons
            "id": str(user['_id'])
        })
    return Response({"error": "Invalid credentials"}, status=401)

@api_view(['GET'])
def get_all_users(request):
    """Admin only: View all accounts."""
    # In a real app, you'd check the requester's role here
    users = list(users_col.find({}, {"password": 0})) # Exclude passwords
    for u in users: u['_id'] = str(u['_id']) # ObjectId is not JSON serializable, convert to string    
    return Response(users)

