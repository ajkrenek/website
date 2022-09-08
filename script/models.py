from django.db import models
from django import forms
from ckeditor.fields import RichTextField

# Create your models here.
class Mail(models.Model):
    subject = models.CharField(max_length=200)
    email = forms.EmailField()
    subreddit = models.CharField(max_length=200)
    tumblr = models.CharField(max_length=200)
    message = RichTextField(blank=True, null=True)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('inquiry')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg

    def send(self):

        subject, msg = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )
