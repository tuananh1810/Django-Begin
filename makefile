(kích hoạt môi trg ảo)
.\env\Scripts\Activate.ps1   	  
(chạy khi sửa models)
python manage.py makemigrations 		
python manage.py migrate 
(runserver)		
python manage.py runserver 
(check admin) 
python manage.py shell 			 
from django.contrib.auth.models import User			 
User.objects.all()		 (check admin)  exit()
