# EventQueuedDto


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**success** | **bool** |  | 

## Example

```python
from montelo.client.models.event_queued_dto import EventQueuedDto

# TODO update the JSON string below
json = "{}"
# create an instance of EventQueuedDto from a JSON string
event_queued_dto_instance = EventQueuedDto.from_json(json)
# print the JSON string representation of the object
print EventQueuedDto.to_json()

# convert the object into a dict
event_queued_dto_dict = event_queued_dto_instance.to_dict()
# create an instance of EventQueuedDto from a dict
event_queued_dto_form_dict = event_queued_dto.from_dict(event_queued_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


