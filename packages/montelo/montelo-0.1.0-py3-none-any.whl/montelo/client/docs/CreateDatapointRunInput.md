# CreateDatapointRunInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**experiment_id** | **str** |  | 
**datapoint_id** | **str** |  | 

## Example

```python
from montelo.client.models.create_datapoint_run_input import CreateDatapointRunInput

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatapointRunInput from a JSON string
create_datapoint_run_input_instance = CreateDatapointRunInput.from_json(json)
# print the JSON string representation of the object
print CreateDatapointRunInput.to_json()

# convert the object into a dict
create_datapoint_run_input_dict = create_datapoint_run_input_instance.to_dict()
# create an instance of CreateDatapointRunInput from a dict
create_datapoint_run_input_form_dict = create_datapoint_run_input.from_dict(create_datapoint_run_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


