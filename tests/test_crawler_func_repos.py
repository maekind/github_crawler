#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Functionnal tests for crawling repositories """
import json
from src.crawler import Crawler


def test_launch_repositories_crawler():
    """ Method to test the functionnal crawler with repositories """
    # Get search options from file
    with open("./tests/repositories.json", "r") as json_file:
        search_options = json.load(json_file)

    # Run bot
    bot = Crawler(name="Test crawler", search=search_options)
    bot.run()

    expected_result = [
        {'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage',
         'extra': {
             'owner': 'atuldjadhav',
             'language_stats': {
                 'CSS': 52.0,
                 'JavaScript': 47.2,
                 'HTML': 0.8
             }
         }
         },
        {'url': 'https://github.com/michealbalogun/Horizon-dashboard',
         'extra': {
             'owner': 'michealbalogun',
             'language_stats': {
                 'Python': 100.0
             }
         }
         }
    ]

    assert bot.results == expected_result


def test_launch_wikis_crawler():
    """ Method to test the functionnal crawler with wikis """
    # Get search options from file
    with open("./tests/wikis.json", "r") as json_file:
        search_options = json.load(json_file)

    # Run bot
    bot = Crawler(name="Test crawler", search=search_options)
    bot.run()

    expected_result = [
        {
            "url": "https://github.com/MirantisDellCrowbar/crowbar"
        },
        {
            "url": "https://github.com/dellcloudedge/crowbar"
        },
        {
            "url": "https://github.com/eryeru12/crowbar"
        },
        {
            "url": "https://github.com/escrevebastante/tongue"
        },
        {
            "url": "https://github.com/jamestyj/crowbar"
        },
        {
            "url": "https://github.com/marcosaletta/Juno-CentOS7-Guide"
        },
        {
            "url": "https://github.com/opencit/opencit"
        },
        {
            "url": "https://github.com/opencit/opencit"
        },
        {
            "url": "https://github.com/vault-team/vault-website"
        },
        {
            "url": "https://github.com/vinayakponangi/crowbar"
        }
    ]

    assert bot.results_sorted_by_url == expected_result


def test_launch_issues_crawler():
    """ Method to test the functionnal crawler with issues """
    # Get search options from file
    with open("./tests/issues.json", "r") as json_file:
        search_options = json.load(json_file)

    # Run bot
    bot = Crawler(name="Test crawler", search=search_options)
    bot.run()

    expected_result = [
        {
            "url": "https://github.com/Cache-Cloud/simple-icons/issues"
        },
        {
            "url": "https://github.com/MOB-atheist/horrible-icons/issues"
        },
        {
            "url": "https://github.com/Rajpratik71/openstack-org/issues"
        },
        {
            "url": "https://github.com/aaronkurtz/gourmand/issues"
        },
        {
            "url": "https://github.com/altai/nova-billing/issues"
        },
        {
            "url": "https://github.com/hellowj/blog/issues"
        },
        {
            "url": "https://github.com/moby/moby/issues"
        },
        {
            "url": "https://github.com/novnc/websockify/issues"
        },
        {
            "url": "https://github.com/sfPPP/openstack-note/issues"
        },
        {
            "url": "https://github.com/suxgkn/myfiles/issues"
        }
    ]

    assert bot.results_sorted_by_url == expected_result
