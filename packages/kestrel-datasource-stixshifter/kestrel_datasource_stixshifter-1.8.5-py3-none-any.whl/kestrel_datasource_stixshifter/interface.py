"""The STIX-shifter data source package provides access to data sources via
`stix-shifter`_.

The STIX-shifter interface connects to multiple data sources. Users need to
provide one *profile* per data source. The profile name (case insensitive) will
be used in the ``FROM`` clause of the Kestrel ``GET`` command, e.g., ``newvar =
GET entity-type FROM stixshifter://profilename WHERE ...``. Kestrel runtime
will load profiles from 3 places (the later will override the former):

#. STIX-shifter interface config file (only when a Kestrel session starts):

    Create the STIX-shifter interface config file (YAML):

    - Default path: ``~/.config/kestrel/stixshifter.yaml``.

    - A customized path specified in the environment variable ``KESTREL_STIXSHIFTER_CONFIG``.

    Example of STIX-shifter interface config file containing profiles
    (note that the ``options`` section is not required):

    .. code-block:: yaml

        profiles:
            host101:
                connector: elastic_ecs
                connection:
                    host: elastic.securitylog.company.com
                    port: 9200
                    indices: host101
                    pagination: false # disable pagination (only <10k results) to have better performance; Kestrel default: true
                    options:  # use any of this section when needed
                        verify_cert: false  # allow invalid/expired/self-signed certificate
                        retrieval_batch_size: 10000  # set to 10000 to match default Elasticsearch page size; Kestrel default across connectors: 2000
                        single_batch_timeout: 120  # increase it if hit 60 seconds (Kestrel default) timeout error for each batch of retrieval
                        cool_down_after_transmission: 2  # seconds to cool down between data source API calls, required by some API such as sentinelone; Kestrel default: 0
                        subquery_time_window: 3600 # split each query into multiple subqueries with smaller time windows specified here in seconds; Kestrel default: 0 (not split query)
                        allow_dev_connector: True  # do not check version of a connector to allow custom/testing connector installed with any version; Kestrel default: False
                        dialects:  # more info: https://github.com/opencybersecurityalliance/stix-shifter/tree/develop/stix_shifter_modules/elastic_ecs#dialects
                          - beats  # need it if the index is created by Filebeat/Winlogbeat/*beat
                config:
                    auth:
                        id: VuaCfGcBCdbkQm-e5aOx
                        api_key: ui2lp2axTNmsyakw9tvNnw
            host102:
                connector: qradar
                connection:
                    host: qradar.securitylog.company.com
                    port: 443
                config:
                    auth:
                        SEC: 123e4567-e89b-12d3-a456-426614174000
            host103:
                connector: cbcloud
                connection:
                    host: cbcloud.securitylog.company.com
                    port: 443
                config:
                    auth:
                        org-key: D5DQRHQP
                        token: HT8EMI32DSIMAQ7DJM
        options:  # this section is not required
            fast_translate:  # use firepit-native translation (Dataframe as vessel) instead of stix-shifter result translation (JSON as vessel) for the following connectors
                - qradar
                - elastic_ecs
            translation_workers_count: 8  # default: 2

    Full specifications for data source profile sections/fields:

    - Connector-specific fields: in `stix-shifter`_, go to ``stix_shifter_modules/connector_name/configuration`` like `elastic_ecs config`_.

    - General fields shared across connectors: in `stix-shifter`_, go to `stix_shifter_modules/lang_en.json`_.

    The stix-shifter YAML config supports expansion of environment variables,
    e.g., ``$HOST101_ID`` and ``$HOST101_KEY`` will be replaced by values from
    the environment variables when the following section of the config loads by
    Kestrel:

    .. code-block:: yaml

        profiles:
            host101:
                config:
                    auth:
                        id: $HOST101_ID
                        api_key: $HOST101_KEY

#. environment variables (only when a Kestrel session starts):

    Three environment variables are required for each profile:

    - ``STIXSHIFTER_PROFILENAME_CONNECTOR``: the STIX-shifter connector name,
      e.g., ``elastic_ecs``.

    - ``STIXSHIFTER_PROFILENAME_CONNECTION``: the STIX-shifter `connection
      <https://github.com/opencybersecurityalliance/stix-shifter/blob/master/OVERVIEW.md#connection>`_
      object in JSON string.

    - ``STIXSHIFTER_PROFILENAME_CONFIG``: the STIX-shifter `configuration
      <https://github.com/opencybersecurityalliance/stix-shifter/blob/master/OVERVIEW.md#configuration>`_
      object in JSON string.

    Example of environment variables for a profile:

    .. code-block:: console

        $ export STIXSHIFTER_HOST101_CONNECTOR=elastic_ecs
        $ export STIXSHIFTER_HOST101_CONNECTION='{"host":"elastic.securitylog.company.com", "port":9200, "indices":"host101"}'
        $ export STIXSHIFTER_HOST101_CONFIG='{"auth":{"id":"VuaCfGcBCdbkQm-e5aOx", "api_key":"ui2lp2axTNmsyakw9tvNnw"}}'

#. any in-session edit through the ``CONFIG`` command.

After added data source profiles into ``stixshifter.yaml``, you can test the data source:

.. code-block:: console

    $ stix-shifter-diag data_source_name

where ``data_source_name`` is any profile named in the ``stixshifter.yaml`` config file, usually used in ``FROM stixshifter://data_source_name`` in the ``GET`` command.

The diagnosis utility will check config, test query translation, try connect to the data source to execute a small and a large query, and retrieve data back. Details of all steps will be printed for diagnosis purpose.

If you launch Kestrel in debug mode, STIX-shifter debug mode is still not
enabled by default. To record debug level logs of STIX-shifter, create
environment variable ``KESTREL_STIXSHIFTER_DEBUG`` with any value.

.. _STIX-shifter: https://github.com/opencybersecurityalliance/stix-shifter
.. _elastic_ecs config: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_modules/elastic_ecs/configuration/lang_en.json
.. _stix_shifter_modules/lang_en.json: https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/stix_shifter_modules/lang_en.json

"""

import multiprocessing
from kestrel.datasource import AbstractDataSourceInterface
from kestrel_datasource_stixshifter.config import load_profiles
from kestrel_datasource_stixshifter.query import query_datasource


multiprocessing.set_start_method("spawn", force=True)


class StixShifterInterface(AbstractDataSourceInterface):
    @staticmethod
    def schemes():
        """STIX-shifter data source interface only supports ``stixshifter://`` scheme."""
        return ["stixshifter"]

    @staticmethod
    def list_data_sources(config):
        """Get configured data sources from environment variable profiles."""

        # CONFIG command is not supported
        # profiles will be updated according to YAML file and env var
        config["profiles"] = load_profiles()

        data_sources = list(config["profiles"].keys())
        data_sources.sort()
        return data_sources

    @staticmethod
    def query(uri, pattern, session_id, config, store, limit=None):
        """Query a stixshifter data source."""

        return query_datasource(uri, pattern, session_id, config, store, limit)
