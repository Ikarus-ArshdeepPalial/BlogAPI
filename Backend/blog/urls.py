"""urls for blog api"""

from django.urls import path
from blog.views import CreateBlogView , UpdateBlogView, BlogContentImageView

app_name = "blog"

urlpatterns = [
    path("create/", CreateBlogView.as_view(), name="create"),
    path("manage/<int:pk>/", UpdateBlogView.as_view(), name="manage"),
    path("image/manage/", BlogContentImageView.as_view(), name="image-manage"),
]