from rest_framework.viewsets import ViewSet
from opportuna.models import Post

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class PostingViewSet(ViewSet):
    
    def get_job_postings(self, request):
        
        query_params = request.query_params
        
        limit = query_params.get('limit')

        offset = query_params.get('offset')


        posts_queryset = Post.objects.all().order_by('-created_at')[int(offset): int(limit)]

        data = []

        for post_instance in posts_queryset:
            data.append({"title": post_instance.title, "description": post_instance.discription,
                         "company": post_instance.company,
                         "apply_url":post_instance.meta_tags.get('apply_urls')})
            
        return Response(status=HTTP_200_OK, data=data)


        
        