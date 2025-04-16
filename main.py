import logging
import os

from service import Provider, Service

logger = logging.getLogger(__name__)


def _provision_providers():
    available_providers = []
    # remove empty strings
    provider_urls = [s for s in os.getenv("PROVIDER_URLS").split(",") if s]
    for provider_url in provider_urls:
        try:
            available_providers.append(Provider(provider_url))
        except Exception as e:
            logger.error(f"Error instantiating provider {provider_url}: {e}")
    return available_providers


def main():
    providers = _provision_providers()
    service = Service(providers)
    service.run()


if __name__ == "__main__":
    logger.info("Starting service")
    main()
