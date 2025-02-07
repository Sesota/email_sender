import re
from itertools import batched

from beanie import Document
from pydantic import BaseModel, Field, HttpUrl, computed_field, field_validator


class Address(BaseModel):
    name: str
    affiliation: str | None = None
    email: str


def structure_address(in_: str) -> Address:
    ret = []
    in_: str = in_.replace("& amp;", "&")
    in_: str = in_.strip("; ")
    # for name, affiliation, email in batched(in_.split("; "), 3):
    #     email = email.replace("email: ", "")
    #     ret.append(
    #         Address(
    #             name=name,
    #             affiliation=affiliation or None,
    #             email=email,
    #         )
    #     )
    # return ret


class Doc(Document):
    class Settings:
        name = "docs"

    authors: list[str] = Field(default_factory=list, alias="Authors")
    title: str = Field(alias="Title")
    year: int = Field(alias="Year")
    citations: int = Field(alias="Cited by")
    link: HttpUrl = Field(alias="Link")
    affiliations: list[str] = Field(default_factory=list, alias="Affiliations")
    abstract: str = Field(alias="Abstract")
    author_kws: list[str] = Field(default_factory=list, alias="Author Keywords")
    index_kws: list[str] = Field(default_factory=list, alias="Index Keywords")
    # address: list[Address] = Field(default_factory=list, alias="Correspondence Address")
    address: str | None = Field(None, alias="Correspondence Address")

    @field_validator(
        "authors", "affiliations", "author_kws", "index_kws", mode="before"
    )
    def split_semicolon(cls, v: str) -> list[str]:
        return v.split("; ")

    # @field_validator("address", mode="before")
    # def structure_address_field(cls, v: str | None) -> list[Address]:
    #     if v is None:
    #         return []
    #     return structure_address(v)

    @computed_field
    def emails(self) -> list[str]:
        EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        ret = self.address
        # for v in self.authors + self.affiliations:
        #     for w in v.split():
        #         ret = ret.replace(w, "")

        # ret = ret.replace("email: ", "")
        # ret = ret.strip("; ")
        # return ret
        # return re.findall(rf'ema?il: ({EMAIL_REGEX})(?:; )?', ret)
        return re.findall(rf"({EMAIL_REGEX})(?:; )?", ret)

    @computed_field
    def persons(self) -> list[Address]:
        return [
            Address(name=author, affiliation=aff, email=email)
            for author, aff, email in zip(self.authors, self.affiliations, self.emails)
        ]
