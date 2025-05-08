from pm import PromptManager
from prompt import (
    GENERATE_TITLE_PROMPT,
    GENERATE_SECTIONS_PROMPT,
    GENERATE_CONTENT_PROMPT,
)

## Generate Blog.

## Write a blog about "LLM for day-to-day task".

## ------
## - Generate Title
## - Generate Sections
## - Each Section, write content
## - Recheck the cohesion
## ------


class GenerateBlog:
    def __init__(self, topic):
        self.topic = topic
        self.sections = ""

    def generate_title(self):
        pm = PromptManager()
        pm.add_message("system", GENERATE_TITLE_PROMPT.format(topic=self.topic))
        pm.add_message("user", "Generate the title for blog.")
        return pm.generate()

    def generate_sections(self):
        pm = PromptManager()
        pm.add_message("system", GENERATE_SECTIONS_PROMPT.format(topic=self.topic))
        pm.add_message("user", "Generate the blog section!")
        return pm.generate()

    def generate_content(self, section_title):
        pm = PromptManager()
        pm.add_message(
            "system", GENERATE_CONTENT_PROMPT.format(section_title=section_title)
        )
        pm.add_message("user", "Generate the content based on section title")
        return pm.generate()


def generate_blog():
    client = GenerateBlog("Why learning python is important for developer")

    title = client.generate_title()
    sections = client.generate_sections()

    print(title)
    print(sections)


if __name__ == "__main__":
    generate_blog()
