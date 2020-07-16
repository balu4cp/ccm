from django.conf.urls import url
from hub.views.apis import api_usermanagement

urlpatterns = [

	# url(r'^api/ffadmin/users/roles/get$', usermanagement.RolesGetAPI.as_view()),
	url(r'^api/hub/user/create$', api_usermanagement.HubUserCreateAPI.as_view()),
	# url(r'^api/username/validate$', usermanagement.UsernameValidateAPI.as_view()),	
	url(r'^api/hub/users/list$', api_usermanagement.HubUserListAPI.as_view()),	
	url(r'^api/hub/user/detail$', api_usermanagement.HubUserDetailsAPI.as_view()),	
	url(r'^api/hub/user/password/reset$', api_usermanagement.HubUserResetPasswordAPI.as_view()),	
	url(r'^api/hub/user/resend/email$', api_usermanagement.HubUserResendEmailAPI.as_view()),	
	url(r'^api/hub/user/status/toggle$', api_usermanagement.HubUserStatusChangeAPI.as_view()),	
	url(r'^api/hub/user/update$', api_usermanagement.HubUserUpdateAPI.as_view()),

]
