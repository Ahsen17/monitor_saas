from router import UrlPatterns

from django.contrib import admin

from stats import views as stats
from tests import views as tests

# ===================== registry urls =====================

# system urls
sysGroup = UrlPatterns().group()
sysGroup.registry('admin', admin.site.urls)
sysGroup.registry('metrics/', stats.metrics, name='prometheus_metrics')

# api urls
apiGroup = UrlPatterns().group("api", "v1")
apiGroup.registry('system/configs/', stats.SystemConfigsView.as_view(), name='system_configs')

# test urls
testGroup = UrlPatterns().group("test")
testGroup.registry('iterator/', tests.TestIterator, name='test_iterator')

routes = []
routes.extend(sysGroup.routes())
routes.extend(apiGroup.routes())
routes.extend(testGroup.routes())

urlpatterns = routes