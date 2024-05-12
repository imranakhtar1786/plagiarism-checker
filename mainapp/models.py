from django.db import models

class UserAccount(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    username=models.CharField(max_length=30)
    email=models.EmailField(max_length=30,unique=True)
    phone=models.CharField(max_length=15,default="")
    otp=models.IntegerField(default=None,blank=True,null=True)
    def __str__(self):
        return str(self.id)+" / "+self.name+" / "+self.username
