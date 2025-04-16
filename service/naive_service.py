from collections import deque
from typing import List

from service.exceptions import NodeUnhealthy
from service.provider import Provider


class NaiveService:
    """
    Consumes blocks by numbers from start to end.
    """

    def __init__(self, provider: Provider):
        self.provider = provider

    def run(self):
        last_block = self.provider.get_last_block()
        for block_number in range(last_block):
            self.provider.get_block_by_number(block_number)
