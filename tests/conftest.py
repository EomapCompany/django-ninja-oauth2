import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import jwt
import pytest

ROOT = Path(__file__).parent.parent.resolve()

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests/demo_project"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

import django  # noqa
from ninja_oauth2.security.oauth2 import OAuth2AuthorizationCodeBearer  # noqa

django.setup()


def pytest_generate_tests(metafunc):
    os.environ["NINJA_SKIP_REGISTRY"] = "yes"


@pytest.fixture
def test_base_path():
    return Path(__file__).parent.resolve()


@pytest.fixture()
def private_pem_key(test_base_path):
    with Path.open(Path(test_base_path, "data/auth/private_key.txt")) as fobj:
        data = fobj.read()

    return data.encode("utf-8")


@pytest.fixture()
def public_pem_key(test_base_path):
    with Path.open(Path(test_base_path, "data/auth/public_key.txt")) as fobj:
        data = fobj.read()

    return data.encode("utf-8")


@pytest.fixture()
def oauth2_token(private_pem_key):
    expiry = datetime.now() + timedelta(minutes=5)
    payload = {
        "name": "Max Mustermann",
        "preferred_username": "max",
        "given_name": "Max",
        "family_name": "Mustermann",
        "email": "max@mustermann.de",
        "resource_access": {"test": {"roles": ["full-access"]}},
        "exp": expiry,
        "aud": "account",
    }
    return jwt.encode(payload, private_pem_key, algorithm="RS256")
