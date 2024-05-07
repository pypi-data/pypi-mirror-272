# mypy: disable-error-code="no-any-return,no-untyped-call,no-untyped-def,union-attr"
import sys
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Tuple, Union

from strictdoc.backend.sdoc.document_reference import DocumentReference
from strictdoc.backend.sdoc.models.document import SDocDocument
from strictdoc.backend.sdoc.models.document_grammar import (
    DocumentGrammar,
    GrammarElement,
)
from strictdoc.backend.sdoc.models.object import SDocObject
from strictdoc.backend.sdoc.models.reference import (
    ChildReqReference,
    ParentReqReference,
    Reference,
)
from strictdoc.backend.sdoc.models.section import SDocSection
from strictdoc.backend.sdoc.models.type_system import (
    RESERVED_NON_META_FIELDS,
    ReferenceType,
    RequirementFieldName,
)
from strictdoc.helpers.auto_described import auto_described
from strictdoc.helpers.cast import assert_cast
from strictdoc.helpers.mid import MID


@auto_described
class SDocNodeContext:
    def __init__(self):
        self.title_number_string = None


@auto_described
class SDocNodeField:
    def __init__(
        self,
        parent,
        field_name: str,
        field_value: Optional[str],
        field_value_multiline: Optional[str],
        field_value_references: Optional[List[Reference]],
    ):
        # FIXME: This should be strict_assert at some point.
        assert (
            (field_value is not None and len(field_value) > 0)
            or (
                field_value_multiline is not None
                and len(field_value_multiline) > 0
            )
            or (
                field_value_references is not None
                and len(field_value_references) > 0
            )
        ), "A requirement field must have at least one value."
        self.parent = parent
        self.field_name = field_name

        if field_value_multiline is not None:
            rstripped_field_value_multiline = field_value_multiline.rstrip()

            # Edge case: empty multiline field should have one newline symbol.
            # Example:
            # COMMENT: >>>
            #
            # <<<
            if (
                len(rstripped_field_value_multiline) == 0
                and len(field_value_multiline) != 0
            ):
                field_value_multiline = "\n"
            else:
                field_value_multiline = rstripped_field_value_multiline

        self.field_value_multiline: Optional[str] = field_value_multiline

        self.field_value: Optional[str] = field_value

        self.field_value_references: Optional[List[Reference]] = (
            field_value_references
        )

    def get_value(self):
        value = (
            self.field_value if self.field_value else self.field_value_multiline
        )
        return value


