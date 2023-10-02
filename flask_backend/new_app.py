from flask import Flask,jsonify,request
from flask_cors import CORS
from decouple import config

import openai
from langchain.text_splitter import CharacterTextSplitter

app = Flask(__name__)
CORS(app)

# Constants for calling the OpenAI service
openai_api_key=config('OPENAI_API_KEY')
gpt_model="gpt-4"
# gpt_model="gpt-3.5-turbo"


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

@app.route('/generate_quiz',methods=['GET','POST'])
def generate_quiz():

  
  #manual from frontend
  data = request.json
  manual = data.get('data')

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
  return res_prompt

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
