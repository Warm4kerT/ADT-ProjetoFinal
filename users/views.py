from django.shortcuts import render

# Create your views here.

def home(request,*args, **kwargs):
    print(args, kwargs)
    print(request.user)

    return render(request, "users/hello.html")
