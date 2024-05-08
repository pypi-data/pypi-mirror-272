# FullDatasetWithCountDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**FullDatasetDto**](FullDatasetDto.md) |  | 
**total_count** | **float** |  | 

## Example

```python
from montelo.client.models.full_dataset_with_count_dto import FullDatasetWithCountDto

# TODO update the JSON string below
json = "{}"
# create an instance of FullDatasetWithCountDto from a JSON string
full_dataset_with_count_dto_instance = FullDatasetWithCountDto.from_json(json)
# print the JSON string representation of the object
print FullDatasetWithCountDto.to_json()

# convert the object into a dict
full_dataset_with_count_dto_dict = full_dataset_with_count_dto_instance.to_dict()
# create an instance of FullDatasetWithCountDto from a dict
full_dataset_with_count_dto_form_dict = full_dataset_with_count_dto.from_dict(full_dataset_with_count_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


