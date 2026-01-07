"""urls for blog api"""

from django.urls import path
from blog.views import (
    CreateBlogView, 
    UpdateBlogView, 
    BlogContentImageView, 
    GetBlogList,
    SearchBlogs
)

app_name = "blog"

urlpatterns = [
    path("create/", CreateBlogView.as_view(), name="create"),
    path("manage/<int:pk>/", UpdateBlogView.as_view(), name="manage"),
    path("image/manage/", BlogContentImageView.as_view(), name="image-manage"),
    path("get_blogs/", GetBlogList.as_view(), name="get_blogs"),
    path("search/", SearchBlogs.as_view(), name="search"),
]
