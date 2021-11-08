# Create your models here.
from django.db import models

class FrequentPaper(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    papername = models.CharField(max_length=300,help_text='Enter name of the paper')
    authors=models.CharField(max_length=300,help_text="Enter names of authors of the paper")
    conference=models.CharField(max_length=100,blank=True,null=True,default="NA")
    rank=models.CharField(max_length=2,help_text="Rank of conference")
    frequency=models.IntegerField(help_text="Number of times paper was fetched")
    def __str__(self):
        """String for representing the Model object."""
        return self.papername
    class Meta:
        ordering = ['rank','papername']
class NewPaper(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    papername = models.CharField(max_length=300,help_text='Enter name of the paper')
    authors=models.CharField(max_length=300,help_text="Enter names of authors of the paper")
    conference=models.CharField(max_length=100,blank=True,null=True,default="NA")
    rank=models.CharField(max_length=2,help_text="Rank of conference")
    #-----Adding date field-----
    date = models.DateField()
    def __str__(self):
        """String for representing the Model object."""
        return self.papername
    class Meta:
        ordering = ['rank','papername']
