from rest_framework import generics, permissions, status, mixins
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from blog.serializer import BlogSerializer, BlogPostImageSerializer
from blog.models import Blog, BlogContentImage
from blog.paginator import BlogPagination
from blog.e_search.documents import BlogDocument


class CreateBlogView(generics.CreateAPIView):
    """Create a new blog"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlogSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GetBlogList(generics.ListAPIView):
    """Get all blogs with pagination"""
    
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = BlogPagination

class GetRandomBlog(APIView):
    """Get random blog for home page or the most recent one"""
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        recent = request.query_params.get('recent', 'false').lower() == 'true'
        
        blog = None
        if recent:
            blog = Blog.objects.order_by('-created_at').first()
        else:
            blog = Blog.objects.order_by('?').first()

        if not blog:
            return Response({"detail": "No blogs available."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    

class SearchBlogs(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q')

        if query:
            search = BlogDocument.search().query('multi_match', query=query, fields=['name', 'content'])
            queryset = search.to_queryset()
            serializer = BlogSerializer(queryset, many=True)
            return Response(serializer.data)
        
        return Response([])
    
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
    
class BlogContentImageView(generics.GenericAPIView, mixins.CreateModelMixin):
    """Blog content images"""
    
    # permission_classes = [permissions.IsAuthenticated]
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
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"image_url": serializer.instance.image.url}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()