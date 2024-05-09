# montelo.client.HealthApi

All URIs are relative to *http://localhost:3002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**health_controller_check**](HealthApi.md#health_controller_check) | **GET** /health | 


# **health_controller_check**
> HealthControllerCheck200Response health_controller_check()



### Example


```python
import montelo.client
from montelo.client.models.health_controller_check200_response import HealthControllerCheck200Response
from montelo.client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:3002
# See configuration.py for a list of all supported configuration parameters.
configuration = montelo.client.Configuration(
    host = "http://localhost:3002"
)


# Enter a context with an instance of the API client
with montelo.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = montelo.client.HealthApi(api_client)

    try:
        api_response = api_instance.health_controller_check()
        print("The response of HealthApi->health_controller_check:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling HealthApi->health_controller_check: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**HealthControllerCheck200Response**](HealthControllerCheck200Response.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Health Check is successful |  -  |
**503** | The Health Check is not successful |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

