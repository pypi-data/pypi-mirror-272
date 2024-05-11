import re
from contextlib import suppress
from typing import Optional, Union

from pydantic import BaseModel, Field, model_validator

from bigdata.enum_utils import StrEnum

OLDEST_RECORDS = 2000


class ExpressionOperation(StrEnum):
    IN = "in"
    ALL = "all"
    GREATER_THAN = "greater-than"
    LOWER_THAN = "lower-than"
    BETWEEN = "between"


class ExpressionTypes(StrEnum):
    AND = "and"
    OR = "or"
    NOT = "not"
    KEYWORD = "keyword"
    SIMILARITY = "similarity"
    ENTITY = "entity"
    SOURCE = "source"
    TOPIC = "rp_topic"
    LANGUAGE = "language"
    WATCHLIST = "watchlist"
    DATE = "date"
    CONTENT_TYPE = "content_type"
    SENTIMENT = "sentiment"
    SECTION_METADATA = "section_metadata"
    DOCUMENT_TYPE = "document_type"
    REPORTING_PERIOD = "reporting_period"


class SectionTypes(StrEnum):
    MANAGEMENT_DISCUSSION = "Management Discussion Section"
    QA = "qa"
    QUESTION = "question"
    ANSWER = "answer"


class DocumentTypes(StrEnum):
    ANALYST_INVESTOR_SHAREHOLDER_MEETING = "Analyst, Investor and Shareholder meeting"
    """Analyst, Investor and Shareholder meeting"""
    CONFERENCE_CALL = "General Conference Call"
    """General Conference Call"""
    GENERAL_PRESENTATION = "General Presentation"
    """General Presentation"""
    EARNINGS_CALL = "Earnings Call"
    """Earnings Call"""
    EARNINGS_RELEASE = "Earnings Release"
    """Earnings Release"""
    GUIDANCE_CALL = "Guidance Call"
    """Guidance Call"""
    SALES_REVENUE_CALL = "Sales and Revenue Call"
    """Sales and Revenue Call"""
    SALES_REVENUE_RELEASE = "Sales and Revenue Release"
    """Sales and Revenue Release"""
    SPECIAL_SITUATION_MA = "Special Situation, M&A and Other"
    """Special Situation, M&A and Other"""
    SHAREHOLDERS_MEETING = "Shareholders Meeting"
    """Shareholders Meeting"""
    MANAGEMENT_PLAN_ANNOUNCEMENT = "Management Plan Announcement"
    """Management Plan Announcement"""
    INVESTOR_CONFERENCE_CALL = "Investor Conference Call"
    """Investor Conference Call"""


class FiscalQuarterValidator(BaseModel):
    value: int = Field(ge=1, le=4)

    def get_string(self):
        return f"FQ{self.value}"


class FiscalYearValidator(BaseModel):
    value: int = Field(ge=OLDEST_RECORDS)

    def get_string(self):
        return f"{self.value}FY"


class Expression(BaseModel):
    type: ExpressionTypes
    value: Union[list[Union[str, float, "Expression"]], str, float, "Expression"]
    operation: Optional[ExpressionOperation] = None

    @classmethod
    def new(cls, etype: ExpressionTypes, values: Optional[list[str]]) -> "Expression":
        if not values:
            return None
        return cls(type=etype, operation=ExpressionOperation.IN, value=values)


class FileType(StrEnum):
    ALL = "all"
    FILINGS = "filings"
    TRANSCRIPTS = "transcripts"
    NEWS = "news"
    FILES = "files"


class SortBy(StrEnum):
    """Defines the order of the search results"""

    RELEVANCE = "relevance"
    DATE = "date"


class Ranking(StrEnum):
    STABLE = "stable"
    EXPERIMENTAL = "experimental"
    SIMILARITY = "similarity"


class SearchChain(StrEnum):
    DEDUPLICATION = "deduplication"
    ENRICHER = "enricher"  # NO LONGER USED
    DEFAULT = "default"  # NO LONGER USED?
    CLUSTERING = "clustering"


class SearchPagination(BaseModel):
    limit: int = Field(default=100, gt=0, lt=1001)
    cursor: int = Field(default=1, gt=0)


class SearchSharePermission(StrEnum):
    READ = "read"
    UNDEFINED = "undefined"
