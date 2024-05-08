# AddToDatasetInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input** | **object** |  | 
**expected_output** | **object** |  | 
**source** | **str** |  | 
**source_id** | **str** |  | 
**split** | **str** |  | [optional] 
**metadata** | **object** |  | [optional] 

## Example

```python
from montelo.client.models.add_to_dataset_input import AddToDatasetInput

# TODO update the JSON string below
json = "{}"
# create an instance of AddToDatasetInput from a JSON string
add_to_dataset_input_instance = AddToDatasetInput.from_json(json)
# print the JSON string representation of the object
print AddToDatasetInput.to_json()

# convert the object into a dict
add_to_dataset_input_dict = add_to_dataset_input_instance.to_dict()
# create an instance of AddToDatasetInput from a dict
add_to_dataset_input_form_dict = add_to_dataset_input.from_dict(add_to_dataset_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


