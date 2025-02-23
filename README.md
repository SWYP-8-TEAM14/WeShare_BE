> Commit Message Type:

- Feat: 새로운 기능 추가
- Fix: 버그 수정
- Docs: 문서 수정
- Style: 코드 스타일 변경 (코드 포매팅, 세미콜론 누락 등)
- Refactor: 리팩토링
- Test: 테스트 코드 추가 또는 수정
- Rename: 파일 혹은 폴더명 수정
- Remove: 파일 혹은 폴더 삭제

> App Start

```
# Python 3.12 버전을 사용하여 'weshare'라는 이름의 가상환경 생성
pyenv virtualenv 3.12 weshare

# 현재 디렉토리에서 사용할 Python 환경을 'weshare' 가상환경으로 설정
pyenv local weshare

# Poetry를 사용하여 pyproject.toml에 정의된 프로젝트 의존성 설치
poetry install

# Django의 {app_name} 앱에 대해 모델 변경 사항을 감지하고 migration 파일 생성
python manage.py makemigrations {app_name}

# 생성된 migration 파일들을 적용하여 데이터베이스 스키마 업데이트
python manage.py migrate

# Django 개발 서버 실행 (로컬에서 프로젝트 테스트)
python manage.py runserver
```
