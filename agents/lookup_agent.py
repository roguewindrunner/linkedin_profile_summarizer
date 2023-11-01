from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from tools.tools import get_profile_url
from langchain.agents import initialize_agent, Tool, AgentType
import json


def linkedin_lookup(name: str) -> str:
    with open("li_url.json", "r") as file:
        data = json.load(file)

    if name in data:
        print("Name is already searched")
        linkedin_profile_url = data[name]
        return linkedin_profile_url
    else:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

        template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                          Your answer should contain only a URL"""
        tools_for_agent1 = [
            Tool(
                name="Crawl Google to look for linkedin profile page",
                func=get_profile_url,
                description="useful for when you need get the Linkedin Page URL",
            ),
        ]

        agent = initialize_agent(
            tools=tools_for_agent1,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
        prompt_template = PromptTemplate(
            input_variables=["name_of_person"], template=template
        )

        linkedin_profile_url = agent.run(
            prompt_template.format_prompt(name_of_person=name)
        )
        data[name] = linkedin_profile_url
        with open("li_url.json", "w") as f:
            json.dump(data, f)
        return linkedin_profile_url
