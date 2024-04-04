from django.db import models

# Create your models here.
class client(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=50)
    
class Questions(models.Model):
    que = models.CharField( max_length=500)
    option1= models.CharField( max_length=1000)
    option2= models.CharField( max_length=1000)
    option3= models.CharField( max_length=1000)
    option4= models.CharField( max_length=1000)
    
    
class Answer(models.Model):
    client=models.ForeignKey(client, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=50)
    weight = models.IntegerField()
    
class dscore(models.Model):
    client=models.ForeignKey(client, on_delete=models.CASCADE)
    score = models.IntegerField()