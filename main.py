from typing import Tuple

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary

def describe_linkedin_profile(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)

    linkedin_data = scrape_linkedin_profile(linkedin_profile=linkedin_username)

    summary_template = """
            given the information {information} about a person, create:
            1. a very short summary
            2. a very short two interesting facts about them
            \n {format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        # api_key=os.getenv("OPENAI_API_KEY"), // optional
        temperature=0,
    )
    # chain = summary_prompt_template | llm | StrOutputParser()
    # chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    chain = summary_prompt_template | llm | summary_parser # langchain expression language

    response:Summary = chain.invoke(input={"information": linkedin_data})
    return response, linkedin_data.get("profile_photo")


if __name__ == "__main__":
    load_dotenv()
    output, profile_pic_url = describe_linkedin_profile(name="Anshul Choudhary Optum Chegg")
    print(output)
