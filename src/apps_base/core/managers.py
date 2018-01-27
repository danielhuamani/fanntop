from django.db import models


class CoreActiveModelManager(models.QuerySet):
    def not_trash(self):
        return self.filter(is_trash=False)

    def active(self):
        return self.filter(is_active=True, is_trash=False)
