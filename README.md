# RDS-Practice

## EC2

#### 보안 그룹 생성
* `inhatc-X-XX`
* SSH (22)
* HTTP (80)

#### 패키지 설치
```bash
sudo apt update
sudo apt install -y python3-venv postgresql-client git
```

#### 프로젝트
```bash
git clone git@github.com:inhatc-cloudcomputing/RDS-Practice.git
cd RDS-Practice
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## RDS

#### 데이터베이스 생성
* 데이터베이스 생성 방식: `표준 생성`
* 엔진 유형: `PostgreSQL`
* 템플릿: `샌드박스`
* DB 인스턴스 식별자: `inhatc-X-XX-rds`
* 마스터 사용자 이름: `postgres`
* 자격 증명 관리: `자체 관리`
* 마스터 암호 / 확인: 자유롭게
* DB 인스턴스 클래스: `버스터블 클래스(t 클래스 포함)` - `db.t4g.micro`
* 컴퓨팅 리소스: `EC2 컴퓨팅 리소스에 연결 안함`
* Virtual Private Cloud(VPC): `Default VPC`
* DB 서브넷 그룹: `inhatc-X`
* 퍼블릭 액세스: `아니요`
* VPC 보안 그룹(방화벽): 기존 항목 선택
* 기존 VPC 보안 그룹: `inhatc-X-XX-sg`
* 추가 구성 - 초기 데이터베이스 이름: `mydb`

#### 보안 그룹 인바운드 규칙 수정
* PostgreSQL (5432) - 소스: ec2 프라이빗IP/32

## 서비스

#### 서비스 생성
```bash
python manage.py initenv
python manage.py makemigrations
python manage.py migrate
vi .env
```
```dotenv
# /home/ubuntu/RDS-Practice/.env
DJANGO_SECRET_KEY=<SECRET KEY>
DJANGO_DEBUG=False
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD={your password}
DB_HOST={your db endpoint}
DB_PORT=5432
```
```bash
sudo vi /etc/systemd/system/myproject.service
```
```ini
# /etc/systemd/system/myproject.service
[Unit]
Description=Gunicorn daemon for Django project
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/RDS-Practice
EnvironmentFile=/home/ubuntu/RDS-Practice/.env
ExecStart=/home/ubuntu/RDS-Practice/.venv/bin/gunicorn \
          --workers 4 \
          --bind unix:/tmp/myproject.sock \
          conf.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl start myproject.service
sudo systemctl enable myproject.service
```

#### NGINX 설정
```bash
sudo vi /etc/nginx/sites-available/myproject.conf
```
```nginx
# /etc/nginx/sites-available/myproject.conf
server {
    listen 80;
    server_name _;  # Change to EC2 Public IP

    # location /static/ {
    #     alias /home/ubuntu/RDS-Practice/static/;
    # }

    location / {
        include proxy_params;
        proxy_pass http://unix:/tmp/myproject.sock;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/myproject.conf /etc/nginx/sites-enabled/myproject.conf
sudo nginx -t
sudo service nginx restart
```
