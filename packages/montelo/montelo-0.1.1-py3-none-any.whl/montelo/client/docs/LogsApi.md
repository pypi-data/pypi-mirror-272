# montelo.client.LogsApi

All URIs are relative to *http://localhost:3002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**logs_controller_create_log**](LogsApi.md#logs_controller_create_log) | **POST** /logs | 
[**logs_controller_end_log**](LogsApi.md#logs_controller_end_log) | **PATCH** /logs/{logId}/end | 


# **logs_controller_create_log**
> logs_controller_create_log(create_log_input)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.create_log_input import CreateLogInput
from montelo.client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:3002
# See configuration.py for a list of all supported configuration parameters.
configuration = montelo.client.Configuration(
    host = "http://localhost:3002"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearer
configuration = montelo.client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with montelo.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = montelo.client.LogsApi(api_client)
    create_log_input = montelo.client.CreateLogInput() # CreateLogInput | 

    try:
        api_instance.logs_controller_create_log(create_log_input)
    except Exception as e:
        print("Exception when calling LogsApi->logs_controller_create_log: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_log_input** | [**CreateLogInput**](CreateLogInput.md)|  | 

### Return type

void (empty response body)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logs_controller_end_log**
> logs_controller_end_log(log_id, end_log_input)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.end_log_input import EndLogInput
from montelo.client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:3002
# See configuration.py for a list of all supported configuration parameters.
configuration = montelo.client.Configuration(
    host = "http://localhost:3002"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): bearer
configuration = montelo.client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with montelo.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = montelo.client.LogsApi(api_client)
    log_id = 'log_id_example' # str | 
    end_log_input = montelo.client.EndLogInput() # EndLogInput | 

    try:
        api_instance.logs_controller_end_log(log_id, end_log_input)
    except Exception as e:
        print("Exception when calling LogsApi->logs_controller_end_log: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **log_id** | **str**|  | 
 **end_log_input** | [**EndLogInput**](EndLogInput.md)|  | 

### Return type

void (empty response body)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

