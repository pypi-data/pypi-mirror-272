# ExperimentWithDatapointsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**dataset_id** | **str** |  | 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**created_at** | **str** |  | 
**dataset** | [**FullDatasetDto**](FullDatasetDto.md) |  | 

## Example

```python
from montelo.client.models.experiment_with_datapoints_dto import ExperimentWithDatapointsDto

# TODO update the JSON string below
json = "{}"
# create an instance of ExperimentWithDatapointsDto from a JSON string
experiment_with_datapoints_dto_instance = ExperimentWithDatapointsDto.from_json(json)
# print the JSON string representation of the object
print ExperimentWithDatapointsDto.to_json()

# convert the object into a dict
experiment_with_datapoints_dto_dict = experiment_with_datapoints_dto_instance.to_dict()
# create an instance of ExperimentWithDatapointsDto from a dict
experiment_with_datapoints_dto_form_dict = experiment_with_datapoints_dto.from_dict(experiment_with_datapoints_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


