import os
import secrets
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate a .env file with default values and a random Django Secret Key.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', type=str, default='.env',
            help='경로를 지정하면 해당 위치에 .env 파일을 생성합니다 (기본: ./ .env)'
        )

    def handle(self, *args, **options):
        env_path = options['path']

        if os.path.exists(env_path):
            self.stdout.write(self.style.WARNING(f'⚠️ {env_path} 파일이 이미 존재합니다. 덮어쓰지 않습니다.'))
            return

        secret_key = secrets.token_urlsafe(50)

        template = (
            f'DJANGO_SECRET_KEY={secret_key}\n'
            'DJANGO_DEBUG=False\n'
            'DB_NAME=mydb\n'
            'DB_USER=myuser\n'
            'DB_PASSWORD=mypassword\n'
            'DB_HOST=myhost\n'
            'DB_PORT=5432\n'
        )

        with open(env_path, 'w') as f:
            f.write(template)

        self.stdout.write(self.style.SUCCESS(f'✅ {env_path} 파일이 생성되었습니다.'))
        self.stdout.write(f'🔑 Secret Key: {secret_key[:20]}... (생략)')

