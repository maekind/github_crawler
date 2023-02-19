#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main file for launching our bot """
import argparse
import json
import sys
import logging
from src.crawler import Crawler
from src.logger import Logger

__application_name__ = "Github crawler"


def configure_logger(verbose, console):
    """ Method for configuring default logging options """
    log_level = logging.INFO if not verbose else logging.DEBUG
    log_file = f'{__application_name__.replace(" ", "").lower()}.log'

    return Logger.get_logger(__application_name__,
                             log_level,
                             log_file, 
                             console)


def get_arguments(): # pragma: no cover
    """ Method to retrieve application arguments """
    # Configure arguments
    parser = argparse.ArgumentParser(description=__application_name__)
    parser.add_argument('-v',
                        '--verbose',
                        help="Set verbose option",
                        dest="verbose",
                        required=False,
                        action='store_true')
    parser.add_argument('-i',
                        '--input',
                        help="Json input file with search options",
                        dest='input_file',
                        metavar='STRING',
                        required=True)
    parser.add_argument('-o',
                        '--ouput',
                        help="File name to store the results",
                        dest='output_file',
                        metavar='STRING',
                        required=False)
    parser.add_argument('-c',
                        '--console-logging',
                        help="Set console logging option",
                        dest="console",
                        required=False,
                        action='store_true')
    
    return parser


def exit_with_errors(logger, error): # pragma: no cover
    """ Method to log the last error and exit the application with value 1 """
    logger.error(error)
    sys.exit(1)


def main():
    """ Main method """
    search_options = {}

    # Get application arguments
    parser = get_arguments()
    args = parser.parse_args()

    # Input argument is mandatory
    if args.input_file is None:
        parser.print_help()
        sys.exit(1)

    # Get verbose argument if passsed
    verbose = True if args.verbose else False

    # Get console argument if passed
    console = True if args.console else False

    # Configure logger
    logger = configure_logger(verbose, console)

    try:
        # Get search options from file
        with open(args.input_file, "r") as json_file:
            logger.debug("Load json input")
            search_options = json.load(json_file)

        # Run bot
        bot = Crawler(name=__application_name__, search=search_options)
        bot.run()

        # Print results
        pretty_results = json.dumps(bot.results, indent=4)
        print(bot.results)
        print(pretty_results)

        # Save results in to the ouput file if given as parameter
        if args.output_file:
            with open(args.output_file, "w+") as output_file:
                output_file.write(pretty_results)

    # Global catching exceptions because we catch and raise specific exceptions
    # in each class.
    except Exception as error:
        exit_with_errors(logger, error)

    # Exit the application with success
    sys.exit(0)


if __name__ == '__main__':
    main()
