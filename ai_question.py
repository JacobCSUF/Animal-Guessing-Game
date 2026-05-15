from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List


class AnimalQuestion(BaseModel):
    animal: str = Field(description="Name of the Animal")
    question: str = Field(description="Question used to describe animal")

class Animals(BaseModel):
    list1: List[AnimalQuestion]


def get_top8_questions(ani: List[str] = ["dog", "cat", "cow", "pig", "chicken", "sheep", "rabbit", "horse"]):
    prompt = """
    Given a list of 8 animals return each animal and a yes/no question that strongly 
    distinguishes it from everyone else and is easy to answer for kids.
    Make sure its most obvious trait or even a play on words like: 
    Does it rhyme with dog. Or is it mans best friend.
    Or for pufferfish you could say does it puff up
    Make sure its super easy to answer assuming the person can't 
    view the animal and doesn't know much about the animal
    """

    client = OpenAI()

    response = client.beta.chat.completions.parse(
        model="gpt-5.4-nano",
        messages=[
            {"role": "user", "content": prompt + str(ani)}
        ],
        response_format=Animals,
    )

    questions: Animals = response.choices[0].message.parsed

    return_array = []
    for i in questions.list1:
        return_array.append({"animal": i.animal, "question": i.question})

    return return_array


if __name__ == "__main__":
    print(get_top8_questions())