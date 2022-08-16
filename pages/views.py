from tabnanny import check
from django.shortcuts import render, redirect
from .models import Router, Script, Deployment
from .forms import RawRouterForm, RawScriptForm
from .tasks import check_available_space, file_size, send_to_router
from datetime import date, timedelta
from pathlib import Path
from django.http import HttpResponse
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def add_router(request,*args, **kwargs):
    print(args, kwargs)
    print(request.user)

    form = RawRouterForm()
    if request.method == "POST":
        form = RawRouterForm(request.POST)
        
        if form.is_valid():
            router = Router.objects.create(**form.cleaned_data)
            router.save()
            print("Saved new router")
            id = router.id
            check_available_space(id)
            return redirect("/pages/router_db/")

        else:
            print(form.errors)

    context = {
        'form': form
    }

    return render(request, "pages/router_form.html", context)

def router_db(request,*args, **kwargs):
    print(args, kwargs)
    print(request.user)

    context = {
        "list" : Router.objects.all()
    }

    return render(request, "pages/router_db.html", context)

def add_script(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)

    if request.method == "POST":
        form = RawScriptForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_script = Script(**form.cleaned_data)
            file_path = os.path.join(BASE_DIR, 'uploads/scripts/' + form.cleaned_data.get('file').name)
            new_script.size = 0
            new_script.save()
            file_size(new_script.id)
            print("Saved new Script")
            
            routers_update = Router.objects.filter(model=form.cleaned_data.get('compatible_model'))
            for dp_router in routers_update:
                new_dp = Deployment.objects.create(router=dp_router,update=new_script,date=date.today())
                send_to_router(new_dp.id, verbose_name="Deployment", repeat=60, repeat_until=date.today()+timedelta(minutes=60))
                print("New Deployment " + str(new_dp.router.name))
            
            return redirect("/pages/script_db/")

        else:
            print(form.errors)

    else:
        form = RawScriptForm()

    context = {
        'form': form
    }

    return render(request, "pages/script_form.html", context)

def script_db(request,*args, **kwargs):
    print(args, kwargs)
    print(request.user)

    context = {
        "list" :  reversed(Script.objects.all())
    }

    return render(request, "pages/script_db.html", context)

def delete_script(request, script_id):
    print(request.user)

    my_script = Script.objects.get(id=script_id)

    if Deployment.objects.filter(update=my_script).exists():
        dp = Deployment.objects.get(update=my_script)
        dp.delete()

    my_script.delete()

    return redirect('/pages/script_db')

def delete_router(request, router_id):
    print(request.user)

    my_router = Router.objects.get(id=router_id)

    if Deployment.objects.filter(router=my_router).exists():
        dp = Deployment.objects.get(router_id=router_id)
        dp.delete()
    
    my_router.delete()
    #messages.success(request, ('Task has been Deleted!'))
    return redirect('/pages/router_db')

def deployment_db(request,*args, **kwargs):
    print(args, kwargs)
    print(request.user)

    context = {
        "list" :   reversed(Deployment.objects.all())
    }

    return render(request, "pages/deployment_db.html", context)

def show_file(request, dp_id):
    print(request.user)
    dp = Deployment.objects.get(id=dp_id)
    path =  str(dp.logFile)
    file =  open(path, 'r')
    out = file.readlines()
    html=[]
    for line in out:
        html += '<p>' + line + '</p>'

    response = HttpResponse(html)
    return response
