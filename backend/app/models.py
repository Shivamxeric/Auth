from django.db import models

# Create your models here.




class Auth(models.Model):
    id = models.AutoField(primary_key=True)         
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'Auth'   # 👈 this is the key


    def __str__(self):
        return self.username
