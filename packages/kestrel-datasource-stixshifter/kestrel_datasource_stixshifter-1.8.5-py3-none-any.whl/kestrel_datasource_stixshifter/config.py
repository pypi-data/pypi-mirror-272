import os
import json
import logging
import multiprocessing
from copy import deepcopy

from kestrel.config import (
    CONFIG_DIR_DEFAULT,
    load_user_config,
)
from kestrel.utils import (
    update_nested_dict,
    mask_value_in_nested_dict,
)
from kestrel.exceptions import InvalidDataSource

PROFILE_PATH_DEFAULT = CONFIG_DIR_DEFAULT / "stixshifter.yaml"
PROFILE_PATH_ENV_VAR = "KESTREL_STIXSHIFTER_CONFIG"
STIXSHIFTER_DEBUG_ENV_VAR = "KESTREL_STIXSHIFTER_DEBUG"  # debug mode for stix-shifter if the environment variable exists
ENV_VAR_PREFIX = "STIXSHIFTER_"
RETRIEVAL_BATCH_SIZE = 2000
SINGLE_BATCH_TIMEOUT = 60
SUBQUERY_TIME_WINDOW_IN_SECONDS = 0  # if >0, then segment START/STOP into this Windows Size to file multiple subqueries
COOL_DOWN_AFTER_TRANSMISSION = 0
ALLOW_DEV_CONNECTOR = False
VERIFY_CERT = True
FAST_TRANSLATE_CONNECTORS = []  # Suggested: ["qradar", "elastic_ecs"]


_logger = logging.getLogger(__name__)


def set_stixshifter_logging_level():
    debug_mode = os.getenv(STIXSHIFTER_DEBUG_ENV_VAR, False)
    logging_level = logging.DEBUG if debug_mode else logging.INFO
    _logger.debug(f"set stix-shifter logging level: {logging_level}")
    logging.getLogger("stix_shifter").setLevel(logging_level)
    logging.getLogger("stix_shifter_utils").setLevel(logging_level)
    logging.getLogger("stix_shifter_modules").setLevel(logging_level)


def load_profiles_from_env_var():
    env_vars = os.environ.keys()
    stixshifter_vars = filter(lambda x: x.startswith(ENV_VAR_PREFIX), env_vars)
    profiles = {}
    for evar in stixshifter_vars:
        items = evar.lower().split("_")
        suffix = items[-1]
        profile = "_".join(items[1:-1])
        _logger.debug(f"processing stix-shifter env var: {evar}:")
        if profile not in profiles:
            profiles[profile] = {}

        # decoding JSON or string values from environment variables
        if suffix == "connection" or suffix == "config":
            try:
                value = json.loads(os.environ[evar])
            except json.decoder.JSONDecodeError:
                raise InvalidDataSource(
                    profile,
                    "stixshifter",
                    f"invalid JSON in {evar} environment variable",
                )
        else:
            value = os.environ[evar]

        _logger.debug(f"profile: {profile}, suffix: {suffix}, value: {value}")
        profiles[profile][suffix] = value

    return profiles


