import subprocess
import pytest

from kestrel_datasource_stixshifter.diagnosis import Diagnosis
from kestrel_datasource_stixshifter.connector import setup_connector_module
from .utils import stixshifter_profile_lab101, stixshifter_profile_ecs


STIX_SHIFTER_DIAG = "stix-shifter-diag"


def test_diagnosis(stixshifter_profile_lab101):
    pattern = " ".join(
        [
            "[ipv4-addr:value != '255.255.255.255']",
            "START t'2000-01-01T00:00:00.000Z' STOP t'3000-01-01T00:00:00.000Z'",
        ]
    )
    diag = Diagnosis("lab101")
    diag.diagnose_config()
    diag.diagnose_ping()
    assert pattern == diag.diagnose_translate_query(pattern)["queries"][0]
    res = diag.diagnose_run_query_and_retrieval_result([pattern], 1)
    assert len(res) == 1 and res[0] == 533


def test_cli(stixshifter_profile_lab101):
    expected_output = """
## Diagnose: config verification

#### Kestrel specific config
retrieval batch size: 2000
cool down after transmission: 0
allow unverified connector: False
verify SSL or not: True
split query into subquery: False
subquery with time window (in seconds): 0
enable fast translation: False

#### Config to be passed to stix-shifter
connector name: stix_bundle
connection object [ref: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/OVERVIEW.md#connection]:
{
    "host": "https://github.com/opencybersecurityalliance/data-bucket-kestrel/blob/main/stix-bundles/lab101.json?raw=true",
    "options": {
        "result_limit": 4000,
        "timeout": 60
    }
}
configuration object [ref: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/OVERVIEW.md#configuration]:
{
    "auth": {
        "username": null,
        "password": null
    }
}

## Diagnose: stix-shifter query translation

#### Input: STIX pattern
[ipv4-addr:value != '255.255.255.255'] START t'2000-01-01T00:00:00.000Z' STOP t'3000-01-01T00:00:00.000Z'

#### Output: 1 data source native queries
[ipv4-addr:value != '255.255.255.255'] START t'2000-01-01T00:00:00.000Z' STOP t'3000-01-01T00:00:00.000Z'

## Diagnose: stix-shifter to data source connection (network, auth)

#### Results from stixshifter transmission.ping()
{
    "success": true
}

## Diagnose: stix-shifter query execution: <=1 batch(s)

#### data retrieval results:
one batch retrieved: 533 entries

## Diagnose: stix-shifter query execution: <=5 batch(s)

#### data retrieval results:
one batch retrieved: 533 entries
"""

    result = subprocess.run(
        args=[STIX_SHIFTER_DIAG, "--start=2000-01-01T00:00:00.000Z", "--stop=3000-01-01T00:00:00.000Z", "lab101"],
        universal_newlines=True,
        stdout=subprocess.PIPE,
    )

    result_lines = result.stdout.splitlines()
    result_lines = [x for x in result_lines if x]
    expected_lines = expected_output.splitlines()
    expected_lines = [x for x in expected_lines if x]
    for x, y in zip(result_lines, expected_lines):
        assert x == y


def test_cli_ecs(stixshifter_profile_ecs):
    expected_output = """
## Diagnose: config verification

#### Kestrel specific config
retrieval batch size: 2000
cool down after transmission: 0
allow unverified connector: False
verify SSL or not: True
split query into subquery: False
subquery with time window (in seconds): 0
enable fast translation: False

#### Config to be passed to stix-shifter
connector name: elastic_ecs
connection object [ref: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/OVERVIEW.md#connection]:
{
    "host": "elastic.securitylog.company.com",
    "port": 9200,
    "selfSignedCert": false,
    "indices": "host101",
    "options": {
        "result_limit": 4000,
        "timeout": 60
    }
}
configuration object [ref: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/OVERVIEW.md#configuration]:
{
    "auth": {
        "id": "********",
        "api_key": "********"
    }
}

## Diagnose: stix-shifter query translation

#### Input: STIX pattern
[x-oca-asset:device_id = '123456'] START t'2000-01-01T00:00:00.000Z' STOP t'3000-01-01T00:00:00.000Z'

#### Output: 1 data source native queries
(host.id : "123456" OR observer.serial_number : "123456") AND (@timestamp:["2000-01-01T00:00:00.000Z" TO "3000-01-01T00:00:00.000Z"])
"""

    setup_connector_module("elastic_ecs")

    result = subprocess.run(
        args=[
            STIX_SHIFTER_DIAG,
            "-p",
            "[x-oca-asset:device_id = '123456'] START t'2000-01-01T00:00:00.000Z' STOP t'3000-01-01T00:00:00.000Z'",
            "-t",
            "ecs",
        ],
        universal_newlines=True,
        stdout=subprocess.PIPE,
    )

    result_lines = result.stdout.splitlines()
    result_lines = [x for x in result_lines if x]
    expected_lines = expected_output.splitlines()
    expected_lines = [x for x in expected_lines if x]
    for x, y in zip(result_lines, expected_lines):
        assert x == y
