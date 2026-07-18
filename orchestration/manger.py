from common.logger import logger

from orchestration.registry import CONNECTORS


class PipelineManager:

    def __init__(self):

        self.connectors = CONNECTORS
for connector_class in self.connectors:

    connector = connector_class()

    try:

        connector.run()

    except Exception as e:

        logger.exception(
            f"{connector.name} failed: {e}"
        )
