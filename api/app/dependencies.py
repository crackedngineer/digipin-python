from .services.digipin_services import DigipinService


def get_digipin_service() -> DigipinService:
    """Dependency for DigipinService."""
    return DigipinService()
