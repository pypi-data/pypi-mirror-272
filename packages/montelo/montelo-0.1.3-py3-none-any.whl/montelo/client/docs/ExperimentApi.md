# montelo.client.ExperimentApi

All URIs are relative to *http://localhost:3002*

Method | HTTP request | Description
------------- | ------------- | -------------
[**experiment_controller_create**](ExperimentApi.md#experiment_controller_create) | **POST** /dataset/{datasetSlug}/experiment | 
[**experiment_controller_get_paginated_datapoints_for_experiment**](ExperimentApi.md#experiment_controller_get_paginated_datapoints_for_experiment) | **GET** /experiment/{experimentId}/datapoints | 


# **experiment_controller_create**
> ExperimentDto experiment_controller_create(dataset_slug, create_experiment_input)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.create_experiment_input import CreateExperimentInput
from montelo.client.models.experiment_dto import ExperimentDto
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
    api_instance = montelo.client.ExperimentApi(api_client)
    dataset_slug = 'dataset_slug_example' # str | 
    create_experiment_input = montelo.client.CreateExperimentInput() # CreateExperimentInput | 

    try:
        api_response = api_instance.experiment_controller_create(dataset_slug, create_experiment_input)
        print("The response of ExperimentApi->experiment_controller_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentApi->experiment_controller_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_slug** | **str**|  | 
 **create_experiment_input** | [**CreateExperimentInput**](CreateExperimentInput.md)|  | 

### Return type

[**ExperimentDto**](ExperimentDto.md)

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

# **experiment_controller_get_paginated_datapoints_for_experiment**
> PaginatedExperimentWithDatapointsDto experiment_controller_get_paginated_datapoints_for_experiment(experiment_id, take=take, skip=skip)



### Example

* Bearer (JWT) Authentication (bearer):

```python
import montelo.client
from montelo.client.models.paginated_experiment_with_datapoints_dto import PaginatedExperimentWithDatapointsDto
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
    api_instance = montelo.client.ExperimentApi(api_client)
    experiment_id = 'experiment_id_example' # str | 
    take = 'take_example' # str |  (optional)
    skip = 'skip_example' # str |  (optional)

    try:
        api_response = api_instance.experiment_controller_get_paginated_datapoints_for_experiment(experiment_id, take=take, skip=skip)
        print("The response of ExperimentApi->experiment_controller_get_paginated_datapoints_for_experiment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExperimentApi->experiment_controller_get_paginated_datapoints_for_experiment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **experiment_id** | **str**|  | 
 **take** | **str**|  | [optional] 
 **skip** | **str**|  | [optional] 

### Return type

[**PaginatedExperimentWithDatapointsDto**](PaginatedExperimentWithDatapointsDto.md)

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

