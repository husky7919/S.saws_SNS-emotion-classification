from django.apps import AppConfig
from .bert import BertModels


class MainConfig(AppConfig):
    name = 'main'
    modelss = BertModels()
