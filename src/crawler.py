#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Github crawler for retrieving information about
    repositories, wikis or issues """

import logging
import random
from urllib.parse import urljoin
import re
import requests
from bs4 import BeautifulSoup


class Crawler:
    """ Main class for crawler implementation """

    SEARCH_TYPES = ["Repositories", "Wikis", "Issues"]
    GITHUB_URL = "https://github.com/search?q={search}&type={type}"
    PARSE_CRITERIAS = {
        "repositories": {
            "select": "ul.repo-list>li:has(a.v-align-middle[href])",
            "select_one": "a.v-align-middle[href]"
        },
        "wikis": {
            "select": "div.hx_hit-wiki:has(a.Link--muted.text-small.text-bold[href])",
            "select_one": "a.Link--muted.text-small.text-bold[href]"
        },
        "issues": {
            "select": "div.issue-list-item:has(a.Link--muted.text-bold[href])",
            "select_one": "a.Link--muted.text-bold[href]"
        }
    }

    def __init__(self, name, search, timeout=10000):
        """ Default constructor """

        # Search parameters initialization
        try:
            self._keywords = search["keywords"]
            self._proxies = search["proxies"]
            # I assume that if a non defined type is passed, we retrieve repositories informations.
            # As it works if we launch a search query with a non existant type directly in to the
            # browser. i.e. https://github.com/search?q=openstack&type=jonhdoe
            self._type = search["type"] if search["type"] in self.SEARCH_TYPES else "Repositories"
        except KeyError as error:
            raise KeyError(f"Key not found: {error}") from error

        # Initialize crawler name
        self._name = name

        # Configure logger
        self._logger = logging.getLogger(self._name)

        # Configure default timeout
        self._timeout = timeout

        # Initialize of the results lists
        self._results = []

    def run(self):
        """ Launch crawl process """
        self._logger.info('Start crawling')
        self._logger.debug(f'keywords: {self._keywords}')
        self._logger.debug(f'type: {self._type}')

        html = self._download_search_results()

        if html:
            self._results = self._get_data(html)

    @property
    def results(self):
        """ Property results """
        return self._results

    def __str__(self):
        """ String class representation """
        return self._name

    def _download_search_results(self):
        """ Returns the content of the url """
        try:
            self._logger.info("Get random proxy from given list")
            proxy = self._get_random_proxy()
            self._logger.debug(f'Selected proxy: {proxy}')

            self._logger.info("Get results")

            response = requests.get(
                self.GITHUB_URL.format(
                    search="+".join(self._keywords), type=self._type),
                timeout=self._timeout,
                proxies={"http": proxy})

            response.raise_for_status()

            return response.text

        except requests.exceptions.HTTPError as error:
            self._logger.error(f'{error}-Status code {response.status_code}')
            raise error
        except requests.exceptions.Timeout:
            self._logger.error("Url request timeout!")
        except ValueError as error:
            self._logger.error(error)
            raise error

    def _get_data(self, html):
        """ Check for other linked urls and yields one by one """
        self._logger.info("Retrieve data from raw html")
        soup = BeautifulSoup(html, 'html.parser')

        results = []
        # We get the details for each result
        for url in self._get_links(soup,
                                   self.PARSE_CRITERIAS.get(
                                       self._type.lower())["select"],
                                   self.PARSE_CRITERIAS.get(self._type.lower())["select_one"]):
            results_dic = {}
            results_dic.update({"url": url})
            extra_dic = {}
            # Get extra data for repos
            if self._type.lower() == "repositories":
                owner, languages = self._get_details_from_link(url)

                if owner:
                    extra_dic.update({"owner": owner})

                if languages:
                    extra_dic.update({"language_stats": languages})

            if extra_dic:
                results_dic.update({"extra": extra_dic})

            results.append(results_dic)

        return results

    def _get_links(self, soup, select_criteria, select_one_criteria):
        """ Method for gathering links from the search result given searching critterias 
        depending of the search type """

        for repo in soup.select(select_criteria):
            link = repo.select_one(select_one_criteria)
            if link and link.get('href').startswith('/'):
                repo_url = urljoin("https://github.com", link.get('href'))
                self._logger.debug(repo_url)
                yield repo_url

    def _get_details_from_link(self, link):
        """ Method to get extra data from a repo link """
        self._logger.info("Get extra data")

        try:
            self._logger.info("Get random proxy from given list")
            proxy = self._get_random_proxy()
            self._logger.debug(f'Selected proxy: {proxy}')

            # Send request to get html from repo link
            response = requests.get(
                link,
                timeout=self._timeout,
                proxies={"http": proxy})

            response.raise_for_status()

            self._logger.info("Retrieve data from raw html")
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get extra languages
            languages = self._extract_most_used_languages(soup)

            # Get extra repo owner
            owner = self._extract_owner(soup)

            return owner, languages

        except requests.exceptions.HTTPError as error:
            self._logger.error(f'{error}-Status code {response.status_code}')
            raise error
        except ValueError as error:
            self._logger.error(error)
            raise error
        except requests.exceptions.Timeout:
            self._logger.error("Url request timeout!")

    def _extract_most_used_languages(self, soup):
        """ Method to extrac the most used languages from the repo link """
        # Initialize languages dictionary
        languages = {}

        for languages_list in soup.select("ul.list-style-none>li:has(span.color-fg-default.text-bold.mr-1)"):
            # Get language
            language = languages_list.select_one(
                'span.color-fg-default.text-bold.mr-1').text

            # Get percentage of use
            for span in languages_list.find_all("span"):
                if '%' in span.text:
                    languages.update(
                        {language: float(span.text.replace("%", ""))})

        return languages

    def _extract_owner(self, soup):
        """ method to extrac owner from the repo link """
        for entry in soup.select("span.author:has(a.url.fn)"):
            class_link = entry.select_one("a.url.fn").text
            if class_link:
                return class_link.replace("\n", "").strip()

    def _get_random_proxy(self):
        """ Method to select a random proxy from the given list. 
            If the proxy list is empty or it does not match with
            the regular expression (ip:port), it raises a ValueException."""

        if self._proxies:
            proxy = random.choice(self._proxies)

            if self._is_proxy(proxy):
                return proxy

            raise ValueError("Proxies list has non-well formed addresses!")

        raise ValueError("Empty proxy list provided!")

    def _is_proxy(self, proxy):
        """ Method to check if the proxy matches the format ip:port """
        regex = r'[0-9]+(?:\.[0-9]+){3}(:[0-9]+)?'

        if proxy is not None and proxy != "":
            return re.match(regex, proxy) is not None

        return False
