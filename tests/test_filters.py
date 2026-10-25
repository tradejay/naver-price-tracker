"""
Unit tests verifying domain-rule noise filtering and classification exceptions.
"""
import pytest
from filters.cleaner import check_service_or_accessory, is_valid_main_product
from filters.classifier import classify_product

def test_filter_installation_service_noise():
    # Should flag installation fees as service noise
    assert check_service_or_accessory("로지텍 랠리바 기본설치비 수도권") == "service"
    assert check_service_or_accessory("화상회의 솔루션 전문 엔지니어 출장비") == "service"
    assert check_service_or_accessory("벽면 타공 및 천장 시공비 옵션") == "service"

def test_filter_accessory_noise():
    # Should flag mounts and cables as accessory noise
    assert check_service_or_accessory("로지텍 랠리 확장 마이크 케이블 키트") == "accessory"
    assert check_service_or_accessory("Rally Bar 전용 TV 마운트 브라켓") == "accessory"
    assert check_service_or_accessory("MeetUp 전용 리모컨 단품") == "accessory"

def test_cart_stand_exception_rule():
    # Dedicated Stand/Cart (952-000251) must NOT be filtered out as low-cost mount
    cart_title = "로지텍 랠리보드 65 카트 스탠드 (952-000251)"
    assert check_service_or_accessory(cart_title) is False
    assert classify_product(cart_title) == "Rally Board 65 Cart"
    assert is_valid_main_product(cart_title, price=3500000, min_threshold=2810000) is True

def test_main_hardware_classification():
    assert classify_product("로지텍 MeetUp 2 올인원 컨퍼런스캠") == "Meetup 2"
    assert classify_product("Logitech Rally Bar White 화이트 화상회의") == "Rally Bar"
    assert classify_product("로지텍 Tap IP 터치 컨트롤러 백색") == "TAP IP"
    assert classify_product("알 수 없는 임의의 웹캠") == "Others"
