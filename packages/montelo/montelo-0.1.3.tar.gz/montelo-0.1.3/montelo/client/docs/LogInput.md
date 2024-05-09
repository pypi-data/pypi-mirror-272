# LogInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**source** | **str** |  | 
**model** | **str** |  | [optional] 
**input** | **object** |  | [optional] 
**output** | **object** |  | [optional] 
**start_time** | **str** |  | [optional] 
**end_time** | **str** |  | [optional] 
**duration** | **float** |  | [optional] 
**tokens** | [**TokenInfo**](TokenInfo.md) |  | [optional] 
**extra** | **object** |  | [optional] 

## Example

```python
from montelo.client.models.log_input import LogInput

# TODO update the JSON string below
json = "{}"
# create an instance of LogInput from a JSON string
log_input_instance = LogInput.from_json(json)
# print the JSON string representation of the object
print LogInput.to_json()

# convert the object into a dict
log_input_dict = log_input_instance.to_dict()
# create an instance of LogInput from a dict
log_input_form_dict = log_input.from_dict(log_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


