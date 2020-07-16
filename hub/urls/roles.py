from django.urls import path
from hub.views.apis import api_role

urlpatterns = [
    path("api/role/create", api_role.HubRoleCreateView.as_view()),
    path("api/role/list/get", api_role.HubRoleListView.as_view()),
    path("api/role/delete", api_role.HubRoleDeleteView.as_view()),
    path("api/role/details/get", api_role.HubRoleDetailedView.as_view()),
    path("api/role/details/update", api_role.HubRoleUpdateView.as_view()),
    path("api/role/status/change", api_role.HubRoleStatusChangeView.as_view()),  
    path("api/role/permissions/get", api_role.HubPermissionListView.as_view()),
]
