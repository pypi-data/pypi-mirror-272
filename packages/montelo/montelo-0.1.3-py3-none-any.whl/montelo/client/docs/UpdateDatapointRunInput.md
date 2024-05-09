# UpdateDatapointRunInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**datapoint_run_id** | **str** |  | 
**output** | **object** |  | 
**evaluation** | **object** |  | 

## Example

```python
from montelo.client.models.update_datapoint_run_input import UpdateDatapointRunInput

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateDatapointRunInput from a JSON string
update_datapoint_run_input_instance = UpdateDatapointRunInput.from_json(json)
# print the JSON string representation of the object
print UpdateDatapointRunInput.to_json()

# convert the object into a dict
update_datapoint_run_input_dict = update_datapoint_run_input_instance.to_dict()
# create an instance of UpdateDatapointRunInput from a dict
update_datapoint_run_input_form_dict = update_datapoint_run_input.from_dict(update_datapoint_run_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


