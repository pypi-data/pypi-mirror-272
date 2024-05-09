import os
from typing import Optional, List

from pydantic import StrictStr

from montelo.client import ApiClient, Configuration, CreateDatasetInput, DatasetDto, AddToDatasetInput, DatapointDto, \
    DatasetApi, DatapointApi, BatchAddToDatasetInput, CreateExperimentInput, ExperimentDto, ExperimentApi, \
    CreateDatapointRunInput, DatapointRunDto, DatapointRunApi, UpdateDatapointRunInput, EventQueuedDto, \
    PaginatedExperimentWithDatapointsDto, LogsApi, EndLogInput, CreateLogInput, LogInput
from montelo.context_vars import ctx_datapoint_run_id
from montelo.types import MonteloClientOptions


class MonteloClient:
    def __init__(self, options: Optional[MonteloClientOptions]):
        self.trace = None
        if options is None:
            api_key = os.environ.get("MONTELO_API_KEY")
            base_url = os.environ.get("MONTELO_BASE_URL", "https://api-sdk.montelo.ai")
        else:
            api_key = options.api_key or os.environ.get("MONTELO_API_KEY")
            base_url = options.base_url or os.environ.get("MONTELO_BASE_URL", "https://api-sdk.montelo.ai")

        if not api_key:
            raise Exception("Montelo API key not set.")

        self.configuration = Configuration(
            host=base_url,
            access_token=api_key
        )

    def set_trace(self, trace):
        self.trace = trace

    def get_trace(self):
        return self.trace

    def create_log(
            self,
            *,
            log: LogInput,
    ):
        datapoint_run_id = ctx_datapoint_run_id.get()
        with ApiClient(configuration=self.configuration) as api_client:
            api_instance = LogsApi(api_client)
            api_instance.logs_controller_create_log(
                create_log_input=CreateLogInput(
                    datapoint_run_id=datapoint_run_id,
                    log=log,
                    trace=self.trace,
                )
            )

    def end_log(
            self,
            *,
            id: StrictStr,
            log: EndLogInput
    ):
        token = ctx_datapoint_run_id.get()
        if not token:
            with ApiClient(configuration=self.configuration) as api_client:
                api_instance = LogsApi(api_client)
                api_instance.logs_controller_end_log(
                    log_id=id,
                    end_log_input=log,
                )

    def create_dataset(self, create_dataset_input: CreateDatasetInput) -> DatasetDto:
        with ApiClient(configuration=self.configuration) as api_client:
            api_instance = DatasetApi(api_client)
            return api_instance.dataset_controller_create(create_dataset_input=create_dataset_input)

    def create_datapoint(
            self,
            *,
            dataset_slug: StrictStr,
            add_to_dataset_input: AddToDatasetInput
    ) -> DatapointDto:
        with ApiClient(configuration=self.configuration) as api_client:
            api_instance = DatapointApi(api_client)
            return api_instance.datapoint_controller_add_to_dataset_by_slug(
                dataset_slug=dataset_slug,
                add_to_dataset_input=add_to_dataset_input,
            )

    def create_batch_datapoints(self, *, slug: StrictStr, datapoints: List[AddToDatasetInput]) -> None:
        with ApiClient(configuration=self.configuration) as api_client:
            api_instance = DatapointApi(api_client)
            batch_params = BatchAddToDatasetInput(datapoints=datapoints)
            api_instance.datapoint_controller_batch_add_to_dataset_by_slug(
                dataset_slug=slug,
                batch_add_to_dataset_input=batch_params
            )

    def create_experiment(
            self,
            *,
            slug: StrictStr,
            create_experiment_input: CreateExperimentInput
    ) -> ExperimentDto:
        with ApiClient(configuration=self.configuration) as api_client:
            api_instance = ExperimentApi(api_client)
            return api_instance.experiment_controller_create(
                dataset_slug=slug,
                create_experiment_input=create_experiment_input
            )

    def create_datapoint_run(self, create_datapoint_run_input: CreateDatapointRunInput) -> DatapointRunDto:
        with ApiClient(configuration=self.configuration) as api_client:
            api_instance = DatapointRunApi(api_client)
            return api_instance.datapoint_run_controller_create_datapoint_run(
                create_datapoint_run_input=create_datapoint_run_input
            )

    def update_datapoint_run(self, update_datapoint_run_input: UpdateDatapointRunInput) -> EventQueuedDto:
        with ApiClient(configuration=self.configuration) as api_client:
            api_instance = DatapointRunApi(api_client)
            return api_instance.datapoint_run_controller_update_datapoint_run(
                update_datapoint_run_input=update_datapoint_run_input
            )

    def get_datapoints_by_experiment_id(
            self,
            *,
            experiment_id: StrictStr,
            take: Optional[int] = None,
            skip: Optional[int] = None
    ) -> PaginatedExperimentWithDatapointsDto:
        with ApiClient(configuration=self.configuration) as api_client:
            api_instance = ExperimentApi(api_client)
            take_str = str(take) if take is not None else None
            skip_str = str(skip) if skip is not None else None

            return api_instance.experiment_controller_get_paginated_datapoints_for_experiment(
                experiment_id=experiment_id,
                take=take_str,
                skip=skip_str,
            )
