from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def ice_break_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)

    linkedin_data = scrape_linkedin_profile(linkedin_profile=linkedin_username)

    summary_template = """
            given the information {information} about a person, create:
            1. a very short summary
            2. a very short two interesting facts about them
        """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        # api_key=os.getenv("OPENAI_API_KEY"), // optional
        temperature=0,
    )
    chain = summary_prompt_template | llm | StrOutputParser()

    response = chain.invoke(input={"information": linkedin_data})
    return response

if __name__ == "__main__":
    load_dotenv()
    output = ice_break_with(name="Eden Marco Udemy")
    print(output)
