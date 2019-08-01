from django.db import models
import re


# Create your models here.

class Singer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="歌手名称", null=True, blank=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "歌手表"
        verbose_name_plural = verbose_name


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="专辑名称", null=True, blank=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "专辑表"
        verbose_name_plural = verbose_name


class PlayList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="歌曲名称", null=True, blank=True)
    url = models.CharField(max_length=30, verbose_name="歌曲链接", null=True, blank=True)
    time = models.CharField(max_length=30, verbose_name="时长", null=True, blank=True)
    comment = models.IntegerField(verbose_name="评论数", null=True, blank=True)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)

    def get_dict(self):
        # if self.singer:
        #     s = self.singer.name
        # else:
        #     s = None
        # if self.album:
        #     a = self.album.name
        # else:
        #     a = None
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'time': self.time,
            'comment': self.comment,
            'singer': self.singer.name if self.singer else None,
            'album': self.album.name if self.album else None,
            'url_id': re.search("[0-9]{4,11}", self.url).group()
        }

    class Meta:
        ordering = ("-id",)
        verbose_name = "歌曲表"
        verbose_name_plural = verbose_name
