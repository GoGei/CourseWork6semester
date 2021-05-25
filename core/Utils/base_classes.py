from django.db import models
from django.utils import translation, timezone
from django.conf import settings


class TranslateMixin(models.Model):
    TRANSLATED_FIELDS = []

    class Meta:
        abstract = True

    def __getattr__(self, key):
        if key and key in self.TRANSLATED_FIELDS:
            return getattr(self, f'{key}_data', {}).get(translation.get_language(), None)
        return super(TranslateMixin, self).__getattribute__(key)

    def __setattr__(self, key, value):
        if key and key in self.TRANSLATED_FIELDS:
            return getattr(self, f'{key}_data', {}).update({translation.get_language(): value})
        return super(TranslateMixin, self).__setattr__(key, value)

    def get_form_initial(self):
        languages = list(zip(*settings.LANGUAGES))[0]
        rc = []
        for language in languages:
            field_data = {'language_code': language}
            for field in self.TRANSLATED_FIELDS:
                data = getattr(self, '%s_data' % field).get(language, None)
                field_data.update({field: data})
            rc.append(field_data)
        return rc


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(archived__isnull=True)


class CrmMixin(models.Model):
    created = models.DateTimeField(default=timezone.now, db_index=True)
    changed = models.DateTimeField(auto_now=timezone.now)
    archived = models.DateTimeField(null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')

    objects = ActiveQuerySet.as_manager()

    class Meta:
        abstract = True

    def archive(self, user=None):
        self.archived = timezone.now()
        self.archived_by = user
        self.save()
