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
