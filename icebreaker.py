from typing import Tuple
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
from agents.lookup_agent import linkedin_lookup
from helper.scraper import scrape_linkedin
from output_parsers import (
    personData_parser,
    PersonData,
)

load_dotenv()


def ice_break(name: str) -> Tuple[PersonData, str]:
    linkedin_profile_url = linkedin_lookup(name=name)
    summary_template = """
       given the linkedin information {information} about a person from I want you to create:
       1. a short summary
       2. two interesting facts about them
       3. A topic that may interest them
       4. 2 creative icebreakers to open a conversation with them
        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": personData_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_data = scrape_linkedin(linkedin_profile_url=linkedin_profile_url)

    result = chain.run(information=linkedin_data)
    print(result)
    print(personData_parser.parse(result))
    print(linkedin_data.get("profile_pic_url"))
    return personData_parser.parse(result), linkedin_data.get("profile_pic_url")
