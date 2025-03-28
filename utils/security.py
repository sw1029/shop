import re
from flask import request

def validate_username(username: str) -> bool:
    """
    사용자 이름은 영문자, 숫자, 언더스코어 포함 3~20자
    """
    return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

def validate_password_strength(password: str) -> bool:
    """
    비밀번호는 최소 6자 이상
    """
    return len(password) >= 6

def get_client_ip() -> str:
    """
    사용자의 실제 IP 주소 반환 (프록시 환경 고려)
    """
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

def sanitize_input(text: str) -> str:
    """
    간단한 XSS 방지를 위한 입력 필터링
    """
    return (text
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;")
            .replace("'", "&#x27;")
            .replace("/", "&#x2F;"))