def get_datasource_from_profiles(profile_name, profiles):
    """Validate and retrieve profile data

    Validate and retrieve profile data. The data should be a dict with
    "connector", "connection", "config" keys, and appropriate values.

    Args:
        profile_name (str): The name of the profile.
        profiles (dict): name to profile (dict) mapping.

    Returns:
        STIX-shifter config triplet
    """
    profile_name = profile_name.lower()
    if profile_name not in profiles:
        raise InvalidDataSource(
            profile_name,
            "stixshifter",
            f"no {profile_name} configuration found",
        )
    else:
        profile = profiles[profile_name]
        if not profile:
            raise InvalidDataSource(
                profile_name,
                "stixshifter",
                f"the profile is empty",
            )
        profile_masked = mask_value_in_nested_dict(deepcopy(profile), "config")
        _logger.debug(f"profile to use: {profile_masked}")
        if "connector" not in profile:
            raise InvalidDataSource(
                profile_name,
                "stixshifter",
                f"no {profile_name} connector defined",
            )
        else:
            connector_name = profile["connector"]
        if "connection" not in profile:
            raise InvalidDataSource(
                profile_name,
                "stixshifter",
                f"no {profile_name} connection defined",
            )
        else:
            connection = profile["connection"]
        if "config" not in profile:
            raise InvalidDataSource(
                profile_name,
                "stixshifter",
                f"no {profile_name} configuration defined",
            )
        else:
            configuration = profile["config"]
        if "host" not in connection:
            raise InvalidDataSource(
                profile_name,
                "stixshifter",
                f'invalid {profile_name} connection section: no "host" field',
            )

        if "auth" not in configuration:
            raise InvalidDataSource(
                profile_name,
                "stixshifter",
                f'invalid {profile_name} configuration section: no "auth" field',
            )

        if "options" not in connection:
            connection["options"] = {}

        retrieval_batch_size = _extract_param_from_connection_config(
            "retrieval_batch_size",
            int,
            RETRIEVAL_BATCH_SIZE,
            connection,
            profile_name,
        )
        # rename this field for stix-shifter use; x2 the size to ensure retrieval
        connection["options"]["result_limit"] = retrieval_batch_size * 2

        single_batch_timeout = _extract_param_from_connection_config(
            "single_batch_timeout",
            int,
            SINGLE_BATCH_TIMEOUT,
            connection,
            profile_name,
        )
        # rename this field for stix-shifter use
        connection["options"]["timeout"] = single_batch_timeout

        cool_down_after_transmission = _extract_param_from_connection_config(
            "cool_down_after_transmission",
            int,
            COOL_DOWN_AFTER_TRANSMISSION,
            connection,
            profile_name,
        )

        allow_dev_connector = _extract_param_from_connection_config(
            "allow_dev_connector",
            bool,
            ALLOW_DEV_CONNECTOR,
            connection,
            profile_name,
        )

        verify_cert = _extract_param_from_connection_config(
            "verify_cert",
            bool,
            VERIFY_CERT,
            connection,
            profile_name,
        )

        subquery_time_window = _extract_param_from_connection_config(
            "subquery_time_window",
            int,
            SUBQUERY_TIME_WINDOW_IN_SECONDS,
            connection,
            profile_name,
        )

    return (
        connector_name,
        connection,
        configuration,
        retrieval_batch_size,
        cool_down_after_transmission,
        allow_dev_connector,
        verify_cert,
        subquery_time_window,
    )


def load_profiles():
    config = load_user_config(PROFILE_PATH_ENV_VAR, PROFILE_PATH_DEFAULT)
    if config and "profiles" in config:
        _logger.debug(f"stix-shifter profiles found in config file")
        profiles_from_file = {k.lower(): v for k, v in config["profiles"].items()}
    else:
        _logger.debug(
            "either config file does not exist or no stix-shifter profile found in config file. This may indicate a config syntax error if config file exists."
        )
        profiles_from_file = {}
    profiles_from_env_var = load_profiles_from_env_var()
    profiles = update_nested_dict(profiles_from_file, profiles_from_env_var)
    profiles_masked = mask_value_in_nested_dict(deepcopy(profiles), "config")
    _logger.debug(f"profiles loaded: {profiles_masked}")
    return profiles


def load_options():
    config = load_user_config(PROFILE_PATH_ENV_VAR, PROFILE_PATH_DEFAULT)
    if config and "options" in config:
        _logger.debug(f"stix-shifter options found in config file")
    else:
        _logger.debug(
            "either config file does not exist or no stix-shifter options found in config file. This may indicate a config syntax error if config file exists."
        )
        config = {"options": {}}
    if "fast_translate" not in config["options"]:
        config["options"]["fast_translate"] = FAST_TRANSLATE_CONNECTORS
    if "translation_workers_count" not in config["options"]:
        config["options"]["translation_workers_count"] = min(
            2, max(1, multiprocessing.cpu_count() - 2)
        )
    return config["options"]


def _extract_param_from_connection_config(
    param_name, processing_func, default, connection, profile_name
):
    value = default
    if param_name in connection["options"]:
        # remove the non-stix-shifter field {param_name} to avoid stix-shifter error
        try:
            value = processing_func(connection["options"].pop(param_name))
        except:
            raise InvalidDataSource(
                profile_name,
                "stixshifter",
                f"invalid {profile_name} connection section: options.{param_name}",
            )
        _logger.debug(f"profile-loaded {param_name}: {value}")
    return value
