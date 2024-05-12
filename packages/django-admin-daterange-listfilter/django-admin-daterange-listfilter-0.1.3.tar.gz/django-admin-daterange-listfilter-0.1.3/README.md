# django-admin-daterange-listfilter

通过日历自由选择时间范围。

## 使用方法

*settings.py*

```python
INSTALLED_APPS = [
    ...
    "django_static_jquery_ui",
    "django_middleware_global_request",
    "django_listfilter_media_extension",
    "django_admin_daterange_listfilter",
    ...
]
```

*admin.py*

```python
from django.contrib import admin
from django_admin_daterange_listfilter.filters import DateRangeFilter
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "add_time",
        "mod_time",
    ]
    list_filter = [
        ("add_time", DateRangeFilter),
        ("mod_time", DateRangeFilter),
    ]


admin.site.register(Category, CategoryAdmin)
```

## 版本记录

### v0.1.0

- 版本首发。

### v0.1.3

- 添加中文i18n翻译。
