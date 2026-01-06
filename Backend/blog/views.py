from rest_framework import generics, permissions, status, mixins
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from blog.serializer import BlogSerializer , BlogPostImageSerializer
from blog.models import Blog, BlogContentImage

class CreateBlogView(generics.CreateAPIView):
    """Create a new blog"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BlogContentImageView(generics.GenericAPIView, mixins.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlogPostImageSerializer
    queryset = BlogContentImage.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        name = self.request.query_params.get("name")
        if name is None:
            raise NotFound("Name query parameter is required.")
        try:
            instance = self.get_queryset().get(name=name)
            return Response({"image_url": instance.image.url})
        except BlogContentImage.DoesNotExist:
            raise NotFound("Image with that name does not exist.")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"image_url": serializer.instance.image.url}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class UpdateBlogView(generics.RetrieveUpdateAPIView):
    """Retrive  and update the user"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def get_object(self):
        blog = super().get_object()

        if self.request.method in ["PUT", "PATCH"]:
            if blog.user != self.request.user:
                raise PermissionDenied("You cannot update another user's blog.")

        return blog


