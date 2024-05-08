# HealthControllerCheck200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | [optional] 
**info** | [**Dict[str, HealthControllerCheck200ResponseInfoValue]**](HealthControllerCheck200ResponseInfoValue.md) |  | [optional] 
**error** | [**Dict[str, HealthControllerCheck200ResponseInfoValue]**](HealthControllerCheck200ResponseInfoValue.md) |  | [optional] 
**details** | [**Dict[str, HealthControllerCheck200ResponseInfoValue]**](HealthControllerCheck200ResponseInfoValue.md) |  | [optional] 

## Example

```python
from montelo.client.models.health_controller_check200_response import HealthControllerCheck200Response

# TODO update the JSON string below
json = "{}"
# create an instance of HealthControllerCheck200Response from a JSON string
health_controller_check200_response_instance = HealthControllerCheck200Response.from_json(json)
# print the JSON string representation of the object
print HealthControllerCheck200Response.to_json()

# convert the object into a dict
health_controller_check200_response_dict = health_controller_check200_response_instance.to_dict()
# create an instance of HealthControllerCheck200Response from a dict
health_controller_check200_response_form_dict = health_controller_check200_response.from_dict(health_controller_check200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


