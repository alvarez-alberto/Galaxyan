from src.engine.services.configs_service import ConfigsService
from src.engine.services.fonts_service import FontsService
from src.engine.services.images_service import ImagesService
from src.engine.services.score_service import ScoreService
from src.engine.services.sounds_service import SoundsService

class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsService()
    fonts_service = FontsService()
    configs_service = ConfigsService()
    score_service = ScoreService()