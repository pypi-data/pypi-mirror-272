# montelo.client.DatapointApi

All URIs are relative to *http://localhost:3002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**datapoint_controller_add_to_dataset_by_slug**](DatapointApi.md#datapoint_controller_add_to_dataset_by_slug) | **POST** /dataset/{datasetSlug}/datapoint | 
[**datapoint_controller_batch_add_to_dataset_by_slug**](DatapointApi.md#datapoint_controller_batch_add_to_dataset_by_slug) | **POST** /dataset/{datasetSlug}/datapoint/batch | 


# **datapoint_controller_add_to_dataset_by_slug**
> DatapointDto datapoint_controller_add_to_dataset_by_slug(dataset_slug, add_to_dataset_input)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.add_to_dataset_input import AddToDatasetInput
from montelo.client.models.datapoint_dto import DatapointDto
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
    api_instance = montelo.client.DatapointApi(api_client)
    dataset_slug = 'dataset_slug_example' # str | 
    add_to_dataset_input = montelo.client.AddToDatasetInput() # AddToDatasetInput | 

    try:
        api_response = api_instance.datapoint_controller_add_to_dataset_by_slug(dataset_slug, add_to_dataset_input)
        print("The response of DatapointApi->datapoint_controller_add_to_dataset_by_slug:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatapointApi->datapoint_controller_add_to_dataset_by_slug: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_slug** | **str**|  | 
 **add_to_dataset_input** | [**AddToDatasetInput**](AddToDatasetInput.md)|  | 

### Return type

[**DatapointDto**](DatapointDto.md)

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

# **datapoint_controller_batch_add_to_dataset_by_slug**
> datapoint_controller_batch_add_to_dataset_by_slug(dataset_slug, batch_add_to_dataset_input)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.batch_add_to_dataset_input import BatchAddToDatasetInput
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
    api_instance = montelo.client.DatapointApi(api_client)
    dataset_slug = 'dataset_slug_example' # str | 
    batch_add_to_dataset_input = montelo.client.BatchAddToDatasetInput() # BatchAddToDatasetInput | 

    try:
        api_instance.datapoint_controller_batch_add_to_dataset_by_slug(dataset_slug, batch_add_to_dataset_input)
    except Exception as e:
        print("Exception when calling DatapointApi->datapoint_controller_batch_add_to_dataset_by_slug: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_slug** | **str**|  | 
 **batch_add_to_dataset_input** | [**BatchAddToDatasetInput**](BatchAddToDatasetInput.md)|  | 

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

