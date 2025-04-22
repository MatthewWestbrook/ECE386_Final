"""This script evaluates an LLM prompt for processing text so that it can be used for the wttr.in API"""

from ollama import Client
import requests

LLM_MODEL: str = "gemma3:27b"    # Optional, change this to be the model you want
client: Client = Client(
  host='http://ai.dfec.xyz:11434' # URL of the LLM
)
LLM_prompt = """
## Instructions
I need to extract a location based on a question regarding the weather at that location. 
The location can be one of three options: 
1. A city 
2. An airport 
3. a generic location that is NOT a city 

### Notes
If you ever need to use a space, just use a '+' instead
If the location is an airport, return the location as the three letter IATA designation of the airport
If the location is generic and not a city, place a '~' before the answer

### Examples 
'what is the weather at the Eiffel Tower?' will lead to response '~Eiffel+Tower' (option 3)
'I would like to know how warm it is in Colorado Springs' will lead to response 'Colorado+Springs' (option 1)
'I would like to know if it is going to rain at Denver International Airport' which will lead to response 'dia' (option 2)
'What is the weather at Ball Arena?' which will lead to response '~Ball+Arena' (option 3)
'I want to know the weather at The Albuquerque International Sunport' which will lead to response 'abq' (option 2)
'How cold will it be in Seattle?' which will lead to response 'Seattle' (option 1)  

### Additional Information
You will first check to see if the location you extract is a city, if it is not, you will check to see if it is an airport. 
If that is not true, you will then extract just the generic location. 
Reminder that it can only be one of the three cases! 
A response should never end in a '+'. 
Do not say anything else, just say the response I am asking for. 

### Prompt
The prompt you will extract the location from is: 
"""

# voice_to_text = "How chilly is it at the Empire state building?"

def llm_parse_for_wttr(LLM_prompt: str) -> str:

    # formatting for ollama json
    response = client.generate(
        model=LLM_MODEL,
        prompt=LLM_prompt,
        stream=False
    )

    # accessed the response part of the dict
    raw_location = response["response"].strip()

    # adds a tilda because my prompt does not ask for that
    return raw_location
    

# Test cases
test_cases = [ # test cases with ones for wttr.in
    {
        "input": LLM_prompt + "How cold is it at the Charlotte Douglas International Airport this week?",
        "expected": "clt"
    },
    {
        "input": LLM_prompt + "What is the temperature near Stonehenge right now?",
        "expected": "~Stonehenge"
    },
    {
        "input": LLM_prompt + "How warm will it be in Portland?",
        "expected": "Portland"
    },
        {
        "input": LLM_prompt + "How cold is it at the John F. Kennedy International Airport this week?",
        "expected": "jfk"
    },
    {
        "input": LLM_prompt + "What is the temperature near the Taj Mahal right now?",
        "expected": "~Taj+Mahal"
    },
    {
        "input": LLM_prompt + "How warm will it be in Saint Louis?",
        "expected": "Saint+Louis"
    },
]

# Function to iterate through test cases
def run_tests():
    num_passed = 0

    for i, test in enumerate(test_cases, 1):
        raw_input = test["input"]
        expected_output = test["expected"]

        print(f"\nTest {i}: {raw_input}")
        try:
            result = llm_parse_for_wttr(raw_input).strip()
            expected = expected_output.strip()

            print("LLM Output  :", result)
            print("Expected    :", expected)

            if result == expected:
                print("✅ PASS")
                num_passed += 1
            else:
                print("❌ FAIL")

        except Exception as e:
            print("💥 ERROR:", e)

    print(f"\nSummary: {num_passed} / {len(test_cases)} tests passed.")

# Run the test cases
run_tests()