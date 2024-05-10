# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module for ensuring compatibility with the qBraid Quantum API.

"""
import json
import logging
import pathlib
from typing import Any

from .runner import Simulator

logger = logging.getLogger(__name__)


def load_local_result(job_data: dict[str, Any]) -> dict[str, Any]:
    """
    Load the local result JSON file for a given job if the job is from 'qbraid_qir_simulator'.

    Args:
        job_data (dict[str, Any]): The job data dictionary.

    Returns:
        dict[str, Any]: The job data dictionary, potentially updated with the loaded results.
    """
    # Check if the job is from 'qbraid_qir_simulator'
    if job_data.get("qbraidDeviceId") != "qbraid_qir_simulator":
        return job_data

    # Proceed if 'vendorJobId' is available
    vendor_job_id = job_data.get("vendorJobId")
    if not vendor_job_id:
        logger.error("No vendorJobId found in job_data.")
        return job_data

    # Construct the result file path
    result_json_path = pathlib.Path.home() / ".qbraid" / "qir_runner" / f"{vendor_job_id}.json"

    # Attempt to load the JSON file
    try:
        with open(result_json_path, "r", encoding="utf-8") as file:
            job_data["result"] = json.load(file)
    except FileNotFoundError:
        logger.error("Result file not found: %s", result_json_path)
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from %s", result_json_path)
    except Exception as err:  # pylint: disable=broad-except
        logger.error("An unexpected error occurred: %s", err)

    return job_data


def transform_device_data(device_data: dict[str, Any]) -> dict[str, Any]:
    """
    Transforms the device data to be compatible with the qBraid API.

    Args:
        device_data (dict): The original device data dictionary.

    Returns:
        dict: The transformed device data dictionary.
    """
    # Create a copy of the input dictionary to avoid modifying the original data
    transformed_data = device_data.copy()

    # Normalize device type to upper case if it is a simulator
    if transformed_data.get("type") == "Simulator":
        transformed_data["type"] = "SIMULATOR"

    # Check and update availability if the device is a specific type of simulator
    if transformed_data.get("qbraid_id") == "qbraid_qir_simulator":
        simulator = Simulator()
        transformed_data["isAvailable"] = simulator.status() == "ONLINE"

    # Update device status based on availability
    if transformed_data.get("status") == "ONLINE" and not transformed_data.get("isAvailable", True):
        transformed_data["status"] = "UNAVAILABLE"

    return transformed_data
