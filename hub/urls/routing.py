from django.urls import path
from hub.views.apis import api_routing

urlpatterns = [
    path("api/routing/get/list", api_routing.HubRoutingListView.as_view()),
    path("api/routing/list/update/vehicle", api_routing.HubUpdateVehicle.as_view()),
    path("api/routing/list/merge/items", api_routing.HubMergeRoutingItems.as_view()),
    path("api/routing/list/unify/shipping", api_routing.HubUnifyShipping.as_view()),
    path("api/routing/filters/data/get", api_routing.RoutingListFiltersGet.as_view()),
    path("api/routing/item/auto/unmerge", api_routing.HubAutoUnmergeItem.as_view()),
    path("api/routing/item/details/get", api_routing.HubRoutingItemDetailsView.as_view()),
    path("api/routing/item/confirm/vehicle", api_routing.HubConfirmVehicle.as_view()),
    path("api/routing/item/mark/missing", api_routing.HubRoutingMarkMissing.as_view()),
    path("api/routing/item/mark/damaged", api_routing.HubRoutingMarkDamaged.as_view()),
    path("api/routing/item/update", api_routing.HubRoutingUpdateItem.as_view()),
    path("api/routing/item/generate/shipping/label", api_routing.HubRoutingGenerateShippingLabel.as_view()),
    path("api/routing/generate/new/item", api_routing.HubRoutingGenerateNewItem.as_view()),
    path("api/routing/hub/franchisee/list/get", api_routing.RoutingHUBFranchiseeListGet.as_view()),
    path("api/routing/item/update/current/location", api_routing.HubRoutingUpdateCurrentLocation.as_view())
]
