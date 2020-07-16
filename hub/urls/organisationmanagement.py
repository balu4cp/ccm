from django.conf.urls import url
from hub.views.apis import api_organisationmanagement
urlpatterns = [

	# url(r'^api/ffadmin/users/roles/get$', usermanagement.RolesGetAPI.as_view()),
	url(r'^api/hub/basicdetails/get$', api_organisationmanagement.HubBasicInfoGetAPI.as_view()),
	url(r'^api/hub/franchisee/create$', api_organisationmanagement.HubFranchiseeCreateAPI.as_view()),
	url(r'^api/hub/franchisee/list$', api_organisationmanagement.HubFranchiseeListAPI.as_view()),
	url(r'^api/hub/franchisee/detail$', api_organisationmanagement.HubFranchiseeDetailsAPI.as_view()),
	url(r'^api/hub/franchisee/update$', api_organisationmanagement.HubFranchiseeUpdateAPI.as_view()),
	url(r'^api/hub/franchisee/contacts/get$', api_organisationmanagement.HubFracchiseeContactListAPI.as_view()),
	url(r'^api/hub/franchisee/contacts/create$', api_organisationmanagement.HubFracchiseeContactCreateAPI.as_view()),
	url(r'^api/hub/franchisee/contacts/update$', api_organisationmanagement.HubFracchiseeContactUpdateAPI.as_view()),
	url(r'^api/hub/franchisee/status/toggle$', api_organisationmanagement.HubFranchiseeStatusChangeAPI.as_view()),
	url(r'^api/hub/franchisee/email/resend$', api_organisationmanagement.HubFranchiseerResendEmailAPI.as_view()),



]
