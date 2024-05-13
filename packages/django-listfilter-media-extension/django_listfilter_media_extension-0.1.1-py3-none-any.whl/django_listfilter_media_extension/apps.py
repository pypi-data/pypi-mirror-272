from django.apps import AppConfig
from .constants import CACHED_FILTER_SPECS
from .constants import CACHED_CHANGELIST_INSTANCE


class DjangoListfilterMediaExtensionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_listfilter_media_extension"

    def ready(self):
        from django.contrib.admin import ModelAdmin

        if not getattr(ModelAdmin, "_list_filter_extra_media_enabled", False):
            self.enable_list_filter_extra_media()

    def enable_list_filter_extra_media(self):
        from django.contrib.admin import ModelAdmin
        from django import forms
        from django_middleware_global_request.middleware import get_request

        ModelAdmin._django_listfilter_media_extension_original_media = ModelAdmin.media
        ModelAdmin._django_listfilter_media_extension_original_get_changelist_instance = (
            ModelAdmin.get_changelist_instance
        )

        def get_changelist_instance(self, request):
            if hasattr(request, CACHED_CHANGELIST_INSTANCE):
                return getattr(request, CACHED_CHANGELIST_INSTANCE)
            result = self._django_listfilter_media_extension_original_get_changelist_instance(
                request
            )
            setattr(request, CACHED_CHANGELIST_INSTANCE, result)
            # get the changelist's filter_specs and cache it into request instance
            try:
                get_filters_result = result.get_filters(request)
                if get_filters_result:
                    filter_specs = get_filters_result[0]
                else:
                    logger.error(
                        "django_listfilter_media_extension.get_changelist_instance.get_filters got NONE filters"
                    )
                    filter_specs = []
            except Exception as error:
                logger.exception(
                    "django_listfilter_media_extension.get_changelist_instance.get_filters failed: {error}".format(
                        error=error
                    )
                )
                filter_specs = []
            setattr(request, CACHED_FILTER_SPECS, filter_specs)

            return result

        @property
        def media(self):
            request = get_request()
            filter_specs = getattr(request, CACHED_FILTER_SPECS, None)
            result = self._django_listfilter_media_extension_original_media
            if filter_specs:
                for spec in filter_specs:
                    media_class = getattr(spec, "Media", None)
                    if media_class:
                        result += forms.Media(media=media_class)
            return result

        ModelAdmin.get_changelist_instance = get_changelist_instance
        ModelAdmin.media = media
