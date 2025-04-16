import os

from service.logger import logger
from service.provider import Provider
from service.service import Service


def _provision_providers():
    available_providers = []
    provider_urls = os.getenv("PROVIDER_URLS").split(",")
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
