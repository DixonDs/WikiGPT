#!/usr/bin/env python3
import argparse
import logging

import pywikibot
import tiktoken

from wikigpt.config import Config
from wikigpt.lead_section_creator import LeadSectionCreator
from wikigpt.openai_chatbot import OpenAIChatbot
from wikigpt.page_splitter import PageSplitter


def parse_arguments():
    parser = argparse.ArgumentParser(description='Improve an article from Wikipedia.')
    parser.add_argument('title', type=str, help='name of the Wikipedia article to retrieve')
    parser.add_argument('--lang', type=str, default='en',
                        help='language code for the Wikipedia version to use (default: "en")')
    return parser.parse_args()


def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)

    args = parse_arguments()
    site = pywikibot.Site(args.lang, 'wikipedia')
    page = pywikibot.Page(site, args.title)

    config = Config()
    openai = OpenAIChatbot(config)
    tokenizer = tiktoken.get_encoding("cl100k_base")
    splitter = PageSplitter(max_tokens=1000, tokenizer=tokenizer)

    creator = LeadSectionCreator(config, openai, splitter)
    creator.create(page)


if __name__ == '__main__':
    main()
