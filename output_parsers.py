from langchain.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field
from typing import List


class PersonData(BaseModel):
    summary: str = Field(description="Summary of the person")
    facts: List[str] = Field(description="Interesting facts about the person")
    topics_of_interests: List[str] = Field(
        description="Topics the person find interesting"
    )
    ice_breakers: List[str] = Field(
        description="Create ice breakers to open a conversation"
    )

    def to_dict(self):
        return {
            "summary": self.summary,
            "facts": self.facts,
            "topics_of_interest": self.topics_of_interests,
            "icebreakers": self.ice_breakers,
        }


personData_parser = PydanticOutputParser(pydantic_object=PersonData)
