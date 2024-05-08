# CreateExperimentInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 

## Example

```python
from montelo.client.models.create_experiment_input import CreateExperimentInput

# TODO update the JSON string below
json = "{}"
# create an instance of CreateExperimentInput from a JSON string
create_experiment_input_instance = CreateExperimentInput.from_json(json)
# print the JSON string representation of the object
print CreateExperimentInput.to_json()

# convert the object into a dict
create_experiment_input_dict = create_experiment_input_instance.to_dict()
# create an instance of CreateExperimentInput from a dict
create_experiment_input_form_dict = create_experiment_input.from_dict(create_experiment_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


