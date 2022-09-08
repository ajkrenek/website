from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.forms import TextInput, EmailInput
from ckeditor.fields import RichTextField


import re, random, praw, smtplib, ssl
import urllib.request
from email.message import EmailMessage
from bs4 import BeautifulSoup
reddit = praw.Reddit(client_id=settings.PRAW_CLIENT_ID,
                     client_secret=settings.PRAW_CLIENT_SECRET,
                     password=settings.PRAW_CLIENT_PASSWORD,
                     user_agent=settings.PRAW_USER_AGENT,
                     username=settings.PRAW_CLIENT_USERNAME)



class MailForm(forms.Form):
    Your_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}), max_length=70)
    Your_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' :'Your Email', 'class': 'form-control'}), max_length=70)
    Subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}), max_length=70)
    Tumblr_Key_Word = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tumblr Quote Key Word', 'class': 'form-control'}), max_length=70, required=False)
    subreddit_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subreddit', 'class': 'form-control'}),max_length=20, required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={'style': 'height:215px;', 'placeholder': 'Type your message!', 'class': 'form-control'}))



    def tumblr_url(self):
        cl_data = super().clean()
        tumblr_word = cl_data.get('Tumblr_Key_Word')

        tumblr_url = f'https://www.tumblr.com/search/{tumblr_word}%20quotes?t=1'
        html = urllib.request.urlopen(tumblr_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        some_list = []
        for post in soup.find_all('a', href=True):
                some_list.append(post['href'])


        post_url = re.findall(r'''
        #structure of post url : https://somename.tumblr.com/post/12094812094814/some-post-name
        https?://                      # https part
        (?:[-\w.]|(?:%[\da-fA-F]{2}))+ # name.tumblr part
        /                              # forward slash
        \w+                            #'post'
        /                              # forward slash
        \d+                            # the digits
        /                              # forward slash
        [\w-]*                         # some-post-name
        ''',str(some_list), re.VERBOSE)

        post = random.choice(post_url)
        return post



    def picture_url(self):
        cl_data = super().clean()
        reddit_sub = cl_data.get('subreddit_name')
        if not reddit_sub:
            reddit_sub = 'frogs'
        else:
            reddit_sub = reddit_sub

        url_list = ""
        sub = f"{reddit_sub}"
        subreddit = reddit.subreddit(sub)
        new_subreddit = subreddit.new(limit=20)

        for submission in new_subreddit:
            picture_url = str(submission.url)
            if picture_url.endswith('jpg') or picture_url.endswith('jpeg') or picture_url.endswith('png'):
                url_list += picture_url +'\n'

        url_link = url_list.split()
        random_url = random.choice(url_link)

        return random_url

    def get_info(self):
        cl_data = super().clean()

        tumblr_post = self.tumblr_url()
        reddit_img = self.picture_url()


        name = cl_data.get('Your_name').strip()
        to_email = cl_data.get('Your_email')
        subject = cl_data.get('Subject')
        message = cl_data.get('message')



        return subject, message, to_email, tumblr_post, reddit_img, name



    def send(self):
        subject, message, to_email, tumblr_post, reddit_img, name = self.get_info()
        msg = EmailMessage()
        msg["Subject"] = f"{subject}"
        msg["From"] = settings.EMAIL_HOST_USER
        msg["To"] = f"{to_email}"
        msg.add_alternative("""\
            <html>
                <body>
                    <p> {message} </p>
                    <p> {tumblr_post} </p>
                    <img src = {reddit_img} width="400" height="400"/>
                    <br>
                    from {name}
                </body>
            </html>
        """.format(name=name, message=message, tumblr_post=tumblr_post, reddit_img=reddit_img), subtype = 'html')

        with smtplib.SMTP_SSL("smtp.gmail.com", settings.EMAIL_PORT) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            server.quit()
