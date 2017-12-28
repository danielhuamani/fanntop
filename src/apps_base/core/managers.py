from django.db import models


class CoreActiveModelManager(models.QuerySet):
    def not_trash(self):
        return self.filter(is_trash=False)