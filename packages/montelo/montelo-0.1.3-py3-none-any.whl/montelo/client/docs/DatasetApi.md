# montelo.client.DatasetApi

All URIs are relative to *http://localhost:3002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dataset_controller_create**](DatasetApi.md#dataset_controller_create) | **POST** /dataset | 
[**dataset_controller_delete**](DatasetApi.md#dataset_controller_delete) | **DELETE** /dataset/{datasetId} | 
[**dataset_controller_get_all_datasets**](DatasetApi.md#dataset_controller_get_all_datasets) | **GET** /dataset | 
[**dataset_controller_get_full_dataset**](DatasetApi.md#dataset_controller_get_full_dataset) | **GET** /dataset/{datasetId} | 


# **dataset_controller_create**
> DatasetDto dataset_controller_create(create_dataset_input)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.create_dataset_input import CreateDatasetInput
from montelo.client.models.dataset_dto import DatasetDto
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
    api_instance = montelo.client.DatasetApi(api_client)
    create_dataset_input = montelo.client.CreateDatasetInput() # CreateDatasetInput | 

    try:
        api_response = api_instance.dataset_controller_create(create_dataset_input)
        print("The response of DatasetApi->dataset_controller_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->dataset_controller_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_dataset_input** | [**CreateDatasetInput**](CreateDatasetInput.md)|  | 

### Return type

[**DatasetDto**](DatasetDto.md)

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

# **dataset_controller_delete**
> DeleteSuccessDto dataset_controller_delete(dataset_id)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.delete_success_dto import DeleteSuccessDto
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
    api_instance = montelo.client.DatasetApi(api_client)
    dataset_id = 'dataset_id_example' # str | 

    try:
        api_response = api_instance.dataset_controller_delete(dataset_id)
        print("The response of DatasetApi->dataset_controller_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->dataset_controller_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **str**|  | 

### Return type

[**DeleteSuccessDto**](DeleteSuccessDto.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_get_all_datasets**
> List[DatasetDto] dataset_controller_get_all_datasets()



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.dataset_dto import DatasetDto
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
    api_instance = montelo.client.DatasetApi(api_client)

    try:
        api_response = api_instance.dataset_controller_get_all_datasets()
        print("The response of DatasetApi->dataset_controller_get_all_datasets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->dataset_controller_get_all_datasets: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[DatasetDto]**](DatasetDto.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dataset_controller_get_full_dataset**
> FullDatasetWithCountDto dataset_controller_get_full_dataset(dataset_id, take=take, skip=skip)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.full_dataset_with_count_dto import FullDatasetWithCountDto
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
    api_instance = montelo.client.DatasetApi(api_client)
    dataset_id = 'dataset_id_example' # str | 
    take = 'take_example' # str | How many traces to get. If undefined returns all. (optional)
    skip = 'skip_example' # str | How many traces to skip. If undefined starts from beginning. (optional)

    try:
        api_response = api_instance.dataset_controller_get_full_dataset(dataset_id, take=take, skip=skip)
        print("The response of DatasetApi->dataset_controller_get_full_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasetApi->dataset_controller_get_full_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **str**|  | 
 **take** | **str**| How many traces to get. If undefined returns all. | [optional] 
 **skip** | **str**| How many traces to skip. If undefined starts from beginning. | [optional] 

### Return type

[**FullDatasetWithCountDto**](FullDatasetWithCountDto.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

