from collections import deque
from time import sleep
from typing import List

from web3.exceptions import BlockNotFound

from service.exceptions import NodeUnhealthy
from service.logger import logger
from service.provider import Provider


class Service:

    def __init__(self, providers: List[Provider]):
        """
        Get from provider_urls env variable
        Instantiate providers, screw the errors, take the healthy ones
        Use collections.deque for storing providers.
        When consuming, take first provider from the deque.
        """
        # if no providers are available, raise an error - that won't work
        if len(providers) == 0:
            raise Exception("No providers are available, won't work!")
        self.provider_queue = deque(providers)

    def _get_last_block(self) -> int:
        """
        Get the last block from any provider that can be reached
        FIXME: this is going to run for infinity if there are no healthy providers
        so some kind of timeout should be added
        """
        while True:
            try:
                return self.provider_queue[0].get_last_block()
            except NodeUnhealthy:
                logger.info(
                    "Can't get the last block: provider is unhealthy, rotating the queue"
                )
                self.provider_queue.rotate()
                continue

    def run(self):
        """Consume from provider for as long as healthy
        When not, switch to the next provider
        """
        logger.info("Starting service")
        last_block = self._get_last_block()
        logger.info(f"Discovered last block: {last_block}")
        while True:
            running_node = self.provider_queue[0]
            logger.info(f"Consuming from provider {running_node.name}")
            try:
                running_node.get_block_by_number(last_block)
                logger.info(f"Consumed block {last_block}")
                last_block += 1
            except BlockNotFound:
                # no drama
                logger.info(
                    f"Block {last_block} not found yet, sleeping for 10 seconds"
                )
                sleep(10)
            except NodeUnhealthy:
                # move the current node to the deque
                logger.info(
                    f"Provider {running_node.name} is unhealthy, moving to the end of the queue"
                )
                self.provider_queue.rotate()
                continue
