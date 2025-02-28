from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list_api(request):
        all_posts = BlogPost.objects.all()
        data = BlogPostSerializer(all_posts, many=True, context={"request": request}).data
        return Response({'data': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_detail_api(request, id):
        post = get_object_or_404(BlogPost, id=id)
        data = BlogPostSerializer(post).data
        return Response({'data': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_search_api(request, query):
        posts = BlogPost.objects.filter(
        Q(Title__icontains=query) | Q(Description__icontains=query))
        data = BlogPostSerializer(posts, many=True).data
        return Response({'data': data})