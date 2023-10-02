from flask import Flask,jsonify,request
from flask_cors import CORS

import openai
import random
from langchain.text_splitter import CharacterTextSplitter

app = Flask(__name__)
CORS(app)

# Constants for calling the OpenAI service
openai_api_key="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"
# gpt_model="gpt-4"
gpt_model="gpt-3.5-turbo"

# manual="เครื่องยนต์ดีเซล (อังกฤษ: diesel engine) เป็นเครื่องยนต์ประเภทหนึ่ง คิดค้นโดยรูด็อล์ฟ ดีเซิล วิศวกรชาวเยอรมัน ในปี ค.ศ. 1897 อาศัยการทำงานของกลจักรการ์โน (Carnot's cycle) ซึ่งคิดขึ้นโดยชาวฝรั่งเศสชื่อ ซาดี การ์โน ตั้งแต่ปี ค.ศ. 1824 เครื่องยนต์ชนิดนี้ไม่มีหัวเทียน การจุดระเบิดอาศัยหลักการอัดอากาศและเชื้อเพลิงให้มีความดันสูงจนเชื้อเพลิงสามารถติดไฟได้หลักการทำงานของเครื่องยนต์ดีเซล คือ อากาศเมื่อถูกอัดตัวจะมีความร้อนสูงขึ้น แต่ถ้าอากาศถูกอัดตัวอย่างรวดเร็วโดยไม่มีการสูญเสียความร้อน ทั้งแรงดันและความร้อนจะสูงขึ้นอย่างรวดเร็ว เมื่อฉีดละอองน้ำมันเชื้อเพลิงเข้าไปในอากาศที่ร้อนจัดจากการอัดตัว ก็จะเกิดการเผาไหม้ขึ้นอย่างทันทีทันใด ทำให้เกิดกำลังงานขึ้น กำลังงานที่เกิดขึ้นจะนำไปใช้ประโยชน์ในรูปของแรงขับหรือแรงผลักดัน ผ่านลูกสูบและก้านสูบทำให้เพลาข้อเหวี่ยงหมุน ณ กำลังอัดเดียวกัน อากาศที่อุณหภูมิเริ่มต้นสูงกว่า เมื่อถูกอัดย่อมมีอุณหภูมิสูงกว่าหรือร้อนกว่าเครื่องยนต์ดีเซลแบ่งออกเป็นแบบใหญ่ๆ ได้เป็น 2 แบบคือ เครื่องยนต์แบบ 4 จังหวะ (The 4-cycle Engine) เครื่องยนต์แบบ 2 จังหวะ (The 2-cycle Engine)"

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
  # print(res_prompt)
  return res_prompt

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
