# TraceInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**user_id** | **str** |  | [optional] 
**extra** | **object** |  | [optional] 

## Example

```python
from montelo.client.models.trace_input import TraceInput

# TODO update the JSON string below
json = "{}"
# create an instance of TraceInput from a JSON string
trace_input_instance = TraceInput.from_json(json)
# print the JSON string representation of the object
print TraceInput.to_json()

# convert the object into a dict
trace_input_dict = trace_input_instance.to_dict()
# create an instance of TraceInput from a dict
trace_input_form_dict = trace_input.from_dict(trace_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


