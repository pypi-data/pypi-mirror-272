# DatapointRunDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**experiment_id** | **str** |  | 
**datapoint_id** | **str** |  | 
**output** | **object** |  | 

## Example

```python
from montelo.client.models.datapoint_run_dto import DatapointRunDto

# TODO update the JSON string below
json = "{}"
# create an instance of DatapointRunDto from a JSON string
datapoint_run_dto_instance = DatapointRunDto.from_json(json)
# print the JSON string representation of the object
print DatapointRunDto.to_json()

# convert the object into a dict
datapoint_run_dto_dict = datapoint_run_dto_instance.to_dict()
# create an instance of DatapointRunDto from a dict
datapoint_run_dto_form_dict = datapoint_run_dto.from_dict(datapoint_run_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


