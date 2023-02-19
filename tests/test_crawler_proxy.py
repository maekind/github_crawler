#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Tests for crawler proxy methods """
import pytest
from src.crawler import Crawler

proxies = [
        "13.81.217.201:80",
        "117.251.103.186:8080",
        "44.232.253.196:3128"
        ]

search_options = {
    "keywords": [
        "openstack",
        "nova",
        "css"
    ],
    "proxies": proxies,
    "type": ""
}

crawler = Crawler("Crawler test", search_options)


def test_is_proxy_with_port():
    """ Method to check for a well formed proxy string.
    The proxy could be in format ip:port or only the ip """
    assert crawler._is_proxy("192.168.2.1:5021") is True


def test_is_proxy_without_port():
    """ Method to check for a well formed proxy string.
    The proxy could be in format ip:port or only the ip """
    assert crawler._is_proxy("192.168.2.1") is True


def test_is_proxy_with_errors():
    """ Method to check for a well formed proxy string.
    The proxy could be in format ip:port or only the ip """
    assert crawler._is_proxy("192.asd.2.1:5!21") is False


def test_is_proxy_with_none():
    """ Method to check for a well formed proxy string.
    The proxy could be in format ip:port or only the ip """
    assert crawler._is_proxy(None) is False


def test_is_proxy_with_empty_string():
    """ Method to check for a well formed proxy string.
    The proxy could be in format ip:port or only the ip """
    assert crawler._is_proxy("") is False

def test_get_random_proxy_ok():
    """ Method to test getting a random proxy from a proxies list """
    assert crawler._get_random_proxy() in proxies

def test_get_random_proxy_from_empty_list():
    """ Method to test getting a random proxy from a proxies list """
    crawler._proxies = []

    with pytest.raises(ValueError):
        crawler._get_random_proxy()
