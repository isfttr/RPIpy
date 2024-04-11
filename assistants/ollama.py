import os
import sys
import subprocess

from langchain_community.llms import Ollama
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Define your desired data structure.
class Country(BaseModel):
    capital: str = Field(description="capital of the country")
    name: str = Field(description="name of the country")


# Update the model name to use Ollama
OLLAMA_MODEL = "llama2"

PROMPT_COUNTRY_INFO = """
    Provide information about {country}.
    {format_instructions}
    """

def main():
    # Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=Country)

    # setup the chat model
    llm = Ollama(model=OLLAMA_MODEL)
    message = HumanMessagePromptTemplate.from_template(
        template=PROMPT_COUNTRY_INFO,
    )
    chat_prompt = ChatPromptTemplate.from_messages([message])

    # get user input
    country_name = input("Enter the name of a country: ")

    # generate the response
    print("Generating response...")
    chat_prompt_with_values = chat_prompt.format_prompt(
        country=country_name, format_instructions=parser.get_format_instructions()
    )
    output = subprocess.run(["docker", "run", "-i", "your_docker_image"], input=chat_prompt_with_values.to_messages(), stdout=subprocess.PIPE)
    country = parser.parse(output.stdout.decode())

    # print the response
    print(f"The capital of {country.name} is {country.capital}.")

if __name__ == "__main__":
    main()