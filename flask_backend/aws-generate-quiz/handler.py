import json
import openai

openai_api_key="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"
gpt_model="gpt-4"

def gpt_call(prompt):
    openai.api_key = openai_api_key

    # Generate a response from the model
    response = openai.ChatCompletion.create(
    model=gpt_model,
    temperature=0,
    messages=prompt
    )

    reply = response.choices[0].message.content
    
    return reply


def generate_quiz(manual):
  
  #manual from frontend
#   data = request.json
#   manual = data.get('data')

  langue_prompt="Thai"
  system_template={"role": "system", "content": "Your role is a trainer to help new employees learn their job working.  You generate one multiple-choice quiz question and and create answers to that quiz to train an employee, when given information from the equipment manuals or employee guidebooks.You must answer the questions in"+langue_prompt+"\n"}
  user_template = {f"role": "user", "content": "## Manual \n" + manual + "\n" +
    "## Question \n The above is the documentation. Write a quiz question for a new employee to test if they understand the above content . The multiple choice question should have only one correct answer and the choice of question should not be a vague choice.\n" +
    "The response should be a JSON object of the following format: \n" +
    "{ question: // the question," +
    "a: // answer option a," +
    "b: // answer option b," +
    "c: // answer option c," +
    "d: // answer option d," +
    "answer: // the correct answer (A, B, C, or D)}\n" + 
    "explain: // an explanation of why the correct answer is correct\n"
    "## Quiz Question \n"
  }
  messages = [system_template, user_template]
  res_prompt = gpt_call(messages)
  # print(res_prompt)
  return res_prompt

def hello(event, context):
  # data = event['body']
  # print(data)
  print(event['body'])
  
  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
    'body':generate_quiz(event['body'])
  }