@auto_described
class SDocNode(SDocObject):
    def __init__(
        self,
        parent,
        requirement_type: str,
        mid: Optional[str],
        fields: List[SDocNodeField],
        requirements=None,
    ):
        assert parent
        assert isinstance(requirement_type, str)

        self.parent = parent
        self.requirement_type: str = requirement_type

        references: List[Reference] = []

        ordered_fields_lookup: OrderedDict[str, List[SDocNodeField]] = (
            OrderedDict()
        )

        has_meta: bool = False
        uses_old_refs_field: bool = False
        for field in fields:
            if field.field_name not in RESERVED_NON_META_FIELDS:
                has_meta = True

            if field.field_name == "REFS":
                uses_old_refs_field = True
            elif field.field_name == "RELATIONS":
                field.field_name = "REFS"
                ordered_fields_lookup.setdefault("REFS", []).append(field)
                uses_old_refs_field = False
                continue

            if field.field_name in ("REFS", "RELATIONS"):
                if (
                    field.field_value_references is None
                    or len(field.field_value_references) == 0
                ):
                    print(  # noqa: T201
                        "error: REFS requirement field can only be of "
                        "Reference type. Furthermore: 1) The REFS field is "
                        "deprecated and must be renamed to RELATIONS. "
                        "2) The requirement RELATIONS field shall "
                        "be the last field, after all other fields. "
                        'See the section "Relations" in the user guide for '
                        "more details."
                    )
                    sys.exit(1)
            ordered_fields_lookup.setdefault(field.field_name, []).append(field)

        if RequirementFieldName.REFS in ordered_fields_lookup:
            refs_field: SDocNodeField = ordered_fields_lookup[
                RequirementFieldName.REFS
            ][0]
            if fields.index(refs_field) != (len(fields) - 1):
                print(  # noqa: T201
                    "warning: RELATIONS (previously REFS) requirement field "
                    "should be the last field, after all other fields. "
                    'See the section "Relations" in the user guide for '
                    "more details. "
                    "Correct requirement example:\n"
                    "[REQUIREMENT]\n"
                    "UID: REQ-2\n"
                    "STATEMENT: When Z, the system X shall do Y.\n"
                    "RELATIONS:\n"
                    "- TYPE: Parent\n"
                    "  VALUE: REQ-1"
                )

            references_opt: Optional[List[Reference]] = ordered_fields_lookup[
                RequirementFieldName.REFS
            ][0].field_value_references
            assert references_opt is not None
            references = references_opt

        assert isinstance(references, List)
        self.references: List[Reference] = references

        self.requirements = requirements

        # TODO: Is it worth to move this to dedicated Presenter* classes to
        # keep this class textx-only?
        self.has_meta: bool = has_meta

        self.ng_uses_old_refs_field: bool = uses_old_refs_field

        # This property is only used for validating fields against grammar
        # during TextX parsing and processing.
        self.fields_as_parsed = fields

        self.ordered_fields_lookup: OrderedDict[str, List[SDocNodeField]] = (
            ordered_fields_lookup
        )
        self.ng_level: Optional[int] = None
        self.ng_document_reference: Optional[DocumentReference] = None
        self.ng_including_document_reference: Optional[DocumentReference] = None
        self.ng_line_start: Optional[int] = None
        self.ng_line_end: Optional[int] = None
        self.ng_col_start: Optional[int] = None
        self.ng_col_end: Optional[int] = None
        self.ng_byte_start: Optional[int] = None
        self.ng_byte_end: Optional[int] = None
        self.context = SDocNodeContext()

        self.reserved_mid: MID = MID(mid) if mid is not None else MID.create()
        self.mid_permanent: bool = mid is not None

        # HEF4
        self.ng_resolved_custom_level: Optional[str] = None
        self.custom_level: Optional[str] = None
        if RequirementFieldName.LEVEL in ordered_fields_lookup:
            level = ordered_fields_lookup[RequirementFieldName.LEVEL][
                0
            ].field_value
            self.ng_resolved_custom_level = level
            self.custom_level = level

        # This is always true, unless the node is filtered out with --filter-requirements.
        self.ng_whitelisted = True

        # Cache for accessing the reserved fields values.
        self.ng_reserved_fields_cache: Dict[str, Any] = {}

    @staticmethod
    def get_type_string() -> str:
        return "requirement"

    def get_node_type_string(self) -> Optional[str]:
        return self.requirement_type

    def get_title(self):
        return self.reserved_title

    @property
    def is_root_included_document(self):
        return False

    @property
    def is_root(self) -> bool:
        return self.document.config.root is True

    # Reserved fields

    @property
    def reserved_uid(self) -> Optional[str]:
        return self._get_cached_field(
            RequirementFieldName.UID, singleline_only=True
        )

    @property
    def reserved_status(self) -> Optional[str]:
        return self._get_cached_field(
            RequirementFieldName.STATUS, singleline_only=True
        )

    @property
    def reserved_tags(self) -> Optional[List[str]]:
        if RequirementFieldName.TAGS in self.ng_reserved_fields_cache:
            return self.ng_reserved_fields_cache[RequirementFieldName.TAGS]
        if RequirementFieldName.TAGS not in self.ordered_fields_lookup:
            self.ng_reserved_fields_cache[RequirementFieldName.TAGS] = None
            return None
        field: SDocNodeField = self.ordered_fields_lookup[
            RequirementFieldName.TAGS
        ][0]
        if field.field_value is not None:
            field_value = field.field_value
        else:
            raise NotImplementedError(
                f"Field {RequirementFieldName.TAGS} "
                f"must be a single-line field."
            )
        tags = field_value.split(", ")
        self.ng_reserved_fields_cache[RequirementFieldName.TAGS] = tags
        return tags

    @property
    def reserved_title(self) -> Optional[str]:
        return self._get_cached_field(
            RequirementFieldName.TITLE, singleline_only=True
        )

    @property
    def reserved_statement(self) -> Optional[str]:
        return self._get_cached_field(
            RequirementFieldName.STATEMENT, singleline_only=False
        )

    @property
    def rationale(self) -> Optional[str]:
        return self._get_cached_field(
            RequirementFieldName.RATIONALE, singleline_only=False
        )

    @property
    def comments(self) -> List[str]:
        if RequirementFieldName.COMMENT in self.ng_reserved_fields_cache:
            return self.ng_reserved_fields_cache[RequirementFieldName.COMMENT]
        if RequirementFieldName.COMMENT not in self.ordered_fields_lookup:
            self.ng_reserved_fields_cache[RequirementFieldName.COMMENT] = []
            return []
        comments = []
        for field in self.ordered_fields_lookup[RequirementFieldName.COMMENT]:
            if field.field_value_multiline is not None:
                comments.append(field.field_value_multiline)
            elif field.field_value is not None:
                comments.append(field.field_value)
            else:
                raise NotImplementedError
        self.ng_reserved_fields_cache[RequirementFieldName.COMMENT] = comments
        return comments

    # Other properties
    @property
    def is_requirement(self):
        return True

    @property
    def is_section(self):
        return False

    @property
    def is_composite_requirement(self):
        return False

    @property
    def document(self) -> SDocDocument:
        document: Optional[SDocDocument] = (
            self.ng_document_reference.get_document()
        )
        assert (
            document is not None
        ), "A valid requirement must always have a reference to the document."
        return document

    def get_document(self):
        return self.ng_document_reference.get_document()

    def get_included_document(self):
        return self.ng_including_document_reference.get_document()

    @property
    def parent_or_including_document(self) -> SDocDocument:
        including_document_or_none = (
            self.ng_including_document_reference.get_document()
        )
        if including_document_or_none is not None:
            return including_document_or_none

        document: Optional[SDocDocument] = (
            self.ng_document_reference.get_document()
        )
        assert (
            document is not None
        ), "A valid requirement must always have a reference to the document."
        return document

    def document_is_included(self):
        return self.ng_including_document_reference.get_document() is not None

    def get_requirement_style_mode(self):
        return self.ng_document_reference.get_document().config.get_requirement_style_mode()

    def has_requirement_references(self, ref_type):
        if not self.references or len(self.references) == 0:
            return False
        for reference in self.references:
            if reference.ref_type == ref_type:
                return True
        return False

    def get_requirement_references(self, ref_type) -> List[Reference]:
        if not self.references or len(self.references) == 0:
            return []
        references: List[Reference] = []
        for reference in self.references:
            if reference.ref_type != ref_type:
                continue
            references.append(reference)
        return references

    def get_requirement_reference_uids(
        self,
    ) -> List[Tuple[str, str, Optional[str]]]:
        if not self.references or len(self.references) == 0:
            return []
        references: List[Tuple[str, str, Optional[str]]] = []
        for reference in self.references:
            if reference.ref_type == ReferenceType.PARENT:
                parent_reference: ParentReqReference = assert_cast(
                    reference, ParentReqReference
                )
                references.append(
                    (
                        parent_reference.ref_type,
                        parent_reference.ref_uid,
                        parent_reference.role,
                    )
                )
            elif reference.ref_type == ReferenceType.CHILD:
                child_reference: ChildReqReference = assert_cast(
                    reference, ChildReqReference
                )
                references.append(
                    (
                        child_reference.ref_type,
                        child_reference.ref_uid,
                        child_reference.role,
                    )
                )
        return references

    def get_parent_requirement_reference_uids(
        self,
    ) -> List[Tuple[str, Optional[str]]]:
        if not self.references or len(self.references) == 0:
            return []
        references: List[Tuple[str, Optional[str]]] = []
        for reference in self.references:
            if reference.ref_type != ReferenceType.PARENT:
                continue
            parent_reference: ParentReqReference = assert_cast(
                reference, ParentReqReference
            )
            references.append((parent_reference.ref_uid, parent_reference.role))
        return references

    def get_child_requirement_reference_uids(
        self,
    ) -> List[Tuple[str, Optional[str]]]:
        if not self.references or len(self.references) == 0:
            return []
        references: List[Tuple[str, Optional[str]]] = []
        for reference in self.references:
            if reference.ref_type != ReferenceType.CHILD:
                continue
            child_reference: ChildReqReference = assert_cast(
                reference, ChildReqReference
            )
            references.append((child_reference.ref_uid, child_reference.role))
        return references

    def enumerate_fields(self):
        requirement_fields = self.ordered_fields_lookup.values()
        for requirement_field_list in requirement_fields:
            yield from requirement_field_list

    def enumerate_all_fields(self):
        for field in self.enumerate_fields():
            if field.field_name == "REFS":
                continue
            meta_field_value = (
                field.field_value
                if field.field_value
                else field.field_value_multiline
            )
            yield field, field.field_name, meta_field_value

    def enumerate_meta_fields(
        self, skip_single_lines=False, skip_multi_lines=False
    ):
        element: GrammarElement = self.document.grammar.elements_by_type[
            self.requirement_type
        ]
        grammar_field_titles = list(map(lambda f: f.title, element.fields))
        statement_field_index = grammar_field_titles.index(
            RequirementFieldName.STATEMENT
        )
        for field in self.enumerate_fields():
            if field.field_name in RESERVED_NON_META_FIELDS:
                continue
            meta_field_value = (
                field.field_value
                if field.field_value
                else field.field_value_multiline
            )
            field_index = grammar_field_titles.index(field.field_name)

            # A field is considered singleline if it goes before the STATEMENT
            # field and vice versa.
            if field_index > statement_field_index:
                is_single_line_field = False
            else:
                is_single_line_field = True

            if is_single_line_field and skip_single_lines:
                continue
            if (not is_single_line_field) and skip_multi_lines:
                continue

            field_human_title = element.fields_map[field.field_name]
            yield field_human_title.get_field_human_name(), meta_field_value

    def get_meta_field_value_by_title(self, field_title: str) -> Optional[str]:
        assert isinstance(field_title, str)
        if field_title not in self.ordered_fields_lookup:
            return None
        field: SDocNodeField = self.ordered_fields_lookup[field_title][0]
        meta_field_value_or_none: Optional[str] = (
            field.field_value
            if field.field_value
            else field.field_value_multiline
        )
        assert meta_field_value_or_none
        meta_field_value = meta_field_value_or_none
        return meta_field_value

    def get_field_human_title(self, field_name: str) -> str:
        element: GrammarElement = self.document.grammar.elements_by_type[
            self.requirement_type
        ]
        field_human_title = element.fields_map[field_name]
        return field_human_title.get_field_human_name()

    def get_requirement_prefix(self) -> str:
        parent: Union[SDocSection, SDocDocument] = assert_cast(
            self.parent, (SDocSection, SDocDocument, SDocCompositeNode)
        )
        return parent.get_requirement_prefix()

    def dump_fields_as_parsed(self):
        return ", ".join(
            list(
                map(
                    lambda r: r.field_name,
                    self.fields_as_parsed,
                )
            )
        )

    def _get_cached_field(
        self, field_name: str, singleline_only: bool
    ) -> Optional[str]:
        if field_name in self.ng_reserved_fields_cache:
            return self.ng_reserved_fields_cache[field_name]
        if field_name not in self.ordered_fields_lookup:
            self.ng_reserved_fields_cache[field_name] = None
            return None
        field: SDocNodeField = self.ordered_fields_lookup[field_name][0]

        if field.field_value is not None:
            field_value = field.field_value
        else:
            if singleline_only:
                raise NotImplementedError(
                    f"Field {field_name} must be a single-line field."
                )
            if field.field_value_multiline is not None:
                field_value = field.field_value_multiline
            else:
                raise NotImplementedError(self)
        self.ng_reserved_fields_cache[field_name] = field_value
        return field_value

    # Below all mutating methods.

    def set_field_value(
        self, *, field_name: str, form_field_index: int, value: Optional[str]
    ):
        """
        The purpose of this purpose is to provide a single-method API for
        updating any field of a requirement. A requirement might use only some
        fields of a document grammar, so an extra exercise done by the method is
        to ensure that an added field that has not been attached to the
        requirement before will be put at the right index.
        """
        assert isinstance(field_name, str)

        if field_name in self.ng_reserved_fields_cache:
            del self.ng_reserved_fields_cache[field_name]

        # If a field value is being removed, there is not much to do.
        if value is None or len(value) == 0:
            # Comment is a special because there can be multiple comments.
            # Empty comments are simply ignored and do not show up in the
            # updated requirement.
            if field_name == RequirementFieldName.COMMENT:
                return

            if field_name in self.ordered_fields_lookup:
                del self.ordered_fields_lookup[field_name]
            return

        # If a field value is being added or updated.

        document: SDocDocument = self.document
        grammar_or_none: Optional[DocumentGrammar] = document.grammar
        assert grammar_or_none is not None
        grammar: DocumentGrammar = grammar_or_none

        element: GrammarElement = grammar.elements_by_type[
            self.requirement_type
        ]
        grammar_field_titles = list(map(lambda f: f.title, element.fields))
        # FIXME: This will go away very soon when the RELATIONS become a
        #        separate field in SDoc REQUIREMENT's grammar.
        grammar_field_titles.append("REFS")
        field_index = grammar_field_titles.index(field_name)

        try:
            title_field_index = grammar_field_titles.index(
                RequirementFieldName.TITLE
            )
        except ValueError:
            # It is a rare edge case when a grammar is without a TITLE but if it
            # happens, use STATEMENT as a fallback.
            title_field_index = grammar_field_titles.index(
                RequirementFieldName.STATEMENT
            )

        field_value = None
        field_value_multiline = None
        field_value_references = None
        if field_index <= title_field_index:
            field_value = value
        else:
            field_value_multiline = value

        if field_name in self.ordered_fields_lookup:
            if len(self.ordered_fields_lookup[field_name]) > form_field_index:
                self.ordered_fields_lookup[field_name][form_field_index] = (
                    SDocNodeField(
                        self,
                        field_name=field_name,
                        field_value=field_value,
                        field_value_multiline=field_value_multiline,
                        field_value_references=field_value_references,
                    )
                )
            else:
                self.ordered_fields_lookup[field_name].insert(
                    form_field_index,
                    SDocNodeField(
                        self,
                        field_name=field_name,
                        field_value=field_value,
                        field_value_multiline=field_value_multiline,
                        field_value_references=field_value_references,
                    ),
                )
            return

        new_ordered_fields_lookup = OrderedDict()
        for field_title in grammar_field_titles[:field_index]:
            if field_title in self.ordered_fields_lookup:
                new_ordered_fields_lookup[field_title] = (
                    self.ordered_fields_lookup[field_title]
                )
        new_ordered_fields_lookup[field_name] = [
            SDocNodeField(
                self,
                field_name=field_name,
                field_value=field_value,
                field_value_multiline=field_value_multiline,
                field_value_references=field_value_references,
            )
        ]
        after_field_index = field_index + 1
        for field_title in grammar_field_titles[after_field_index:]:
            if field_title in self.ordered_fields_lookup:
                new_ordered_fields_lookup[field_title] = (
                    self.ordered_fields_lookup[field_title]
                )
        self.ordered_fields_lookup = new_ordered_fields_lookup
        self._update_has_meta()

    def _update_has_meta(self):
        has_meta: bool = False
        for field in self.enumerate_fields():
            if field.field_name not in RESERVED_NON_META_FIELDS:
                has_meta = True
        self.has_meta = has_meta


@auto_described
class SDocCompositeNode(SDocNode):
    def __init__(self, parent, **fields):
        super().__init__(parent, **fields)
        self.ng_document_reference: Optional[DocumentReference] = None
        self.ng_including_document_reference: Optional[DocumentReference] = None
        self.ng_has_requirements = False

    @property
    def is_composite_requirement(self):
        return True

    @property
    def document(self):
        return self.ng_document_reference.get_document()

    def document_is_included(self):
        return self.ng_including_document_reference.get_document() is not None

    def get_requirement_prefix(self) -> str:
        return self.parent.get_requirement_prefix()
