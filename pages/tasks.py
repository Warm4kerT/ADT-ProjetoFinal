from audioop import reverse
from background_task import background
from django.contrib.auth.models import User
from .models import Deployment, Router, Script
from netmiko import ConnectHandler, SSHDetect
from datetime import datetime
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

@background()
def send_to_router(dp_id):
    dp = Deployment.objects.get(id=dp_id)
    dp_router = dp.router
    router_info = {
        'device_type': 'autodetect',
        'ip': str(dp_router.ip),
        'username': dp_router.username,
        'password': dp_router.password,
        'port': dp_router.porta,
    }

    guesser = SSHDetect(**router_info)
    best_match = guesser.autodetect()
    router_info['device_type']=best_match
    net_connect = ConnectHandler(**router_info)
    net_connect.enable()

    file_path = os.path.join(BASE_DIR, 'uploads/' + str(dp.update.file))
    instruction = open(file_path, 'r')
    lines = instruction.readlines()
    output = net_connect.send_config_set(lines)
    instruction.close()
    
    log_path = os.path.join(BASE_DIR, 'uploads/output/' + str(dp_router.name))
    log = open(log_path,'a')  
    log.write('\n' + str(datetime.now()) + '\n')
    log.write(output)
    log.close()
    
    dp.success = True
    dp.logFile = log_path
    dp.save()

@background
def check_available_space(router_id):
    router = Router.objects.get(id=router_id)
    router_info = {
        'device_type': 'autodetect',
        'ip': str(router.ip),
        'username': router.username,
        'password': router.password,
        'port': router.porta,
    }

    guesser = SSHDetect(**router_info)
    best_match = guesser.autodetect()
    router_info['device_type']=best_match
    net_connect = ConnectHandler(**router_info)
    net_connect.enable()

    response = net_connect.send_command("du -h | tail -1")
    
    if 'K' in response:
        number = response.split('K')
        number = int(number[0])
    if 'M' in response:
        number = response.split('M')
        number = int(number[0])*1024
    if 'G' in response:
        number = response.split('G')
        number = int(number[0])*1024*1024
    
    router.available_space = number
    router.save()

@background
def file_size(script_id):
    script = Script.objects.get(id=script_id)
    path = os.path.join(BASE_DIR, 'uploads/' + str(script.file))
    script.size = os.path.getsize(path)
    script.save()