# BatchAddToDatasetInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**datapoints** | [**List[AddToDatasetInput]**](AddToDatasetInput.md) |  | 

## Example

```python
from montelo.client.models.batch_add_to_dataset_input import BatchAddToDatasetInput

# TODO update the JSON string below
json = "{}"
# create an instance of BatchAddToDatasetInput from a JSON string
batch_add_to_dataset_input_instance = BatchAddToDatasetInput.from_json(json)
# print the JSON string representation of the object
print BatchAddToDatasetInput.to_json()

# convert the object into a dict
batch_add_to_dataset_input_dict = batch_add_to_dataset_input_instance.to_dict()
# create an instance of BatchAddToDatasetInput from a dict
batch_add_to_dataset_input_form_dict = batch_add_to_dataset_input.from_dict(batch_add_to_dataset_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


