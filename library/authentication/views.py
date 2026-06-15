from django.shortcuts import render, get_object_or_404
from .models import CustomUser

def user_list(request):
    users = CustomUser.objects.all()
    
    return render(request, 'authentication/user_list.html', {'users': users})

def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
  
    return render(request, 'authentication/user_detail.html', {'user': user})