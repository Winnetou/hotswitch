from unittest.mock import Mock, patch

import pytest

from service.exceptions import NodeUnhealthy
from service.provider import Provider
from service.service import Service

# this one will instantiate, and do what it's supposed to
get_block_mock = Mock()
get_block_mock.return_value = {"number": 101, "transactions": [], "hash": "deadbeef"}

Web3Mock = Mock(
    is_connected=True,
    eth=Mock(block_number=100, get_block=get_block_mock),
)
# this one will instantiate, but raise an exception on every call
Web3UnhealthyMock = Mock(
    is_connected=True, eth=Mock(block_number=Mock(side_effect=Exception))
)

# this one will never instantiate
Web3DeadMock = Mock(
    is_connected=False,
)


def test_provider_returns_last_block():
    """
    Test that the provider returns the last block - happy path
    """
    with patch("service.provider.Web3", return_value=Web3Mock):
        provider = Provider(provider_url="https://taralala7")
        last_block = provider.get_last_block()
        assert last_block == 100



def test_provider_never_instantiates_unhealthy_node():
    """
    Test that the provider never instantiates the unhealthy node
    """
    with patch("service.provider.Web3", return_value=Web3DeadMock):
        with pytest.raises(Exception):
            Provider(provider_url="https://taralala7")


def test_provider_returns_block_by_number():
    """
    Test that the provider returns the block by number - happy path
    """
    with patch("service.provider.Web3", return_value=Web3Mock):
        provider = Provider(provider_url="https://taralala7")
        block = provider.get_block_by_number(101)
        assert block == {"number": 101, "transactions": [], "hash": "deadbeef"}
