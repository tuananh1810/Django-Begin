# .\myenv\Scripts\Activate.ps1 (kích hoạt môi trg ảo)
# python manage.py makemigrations (chạy khi sửa models)
# python manage.py migrate (chạy khi sửa models)
# python manage.py runserver 
# python manage.py shell (check admin)  
# from django.contrib.auth.models import User (check admin)
# User.objects.all() (check admin)  exit()




"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
