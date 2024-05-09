# EndLogInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**output** | **object** |  | [optional] 
**end_time** | **str** |  | [optional] 
**extra** | **object** |  | [optional] 

## Example

```python
from montelo.client.models.end_log_input import EndLogInput

# TODO update the JSON string below
json = "{}"
# create an instance of EndLogInput from a JSON string
end_log_input_instance = EndLogInput.from_json(json)
# print the JSON string representation of the object
print EndLogInput.to_json()

# convert the object into a dict
end_log_input_dict = end_log_input_instance.to_dict()
# create an instance of EndLogInput from a dict
end_log_input_form_dict = end_log_input.from_dict(end_log_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


