# CreateLogInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**datapoint_run_id** | **str** |  | [optional] 
**log** | [**LogInput**](LogInput.md) |  | 
**trace** | [**TraceInput**](TraceInput.md) |  | [optional] 

## Example

```python
from montelo.client.models.create_log_input import CreateLogInput

# TODO update the JSON string below
json = "{}"
# create an instance of CreateLogInput from a JSON string
create_log_input_instance = CreateLogInput.from_json(json)
# print the JSON string representation of the object
print CreateLogInput.to_json()

# convert the object into a dict
create_log_input_dict = create_log_input_instance.to_dict()
# create an instance of CreateLogInput from a dict
create_log_input_form_dict = create_log_input.from_dict(create_log_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


