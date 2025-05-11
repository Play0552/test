from fastapi import Depends

from app.repository.feature.feature import FeatureRepository, get_feature_repository


class FeatureService:
    def __init__(self, repository: FeatureRepository):
        self.repository = repository


def get_feature_service(
    repository: FeatureRepository = Depends(get_feature_repository),
):
    return FeatureService(repository)
