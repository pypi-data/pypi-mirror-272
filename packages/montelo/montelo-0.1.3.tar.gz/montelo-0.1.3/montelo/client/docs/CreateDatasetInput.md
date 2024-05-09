# CreateDatasetInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**input_schema** | **object** |  | [optional] 
**output_schema** | **object** |  | [optional] 
**is_fine_tuning** | **bool** |  | [optional] 

## Example

```python
from montelo.client.models.create_dataset_input import CreateDatasetInput

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDatasetInput from a JSON string
create_dataset_input_instance = CreateDatasetInput.from_json(json)
# print the JSON string representation of the object
print CreateDatasetInput.to_json()

# convert the object into a dict
create_dataset_input_dict = create_dataset_input_instance.to_dict()
# create an instance of CreateDatasetInput from a dict
create_dataset_input_form_dict = create_dataset_input.from_dict(create_dataset_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


