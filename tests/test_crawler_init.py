#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Tests for crawler init method """
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



def test_init_missing_keywords():
    """ Method for testing initialization with missing keywords key """
    search_options.pop("keywords")

    with pytest.raises(KeyError):
        crawler = Crawler("Crawler test", search_options)

def test_init_missing_proxies():
    """ Method for testing initialization with missing proxies key """
    search_options.pop("proxies")

    with pytest.raises(KeyError):
        crawler = Crawler("Crawler test", search_options)

def test_init_missing_type():
    """ Method for testing initialization with missing type key """
    search_options.pop("type")

    with pytest.raises(KeyError):
        crawler = Crawler("Crawler test", search_options)