import time
import logging
from multiprocessing import Process, Queue, current_process
from typing import Optional
from typeguard import typechecked

from stix_shifter.stix_transmission import stix_transmission
from kestrel_datasource_stixshifter.worker import STOP_SIGN
from kestrel_datasource_stixshifter.worker.utils import (
    TransmissionResult,
    WorkerLog,
    disable_cert_verification_on_transmission,
)


@typechecked
class TransmitterPool(Process):
    def __init__(
        self,
        connector_name: str,
        connection_dict: dict,
        configuration_dict: dict,
        retrieval_batch_size: int,
        number_of_translators: int,
        cool_down_after_transmission: int,
        verify_cert: bool,
        queries: list,
        output_queue: Queue,
        limit: Optional[int],
    ):
        super().__init__()

        self.connector_name = connector_name
        self.connection_dict = connection_dict
        self.configuration_dict = configuration_dict
        self.retrieval_batch_size = retrieval_batch_size
        self.number_of_translators = number_of_translators
        self.cool_down_after_transmission = cool_down_after_transmission
        self.verify_cert = verify_cert
        self.queries = queries
        self.queue = output_queue
        self.limit = limit

    def run(self):
        transmitters = [
            Transmitter(
                self.connector_name,
                self.connection_dict,
                self.configuration_dict,
                self.retrieval_batch_size,
                self.cool_down_after_transmission,
                self.verify_cert,
                query,
                self.queue,
                self.limit,
            )
            for query in self.queries
        ]
        for transmitter in transmitters:
            transmitter.start()
        for transmitter in transmitters:
            transmitter.join()
        for _ in range(self.number_of_translators):
            self.queue.put(STOP_SIGN)


class Transmitter(Process):
    def __init__(
        self,
        connector_name: str,
        connection_dict: dict,
        configuration_dict: dict,
        retrieval_batch_size: int,
        cool_down_after_transmission: int,
        verify_cert: bool,
        query: str,
        output_queue: Queue,
        limit: Optional[int],
    ):
        super().__init__()

        self.connector_name = connector_name
        self.connection_dict = connection_dict
        self.configuration_dict = configuration_dict
        self.retrieval_batch_size = retrieval_batch_size
        self.cool_down_after_transmission = cool_down_after_transmission
        self.verify_cert = verify_cert
        self.query = query
        self.queue = output_queue
        self.limit = limit

    def run(self):
        self.worker_name = current_process().name
        self.transmission = stix_transmission.StixTransmission(
            self.connector_name,
            self.connection_dict,
            self.configuration_dict,
        )

        if not hasattr(self.transmission, "entry_point"):
            packet = TransmissionResult(
                self.worker_name,
                False,
                None,
                None,
                WorkerLog(
                    logging.ERROR,
                    f"stix-shifter connector init: {self.transmission.init_error}",
                ),
            )
            self.queue.put(packet)
        else:
            # hack stix-shifter v7 to support "disable certificate verification"
            if not self.verify_cert:
                disable_cert_verification_on_transmission(self.transmission)

            search_meta_result = self.transmission.query(self.query)

            if search_meta_result["success"]:
                self.search_id = search_meta_result["search_id"]
                if self.wait_datasource_search():
                    # no error so far
                    self.retrieve_data()

                    # some connector needs to delete the query in the datasource,
                    # e.g., chronicle, discard the return (successful or not)
                    self.transmission.delete(self.search_id)
            else:
                err_msg = (
                    search_meta_result["error"]
                    if "error" in search_meta_result
                    else "details not avaliable"
                )
                packet = TransmissionResult(
                    self.worker_name,
                    False,
                    None,
                    None,
                    WorkerLog(
                        logging.ERROR,
                        f"STIX-shifter transmission.query() failed: {err_msg}",
                    ),
                )
                self.queue.put(packet)

    def wait_datasource_search(self):
        # kestrel init status: "KINIT"
        status = {"success": True, "progress": 0, "status": "KINIT"}

        while (
            status["success"]
            and status["progress"] < 100
            and status["status"] in ("KINIT", "RUNNING")
        ):
            if status["status"] == "KINIT":
                time.sleep(self.cool_down_after_transmission)
            elif status["status"] == "RUNNING":
                time.sleep(max(1, self.cool_down_after_transmission))
            status = self.transmission.status(self.search_id)
            if not status["success"]:
                err_msg = (
                    status["error"] if "error" in status else "details not avaliable"
                )
                packet = TransmissionResult(
                    self.worker_name,
                    False,
                    None,
                    None,
                    WorkerLog(
                        logging.ERROR,
                        f"STIX-shifter transmission.status() failed: {err_msg}",
                    ),
                )
                self.queue.put(packet)
                return False
        return True

    def retrieve_data(self):
        result_retrieval_offset = 0
        has_remaining_results = True
        metadata = None
        is_retry_cycle = False
        batch_size = self.retrieval_batch_size
        if self.limit and self.limit < self.retrieval_batch_size:
            batch_size = self.limit

        while has_remaining_results:
            packet = None
            time.sleep(self.cool_down_after_transmission)
            result_batch = self.transmission.results(
                self.search_id,
                result_retrieval_offset,
                batch_size,
                metadata,
            )

            if result_batch["success"]:
                if result_batch["data"]:
                    packet = TransmissionResult(
                        self.worker_name,
                        True,
                        result_batch["data"],
                        result_retrieval_offset,
                        None,
                    )

                    # prepare for next round retrieval
                    result_len = len(result_batch["data"])
                    result_retrieval_offset += result_len

                    if result_len < batch_size:
                        has_remaining_results = False

                    if "metadata" in result_batch:
                        metadata = result_batch["metadata"]
                    else:
                        has_remaining_results = False

                    if self.limit:
                        if result_retrieval_offset >= self.limit:
                            has_remaining_results = False
                        else:
                            batch_size = self.limit - result_retrieval_offset
                            if batch_size > self.retrieval_batch_size:
                                batch_size = self.retrieval_batch_size
                else:
                    has_remaining_results = False

                is_retry_cycle = False

            else:
                err_msg = (
                    result_batch["error"]
                    if "error" in result_batch
                    else "details not avaliable"
                )

                if (
                    err_msg.startswith(
                        f"{self.connector_name} connector error => server timeout_error"
                    )
                    and not is_retry_cycle
                ):
                    # mitigate https://github.com/opencybersecurityalliance/stix-shifter/issues/1493
                    # only give it one retry to mitigate high CPU occupation
                    # otherwise, it could be a real server connection issue
                    # /stix_shifter_utils/stix_transmission/utils/RestApiClientAsync.py
                    packet = TransmissionResult(
                        self.worker_name,
                        False,
                        None,
                        None,
                        WorkerLog(
                            logging.INFO,
                            "Busy CPU; hit stix-shifter aiohttp connection timeout; retry.",
                        ),
                    )
                    is_retry_cycle = True

                else:
                    packet = TransmissionResult(
                        self.worker_name,
                        False,
                        None,
                        None,
                        WorkerLog(
                            logging.ERROR,
                            f"STIX-shifter transmission.result() failed: {err_msg}",
                        ),
                    )
                    has_remaining_results = False

            if packet:
                self.queue.put(packet)
