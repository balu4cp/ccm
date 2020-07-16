from django.conf.urls import url
from hub.views.apis import api_producer

urlpatterns = [

	url(r'^api/hub/producers/list$', api_producer.HubProducerListAPI.as_view()),
	url(r'^api/hub/producer/detail$', api_producer.HubProducerDetailsGetAPI.as_view()),
	url(r'^api/hub/producer/sku/list$', api_producer.HubProducerSKUListGetAPI.as_view()),	
	url(r'^api/hub/producer/sku/detail$', api_producer.HubProducerSKUDetailGetAPI.as_view()),	
	url(r'^api/hub/producer/sku/prediction/list$', api_producer.HubPredictedStockListtGetAPI.as_view()),	
    url(r'^api/producer/sku/procurements/list/get', api_producer.HubProducerSKUProcurementListAPI.as_view()),

    url(r'^api/producer/videos/list/get', api_producer.HubProducerVideoListGetAPI.as_view()),
    url(r'^api/producer/images/list/get', api_producer.HubProducerImageListGetAPI.as_view()),

]
