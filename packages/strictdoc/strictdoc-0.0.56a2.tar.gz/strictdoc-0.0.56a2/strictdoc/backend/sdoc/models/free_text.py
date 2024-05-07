# mypy: disable-error-code="no-untyped-def,type-arg"
import html
from typing import List

from strictdoc.backend.sdoc.models.anchor import Anchor
from strictdoc.backend.sdoc.models.inline_link import InlineLink
from strictdoc.helpers.auto_described import auto_described


@auto_described
class FreeText:
    def __init__(self, parent, parts: List):
        assert isinstance(parts, list)
        self.parent = parent
        self.parts = parts
        self.ng_level = None

    @property
    def parent_or_including_document(self):
        return self.parent.parent_or_including_document

    @property
    def is_requirement(self):
        return False

    @property
    def is_section(self):
        return False

    def get_parts_as_text(self) -> str:
        # [LINK: SECTION-CUSTOM-GRAMMARS]
        text = ""
        for part in self.parts:
            if isinstance(part, str):
                text += part
            elif isinstance(part, InlineLink):
                text += "[LINK: "
                text += part.link
                text += "]"
            elif isinstance(part, Anchor):
                text += "[ANCHOR: "
                text += part.value
                if part.has_title:
                    text += ", "
                    text += part.title
                text += "]"
                text += "\n"
                text += "\n"
            else:
                raise NotImplementedError(part)
        return text

    def get_parts_as_text_escaped(self) -> str:
        return html.escape(self.get_parts_as_text())


class FreeTextContainer(FreeText):
    def __init__(self, parts):
        super().__init__(None, parts)
