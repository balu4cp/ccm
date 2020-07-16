import sys
import traceback
from datetime import datetime, timedelta
from ffadmin.models import RoutingItem
from django.conf import settings
from django.http import HttpResponseRedirect
from django.db import transaction
from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from common import utility #Vishnupriya
from django.shortcuts import render, redirect #Vishnupriya
User = get_user_model()

class users(View):
    template_name = "hub/hub_users_list.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View Users' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class userCreate(View):
    template_name = "hub/hub_user_create.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-Create Users' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class roleCreate(View):
    template_name = "hub/hub_role_create.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-Create Roles' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class roleDetail(View):
    template_name = "hub/hub_role_detail.html"

    def get(self, request, id):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View Roles' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class roles(View):
    template_name = "hub/roles.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View Roles' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))
            
class userDetail(View):
    template_name = "hub/hub_user_detail.html"

    def get(self, request,id):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View Users' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class HubOrganisationListView(View):
    template_name = "hub/hub_organisations_list.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View Organisation' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class HubFranchiseeCreateView(View):
    template_name = "hub/hub_franchisee_create.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-Create Franchisee' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class HubFranchiseeDetailedView(View):
    template_name = "hub/hub_franchisee_detail.html"

    def get(self, request,id):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View Organisation' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class HubProducerListView(View):
    template_name = "hub/hub_producers_list.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View Producers' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class HubProducerDetailedView(View):
    template_name = "hub/hub_producer_detail.html"

    def get(self, request,id):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View Producers' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class HubSKUDetailedView(View):
    template_name = "hub/hub_sku_detail.html"

    def get(self, request,pid,skuid):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View SKUs' in permissions_list and 'Hub-View Producers' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class HubSKUListDetailedView(View):
    template_name = "hub/hub_sku_list_detail.html"

    def get(self, request,uid):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View SKUs' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))

class HubSKUListView(View):
    template_name = "hub/hub_skus_list.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View SKUs' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))


class HubStockOrganisationListView(View):
    template_name = "hub/hub_organisation_stock_list.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-View SKUs' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))
        

class HubSKUCreateView(View):
    template_name = "hub/hub_sku_create.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        if 'Hub-Create SKU' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))


class HubLogisticsRoutingListView(View):
    template_name = "hub/hub_logistics_routing_list.html"

    def get(self, request):
        permissions_list = utility.getUserPermissions(request.user.id)
        socket_url = f"{request.build_absolute_uri().split('/')[2].split(':')[0]}:9002"
        if 'Hub-View Routing List' in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list, 'socket_url': socket_url})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))


class HubLogisticsRoutingDetailedView(View):
    template_name = "hub/hub_logistics_routing_detail.html"

    def get(self, request, id):
        permissions_list = utility.getUserPermissions(request.user.id)
        if "Hub-View Routing List" in permissions_list:
            return render(request, self.template_name, {'permissions_list': permissions_list})
        else:
            return HttpResponseRedirect(reverse('login_redirect'))


class HubLogisticsRoutingQRCode(View):
    template_name = "hub/hub_logistics_routing_qr_code.html"

    def get(self, request, uid):
        try:
            qr_path = RoutingItem.routingitems.get(uid=uid)
            qr_path = str(qr_path.shipping_qr.path)
            qr_path = f'{settings.MEDIA_URL}{qr_path}'
            return render(request, self.template_name, {'qr_code': qr_path})
        except Exception:
            return render(request, self.template_name, {'error_msg': 'Invalid link'})
