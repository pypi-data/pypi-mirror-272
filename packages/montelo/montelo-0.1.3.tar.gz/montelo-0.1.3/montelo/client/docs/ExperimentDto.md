# ExperimentDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**dataset_id** | **str** |  | 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**created_at** | **str** |  | 

## Example

```python
from montelo.client.models.experiment_dto import ExperimentDto

# TODO update the JSON string below
json = "{}"
# create an instance of ExperimentDto from a JSON string
experiment_dto_instance = ExperimentDto.from_json(json)
# print the JSON string representation of the object
print ExperimentDto.to_json()

# convert the object into a dict
experiment_dto_dict = experiment_dto_instance.to_dict()
# create an instance of ExperimentDto from a dict
experiment_dto_form_dict = experiment_dto.from_dict(experiment_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


