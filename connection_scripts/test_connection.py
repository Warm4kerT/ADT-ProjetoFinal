from pages.models import Router
from netmiko import ConnectHandler


def run(*args):
    routers = Router.objects.values_list('ip')

    print(routers)
