import datetime
from .models import IpAddress


def get_ip_address(req):
    x_forwarded_for = req.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = req.META.get("REMOTE_ADDR")
    return ip


def SaveIpAddressMiddleware(get_response):
    """
    Save the Ip address if does not exist
    """

    def process_request(request):
        ip = get_ip_address(request)
        IpAddress.objects.get_or_create(ip_address=ip)

        response = get_response(request)
        return response

    return process_request
