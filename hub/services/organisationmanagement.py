import sys
import traceback
import os
import string
import random
from django.db import transaction
from django.core.exceptions import ValidationError
from typing import Iterable, List, Dict
from django.contrib.auth import get_user_model
from accounts.models import Role,UserProfile,UserRegistrationCode,RolePermission
from django.contrib.auth.models import User 
from django.core.mail import EmailMessage
from common.emailer.emailservice import dispactch_email
from django.db.models import Q
from ffadmin.models import HUB,CountryState,Franchisee,FranchiseeContact
from django.contrib.gis.geos import Point 
from accounts.services.usermanagement import create_new_user,create_userregistration_code,create_userprofile,update_user,create_userrole,create_user_permission
from accounts.services.emailer import send_franchisee_activation_email
from ffadmin.services.franchisee import get_hubs,get_states,get_districts,get_pincodes,create_franchisee,add_franchisee_contact,get_franchisee_contacts,update_franchisee_contact,franchisee_status_change,get_franchisee_details,resend_activation_email,update_franchisee_object
from common import utility


def get_hub_details(logged_user):
    try:
        user_profile=UserProfile.userprofiles.get(user=logged_user,user_type='Hub')
        hub_details=HUB.hubs.filter(id=user_profile.user_type_id).values('id','name','state','district','regions')
        return hub_details[0]
    except Exception as e:
        utility.log_save('Service-Hub Basic Info Get', e, logged_user.username, 'ERROR')
        raise ValidationError(e)     


def get_hub_francisees_list(list_size:int,logged_user,search_term: str=None):
    try:
        user_profile=UserProfile.userprofiles.get(user=logged_user,user_type='Hub')
        hub=HUB.hubs.get(id=user_profile.user_type_id)
        qry=Q(hub=hub)
        if search_term !=None:
            qry=qry&Q(Q(name__icontains=search_term)|Q(admin_name__icontains=search_term)|Q(admin_phone__icontains=search_term)|Q(state__icontains=search_term)|Q(district__icontains=search_term)|Q(region__icontains=search_term))
        francisees=Franchisee.franchisees.filter(qry).values('id','name','admin_name','admin_phone','state','district','region','uid')
        return francisees.order_by('-id')
    except Exception as e:
        utility.log_save('Service-Hub Franchisee List Get', e, logged_user.username, 'ERROR')
        raise ValidationError(e)   
