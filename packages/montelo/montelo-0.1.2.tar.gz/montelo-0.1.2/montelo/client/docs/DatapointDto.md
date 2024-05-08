# DatapointDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**input** | **object** |  | 
**expected_output** | **object** |  | 
**source** | **str** |  | 
**source_id** | **str** |  | 
**dataset_id** | **str** |  | 
**split** | **str** |  | 
**created_at** | **str** |  | 
**metadata** | **object** |  | 

## Example

```python
from montelo.client.models.datapoint_dto import DatapointDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatapointDto from a JSON string
datapoint_dto_instance = DatapointDto.from_json(json)
# print the JSON string representation of the object
print DatapointDto.to_json()

# convert the object into a dict
datapoint_dto_dict = datapoint_dto_instance.to_dict()
# create an instance of DatapointDto from a dict
datapoint_dto_form_dict = datapoint_dto.from_dict(datapoint_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


