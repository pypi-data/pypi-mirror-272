from typing import Any, Dict, Literal, Optional, List

from montelo.MonteloClient import MonteloClient
from montelo.client import AddToDatasetInput, DatapointDto


class MonteloDatapoints:
    def __init__(self, montelo_client: MonteloClient):
        self._montelo_client = montelo_client

    def create(
            self,
            *,
            dataset: str,
            input: Dict[str, Any],
            expected_output: Dict[str, Any],
            split: Optional[Literal["TRAIN", "TEST"]] = None,
            metadata: Optional[Dict[str, Any]] = None,
    ) -> DatapointDto:
        payload = AddToDatasetInput(
            input=input,
            expected_output=expected_output,
            split=split,
            metadata=metadata,
            source="API",
            source_id=None,
        )
        return self._montelo_client.create_datapoint(
            dataset_slug=dataset,
            add_to_dataset_input=payload
        )

    def create_many(
            self,
            *,
            dataset: str,
            datapoints: List[Dict[str, Any]],
            split: Optional[Literal["TRAIN", "TEST"]] = None,
    ) -> None:
        def chunk_list(data, size):
            return (data[i:i + size] for i in range(0, len(data), size))

        chunks = chunk_list(datapoints, 100)

        def process_chunk(chunk):
            dps = [
                AddToDatasetInput(
                    input=datapoint["input"],
                    expected_output=datapoint["expected_output"],
                    metadata=datapoint.get("metadata", None),
                    split=split,
                    source="API",
                    source_id=None
                ) for datapoint in chunk
            ]
            self._montelo_client.create_batch_datapoints(slug=dataset, datapoints=dps)

        [process_chunk(chunk) for chunk in chunks]
