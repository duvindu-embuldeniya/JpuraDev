from django.db import models
import uuid
from django.contrib.auth.models import User
# id = models.UUIDField(default=uuid.uuid1, unique=True, primary_key=True, editable=False)
# tag = models.ManyToManyField(Tag, blank=True)

 
 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    short_intro = models.CharField(max_length=30, null=True)
    bio = models.TextField(null=True)
    location = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='uploaded_profile_model/', blank=True, null=True)
    github_url = models.CharField(max_length=200, blank=True, null=True)
    linkedin_url = models.CharField(max_length=200, blank=True, null=True)
    web_url = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"




class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField()
    source_link = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='uploaded_project_model/', blank=True, null=True)
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['-created']
    

    @property
    def update_values(self):
        all_reviews = self.review_set.all()
        all_reviews_count = all_reviews.count()
        up_reviews = all_reviews.filter(value = 'up')
        up_reviews_count = up_reviews.count()

        percentage = (up_reviews_count/all_reviews_count) * 100
        self.vote_total = up_reviews_count
        self.vote_ratio = percentage
        self.save()
    
    @property
    def get_voters(self):
        queryset = self.review_set.all().values_list('owner__id', flat = True)
        return queryset




class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField()
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.body}"[:20]




class Tag(models.Model):
    name = models.CharField(max_length=16)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"



class Skill(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username} - {self.name}"



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.receiver.username}- {self.subject}"
    
    class Meta:
        ordering = ['is_read', '-created']

