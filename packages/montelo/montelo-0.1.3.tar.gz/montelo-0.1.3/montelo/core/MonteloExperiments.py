import threading
from typing import Optional, Callable, Dict

from pydantic import StrictStr

from montelo.MonteloClient import MonteloClient
from montelo.client import CreateExperimentInput, ExperimentDto, CreateDatapointRunInput, UpdateDatapointRunInput
from montelo.context_vars import ctx_datapoint_run_id


class MonteloExperiments:
    def __init__(self, montelo_client: MonteloClient):
        self._montelo_client = montelo_client

    def create(
            self,
            *,
            dataset: StrictStr,
            name: StrictStr,
            description: Optional[StrictStr] = None
    ) -> ExperimentDto:
        params = CreateExperimentInput(
            name=name,
            description=description,
        )
        return self._montelo_client.create_experiment(
            slug=dataset,
            create_experiment_input=params,
        )

    def run(
            self,
            *,
            experiment_id: StrictStr,
            runner: Callable,
            evaluator: Callable,
            options: Optional[Dict] = None,
    ):
        try:
            # Default options
            take = 100
            skip = 0
            has_more_datapoints = True
            only_test_split = options.get("only_test_split", False) if options else False
            parallelism = options.get("parallelism", 1) if options else 1
            parallelism = 100 if parallelism > 100 else parallelism

            while has_more_datapoints:
                response = self._montelo_client.get_datapoints_by_experiment_id(
                    experiment_id=experiment_id,
                    take=take,
                    skip=skip
                )

                total_datapoints = response.total_datapoints
                datapoints = response.experiment.dataset.datapoints

                filtered_datapoints = [d for d in datapoints if not only_test_split or d.split == "TEST"]

                def process_datapoint(datapoint):
                    datapoint_run = self._montelo_client.create_datapoint_run(
                        create_datapoint_run_input=CreateDatapointRunInput(
                            experiment_id=experiment_id,
                            datapoint_id=datapoint.id,
                        )
                    )
                    ctx_datapoint_run_id.set(datapoint_run.id)

                    output = runner(
                        input=datapoint.input,
                        metadata=datapoint.metadata
                    )

                    evaluation = evaluator(
                        input=datapoint.input,
                        expected_output=datapoint.expected_output,
                        actual_output=output,
                        metadata=datapoint.metadata,
                    )

                    ctx_datapoint_run_id.set("")

                    payload = UpdateDatapointRunInput(
                        datapoint_run_id=datapoint_run.id,
                        output=output,
                        evaluation=evaluation,
                    )
                    self._montelo_client.update_datapoint_run(update_datapoint_run_input=payload)

                def process_in_batches(dps):
                    threads = []
                    for datapoint in dps:
                        thread = threading.Thread(target=process_datapoint, args=(datapoint,))
                        threads.append(thread)
                        thread.start()

                    # Wait for all threads in this batch to complete
                    for thread in threads:
                        thread.join()

                def chunked_datapoints(dps, size):
                    for i in range(0, len(dps), size):
                        yield dps[i:i + size]

                for batch in chunked_datapoints(filtered_datapoints, parallelism):
                    process_in_batches(batch)

                # Update skip for the next batch
                skip += take
                has_more_datapoints = skip < total_datapoints

            print("Experiment completed successfully!")
        except Exception as e:
            print(f"Error running experiment: {str(e)}")

    def create_and_run(
            self,
            *,
            dataset: StrictStr,
            name: StrictStr,
            description: Optional[StrictStr] = None,
            runner: Callable,
            evaluator: Callable,
            options: Optional[Dict] = None,
    ):
        experiment = self.create(
            dataset=dataset,
            name=name,
            description=description,
        )

        self.run(
            experiment_id=experiment.id,
            runner=runner,
            evaluator=evaluator,
            options=options,
        )
