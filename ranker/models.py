# Create your models here.
from django.db import models




class fetchinfo(models.Model):
	keyword = models.CharField(max_length=100,help_text='keyword for search',default ="NULL" )
	paperid = models.CharField(max_length=100,help_text='hash of paper',default ="NULL" )
	papername = models.CharField(max_length=500,help_text='Enter name of the paper')
	authors=models.CharField(max_length=500,help_text="Enter names of authors of the paper")
	conference=models.CharField(max_length=100,blank=True,null=True,default="NA")
	rank=models.CharField(max_length=2,blank=True,null=True,default="NA",help_text="Rank of conference")
	citations = models.IntegerField(default = 0)
	infcitations = models.IntegerField(default = 0,help_text = "Influential_citations")
	url = models.URLField(max_length=200, null = True , default = "NA")
	access = models.BooleanField(default = False)
	def __str__(self):
        	return self.papername
        	
class conferencedata(models.Model):
	name = models.CharField(max_length=100,help_text='conference name',default ="NULL" )
	abbrv = models.CharField(max_length=10,help_text='abbreviation',default ="NULL", null=True )
	rank = models.CharField(max_length=3,help_text='abbreviation',default ="NULL" )
	ptype = models.CharField(max_length=20,help_text='abbreviation',default ="NULL" )
	def __str__(self):
        	return self.name + " " +self.rank +" "+ self.ptype	
        	

class Mkeyword(models.Model):
	keyword = models.CharField(max_length=100,help_text='keyword for search',default ="NULL" )
	pages=models.IntegerField(help_text="Pages already seen")
	


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
