from unittest.mock import Mock

from service.exceptions import NodeUnhealthy
from service.service import Service

HealthyProviderMock = Mock(
    get_last_block=Mock(return_value=100), get_block_by_number=Mock(return_value=101)
)

UnhealthyProviderMock = Mock(
    get_last_block=Mock(side_effect=NodeUnhealthy),
    get_block_by_number=Mock(side_effect=NodeUnhealthy),
)


def test_integration_hotswitch():
    """
    Test that the service can hot switch between providers
    Service has two providers, and when one is unhealthy, the other one is used
    """
    service = Service(providers=[HealthyProviderMock, UnhealthyProviderMock])
    # TODO: finish it, that test is not complete
    # running it ends with infinite loop
    # service.run()
