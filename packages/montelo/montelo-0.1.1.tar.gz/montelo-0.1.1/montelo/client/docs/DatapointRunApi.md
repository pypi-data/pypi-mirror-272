# montelo.client.DatapointRunApi

All URIs are relative to *http://localhost:3002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**datapoint_run_controller_create_datapoint_run**](DatapointRunApi.md#datapoint_run_controller_create_datapoint_run) | **POST** /datapoint-run | 
[**datapoint_run_controller_update_datapoint_run**](DatapointRunApi.md#datapoint_run_controller_update_datapoint_run) | **PATCH** /datapoint-run | 


# **datapoint_run_controller_create_datapoint_run**
> DatapointRunDto datapoint_run_controller_create_datapoint_run(create_datapoint_run_input)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.create_datapoint_run_input import CreateDatapointRunInput
from montelo.client.models.datapoint_run_dto import DatapointRunDto
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
    api_instance = montelo.client.DatapointRunApi(api_client)
    create_datapoint_run_input = montelo.client.CreateDatapointRunInput() # CreateDatapointRunInput | 

    try:
        api_response = api_instance.datapoint_run_controller_create_datapoint_run(create_datapoint_run_input)
        print("The response of DatapointRunApi->datapoint_run_controller_create_datapoint_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatapointRunApi->datapoint_run_controller_create_datapoint_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_datapoint_run_input** | [**CreateDatapointRunInput**](CreateDatapointRunInput.md)|  | 

### Return type

[**DatapointRunDto**](DatapointRunDto.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datapoint_run_controller_update_datapoint_run**
> EventQueuedDto datapoint_run_controller_update_datapoint_run(update_datapoint_run_input)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.event_queued_dto import EventQueuedDto
from montelo.client.models.update_datapoint_run_input import UpdateDatapointRunInput
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
    api_instance = montelo.client.DatapointRunApi(api_client)
    update_datapoint_run_input = montelo.client.UpdateDatapointRunInput() # UpdateDatapointRunInput | 

    try:
        api_response = api_instance.datapoint_run_controller_update_datapoint_run(update_datapoint_run_input)
        print("The response of DatapointRunApi->datapoint_run_controller_update_datapoint_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatapointRunApi->datapoint_run_controller_update_datapoint_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_datapoint_run_input** | [**UpdateDatapointRunInput**](UpdateDatapointRunInput.md)|  | 

### Return type

[**EventQueuedDto**](EventQueuedDto.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

