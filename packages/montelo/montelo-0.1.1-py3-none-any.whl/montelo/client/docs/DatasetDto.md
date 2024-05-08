# DatasetDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**env_id** | **str** |  | 
**slug** | **str** |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**input_schema** | **object** |  | 
**output_schema** | **object** |  | 
**is_fine_tuning** | **bool** |  | 

## Example

```python
from montelo.client.models.dataset_dto import DatasetDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetDto from a JSON string
dataset_dto_instance = DatasetDto.from_json(json)
# print the JSON string representation of the object
print DatasetDto.to_json()

# convert the object into a dict
dataset_dto_dict = dataset_dto_instance.to_dict()
# create an instance of DatasetDto from a dict
dataset_dto_form_dict = dataset_dto.from_dict(dataset_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


