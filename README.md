# WeShare

> 개인 및 그룹 단위로 물품을 공유하고 관리할 수 있는 서비스

---

## 목차
- [프로젝트 개요](#프로젝트-개요)
- [기술 스택](#기술-스택)
- [주요 기능](#주요-기능)
- [프로젝트 구조](#프로젝트-구조)
- [배포 및 인프라](#배포-및-인프라)
- [API 문서](#api-문서)
- [로컬 실행 방법](#로컬-실행-방법)
- [테스트](#테스트)

---

## 프로젝트 개요

WeShare는 개인 또는 그룹(회사, 동아리 등) 단위로 **물품을 등록, 공유, 대여**할 수 있는 플랫폼입니다.  
- 개인 물품 관리 가능  
- 그룹 단위 물품 관리 가능  
- 다른 사용자/그룹의 물품 대여 기능 구현  

주로 Django와 Django REST Framework를 사용하여 백엔드 API를 구현했습니다.  
ORM 기반 모델 설계와 Serializer를 활용한 데이터 직렬화 경험을 중심으로 작성했습니다.

---

## 기술 스택

### Backend
![Python](https://img.shields.io/badge/Python-3.12.9-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-5.1.6-green?style=flat-square&logo=django)
![DRF](https://img.shields.io/badge/DRF-3.15.2-red?style=flat-square&logo=django)

### Database
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.18-blue?style=flat-square&logo=postgresql)

### Infrastructure
![Nginx](https://img.shields.io/badge/Nginx-1.29.0-lightgrey?style=flat-square&logo=nginx)
![Gunicorn](https://img.shields.io/badge/Gunicorn-23.0.0-orange?style=flat-square)

---

## 주요 기능

### 사용자 관리
- 회원 가입, 로그인, 프로필 관리

### 그룹 관리
- 그룹 생성 및 관리 (회사, 동아리 등)  
- 그룹별 물품 CRUD 기능

### 물품 관리
- CRUD 기능 구현  
- 그룹/개인 물품 구분 가능

### 대여 관리
- 대여 신청 및 상태 관리 (대기, 승인, 반납)

---

## 프로젝트 구조

```
WeShare/
├── apps/
│ ├── users/ # 회원 관리
│ ├── groups/ # 그룹 관리
│ ├── items/ # 물품 관리
│ └── rentals/ # 대여 관리
├── config/
│ └── settings.py
├── manage.py
└── ...
```

---

## 배포 및 인프라
- **서버**: AWS EC2  
- **웹 서버**: Nginx  
- **WSGI 서버**: Gunicorn  
- 로컬 개발에서는 `django-sslserver`를 사용하여 HTTPS 테스트 가능

---

## API 문서

> 전체 API 문서는 서비스 실행 후 아래 URL에서 확인 가능합니다.  

http://localhost:8000/api/docs/

---

## 로컬 실행 방법

1. 가상환경 활성화 (Python 3.12 기준)
```
pyenv activate weshare
의존성 설치

poetry install
마이그레이션 적용

python manage.py migrate
개발 서버 실행

python manage.py runserver

```
이후 브라우저에서 http://localhost:8000/api/docs/ 확인 가능

