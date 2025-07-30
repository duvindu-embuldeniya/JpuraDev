from django.db.models.signals import post_save, post_delete
from . models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender = User)
def create_profile(sender,instance,created,*args,**kwargs):
    if created:
        created_user = instance
        Profile.objects.create(
            user = created_user
        )

    subject = "Welcome"
    message = "We are glad you are here!"

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [instance.email],
        fail_silently=False,
    )


@receiver(post_delete, sender = Profile)
def delete_user(sender,instance,*args,**kwargs):
    deleted_user = instance
    deleted_user.user.delete()



# post_save.connect(create_profile, sender=User)
# post_delete.connect(delete_user, sender = Profile)