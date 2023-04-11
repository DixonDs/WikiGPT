import os

import pywikibot
from pywikibot import textlib

from wikigpt.config import Config
from wikigpt.openai_chatbot import OpenAIChatbot
from wikigpt.page_splitter import PageSplitter


class LeadSectionCreator:
    def __init__(self, config: Config, openai: OpenAIChatbot, splitter: PageSplitter):
        self.config = config
        self.openai = openai
        self.splitter = splitter

    def create(self, page: pywikibot.Page):
        text = page.text

        sections = textlib.extract_sections(page.text, page.site)
        lead_section = sections.header

        prompt_template = self._read_prompt_template()

        article_parts = self.splitter.split(text)

        for i, part in enumerate(article_parts):
            prompt = prompt_template.format(title=page.title(), lead_section=lead_section, part_number=i+1,
                                            total_parts=len(article_parts), part=part)
            lead_section = self.openai.complete(prompt)

        draft_path = self._store_draft(page, lead_section)

        pywikibot.output(f"Draft lead section saved to {draft_path}")

        return lead_section

    def _read_prompt_template(self):
        prompt_template_path = os.path.join(self.config.prompts_directory, f"generate_lead.txt")
        with open(prompt_template_path, "r", encoding='utf-8') as f:
            prompt_template = f.read()
        return prompt_template

    def _store_draft(self, page: pywikibot.Page, generated_lead: str):
        drafts_directory = os.path.join(self.config.drafts_directory, page.title())
        os.makedirs(drafts_directory, exist_ok=True)
        draft_path = os.path.join(self.config.drafts_directory, f"{page.title()}.txt")

        with open(draft_path, "w", encoding='utf-8') as f:
            f.write(generated_lead)

        return draft_path
