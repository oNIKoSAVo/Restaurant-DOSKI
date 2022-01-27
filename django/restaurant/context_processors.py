from restaurant.models import Setting


def footer(request):
    try:
        setting = Setting.objects.get(pk=1)
#         print(setting.privacy_file.url)
        return {
            "oferta_url": setting.oferta_file.url if setting.oferta_file else None,
            "privacy_url": setting.privacy_file.url if setting.privacy_file else None
        }
    except Setting.DoesNotExist:
        return {}
