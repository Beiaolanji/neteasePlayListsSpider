# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from netease.get_list import search
from .models import *


class GetList(APIView):
    def get(self, request):
        search(request.GET.get('key_word'))
        return Response({})


class PlayLists(APIView):
    def get(self, request, pl_id=-1):
        if pl_id == -1:
            data = [i.get_dict() for i in PlayList.objects.all().order_by('id')]
            return Response(data)
        else:
            data = PlayList.objects.get(id=pl_id).get_dict()
            return Response(data)

    def post(self, request):
        pl = PlayList()
        # https://music.163.com/song/media/outer/url?id=1334780717.mp3
        url = "https://music.163.com/song/media/outer/url?id=" + request.POST.get('url_id') + ".mp3"
        if not PlayList.objects.filter(url=url):
            pl.name = request.POST.get('name')
            pl.url = url
            pl.time = request.POST.get('time')
            pl.comment = request.POST.get('comment')
            if request.POST.get('singer_name'):
                sn, t = Singer.objects.get_or_create(name=request.POST.get('singer_name'))
            else:
                sn = None
            pl.singer = sn
            if request.POST.get('album_name'):
                an, t = Album.objects.get_or_create(name=request.POST.get('album_name'))
            else:
                an = None
            pl.album = an
            pl.save()
            return Response({}, status=201)
        else:
            return Response({}, status=400)

    def put(self, request):
        url = "https://music.163.com/song/media/outer/url?id=" + request.POST.get('url_id') + ".mp3"
        pl = PlayList.objects.get(id=request.POST.get('id'))
        pl.name = request.POST.get('name')
        pl.url = url
        pl.comment = request.POST.get('comment')
        if request.POST.get('singer_name'):
            sn, t = Singer.objects.get_or_create(name=request.POST.get('singer_name'))
        else:
            sn = None
        pl.singer = sn
        if request.POST.get('album_name'):
            an, t = Album.objects.get_or_create(name=request.POST.get('album_name'))
        else:
            an = None
        pl.album = an
        pl.save()
        return Response({}, status=201)

    def delete(self, request):
        pl = PlayList.objects.get(id=request.POST.get('id'))
        pl.delete()
        return Response({}, status=204)
