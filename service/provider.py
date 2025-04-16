from web3 import Web3
from web3.exceptions import BlockNotFound
from service.exceptions import NodeUnhealthy

from service.logger import logger


class Provider:
    def __init__(self, provider_url: str):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.w3.is_connected:
            raise Exception(f"Failed to connect to provider {provider_url}")
        self.name = provider_url

    def get_last_block(self) -> int:
        """
        Get the last block from the provider
        """
        try:
            return self.w3.eth.block_number
        except:
            raise NodeUnhealthy

    def get_block_by_number(self, block_number: int):
        # TODO: measure and log time
        try:
            block = self.w3.eth.get_block(block_number)
            return block
        except BlockNotFound:
            # no drama
            raise

        except Exception as e:
            logger.error(
                f"Error getting block {block_number} from provider {self.name}: {e}"
            )
            raise NodeUnhealthy
