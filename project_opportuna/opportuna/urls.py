from django.urls import include, path
from opportuna.views import PostingViewSet

urlpatterns = [
    path('posting/', PostingViewSet.as_view({"get":"get_job_postings"}), name="get_job_posting_api_view")
]