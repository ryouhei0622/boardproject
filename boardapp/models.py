from django.db import models

# Create your models here.

class BoardModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    #settingsでアップロードされた画像をどこに保存するのかを指定するなら
    #upload_toはblankで大丈夫
    snsimage = models.ImageField(upload_to='')
    #いいねの数
    good = models.IntegerField(null=True, blank=True, default=1)
    #既読の数
    read = models.IntegerField(null=True, blank=True, default=1)
    #既読した人の名前を保持することによって既読の数の重複を防ぐ
    readtext = models.TextField(null=True, blank=True, default='a')