
from PIL import Image
import io
from django.conf import settings
import os
from django.core.mail import send_mail
import csv
import boto3
# from apps.services import mailer
from apps.users import models as UserModels
from decouple import config
from huey import RedisHuey, crontab
from apps.recipes.mailer import SoleEmailer

huey = RedisHuey()


huey = RedisHuey('crontab', host='redis://127.0.0.1:6379/')

@huey.task()
def reduce_recipe_image_size(image_path):
    """
    Asynchronous task to reduce the size of recipe images.
    """
    full_path = os.path.join(settings.MEDIA_ROOT, image_path)
    try:
        with Image.open(full_path) as img:
            img = img.convert('RGB')  
            img.thumbnail((800, 800)) 
            img.save(full_path, optimize=True, quality=70)  
    except Exception as e:
        print(f"Error resizing image: {e}")
    
@huey.periodic_task(crontab(day_of_week=0, hour=0, minute=0))
def export_user_data_to_s3():

    users = UserModels.User.objects.all().values('id', 'username', 'email', 'date_joined')  

    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=['id', 'username', 'email', 'date_joined'])
    writer.writeheader()
    writer.writerows(users)

    # Save CSV to S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config(""),
        aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
        region_name=config("AWS_S3_REGION_NAME") 
    )

    s3_client.put_object(
        Bucket=config("AWS_STORAGE_BUCKET_NAME"),
        Key='weekly_exports/user_data.csv',
        Body=csv_buffer.getvalue(),
        ContentType='text/csv'
    )
    return "User data uploaded to S3 successfully!"




  