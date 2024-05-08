# PaginatedExperimentWithDatapointsDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**experiment** | [**ExperimentWithDatapointsDto**](ExperimentWithDatapointsDto.md) |  | 
**total_datapoints** | **float** |  | 

## Example

```python
from montelo.client.models.paginated_experiment_with_datapoints_dto import PaginatedExperimentWithDatapointsDto

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedExperimentWithDatapointsDto from a JSON string
paginated_experiment_with_datapoints_dto_instance = PaginatedExperimentWithDatapointsDto.from_json(json)
# print the JSON string representation of the object
print PaginatedExperimentWithDatapointsDto.to_json()

# convert the object into a dict
paginated_experiment_with_datapoints_dto_dict = paginated_experiment_with_datapoints_dto_instance.to_dict()
# create an instance of PaginatedExperimentWithDatapointsDto from a dict
paginated_experiment_with_datapoints_dto_form_dict = paginated_experiment_with_datapoints_dto.from_dict(paginated_experiment_with_datapoints_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


