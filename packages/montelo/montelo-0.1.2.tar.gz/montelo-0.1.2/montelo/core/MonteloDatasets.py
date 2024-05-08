from typing import Optional, Dict, Any

from montelo.MonteloClient import MonteloClient
from montelo.client import CreateDatasetInput, DatasetDto


class MonteloDatasets:
    def __init__(self, montelo_client: MonteloClient):
        self._montelo_client = montelo_client

    def create(
            self,
            *,
            name: str,
            description: Optional[str] = None,
            input_schema: Optional[Dict[str, Any]],
            output_schema: Optional[Dict[str, Any]],
    ) -> DatasetDto:
        params = CreateDatasetInput(
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            is_fine_tuning=False,
        )
        return self._montelo_client.create_dataset(create_dataset_input=params)

    def create_fine_tune(
            self,
            *,
            name: str,
            description: Optional[str] = None,
    ) -> DatasetDto:
        params = CreateDatasetInput(
            name=name,
            description=description,
            is_fine_tuning=True,
        )
        return self._montelo_client.create_dataset(create_dataset_input=params)
