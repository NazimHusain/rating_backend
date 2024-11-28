from django.core.mail import send_mail
from django.core.mail import EmailMessage
# from decouple import config
from apps.users import models as UserModels
from huey import RedisHuey, crontab

huey = RedisHuey()

class SoleEmailer():
    """ Base Class for sending mail"""

    def _send_mail(self: "SoleEmailer", to_email: str, subject: str, message: str) -> None:
        """ Base method to send basic email"""
        send_mail(
            subject,
            message,
            'nazimhusain325@gmail.com',
            [to_email],
            fail_silently=False,
        )



    def send_daily_emails(self: "SoleEmailer", user_email: str) -> None:
        users = UserModels.User.objects.all()
        for user in users:
            subject = "mail"
            message = "Sending Mail daily exept saturday  and sunday."
            self._send_mail(user.email, subject, message)
            return user_email
        
    @huey.periodic_task(crontab(hour=6, minute=0, day_of_week="1-5"))
    def send_daily_emails(self):
        """Sends daily emails except Saturday and Sunday"""
        users = UserModels.User.objects.all()
        for user in users:
            subject = "Daily Email"
            message = "Sending Mail daily except Saturday and Sunday."
            self._send_mail(user.email, subject, message)


    
    
    
    
   