# Import necessary libraries
from flask import Flask, render_template, request, redirect
import openai
import os
import time

from db_connection import get_inventory

# Set the OpenAI API key
openai.api_key = "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"

# Define the name of the bot
name = 'BOT'

# Define the role of the bot
role = 'inventory manager'

# Define the impersonated role with instructions
impersonated_role = """
    From now on, you are going to act as BOT. Your role is inventory manager.
    You are a true impersonation of BOT and you reply to all requests with I pronoun. A human is mainly interested in requests related to item in inventory. A request can belong to four different categories as below. 

SALES: Related to sales history of an item
FORECAST: Related to future forecast of an item
INVENTORY: Inventory status of an item
UNRELATED: User request is not related to sales, forecast or inventory

Given a user request you need to map the request to one of these categories and return the response in a json 
format with five fields as below. Always give response in json format no matter what the request may be.

type: Type of request
item: Name of item being request
date: Date for which data is requested
month: Month for which data is requested
year: Year for which data is requested

Here are few examples - 

Current date and time is February 23, 2024. 

User: How many balloons were sold last month?

Response: {'type': 'SALES', 'item': 'BALOON', 'date': 'NA', 'month': 'February', 'year': 2024}

User: How many dhotis are available?

Response: {'type': 'INVENTORY', 'item': 'DHOTI', 'date': 'NA', 'month': 'NA', 'year': 'NA'}

User: How many pajamas are expected to sold next year?

Response: {'type': 'FORECAST', 'item': 'PAJAMA', 'date': 'NA', 'month': 'NA', 'year': '2025'}

User: When is next Taylor Swift concert?

Response: {'type': 'UNRELATED', 'item': 'NA', 'date': 'NA', 'month': 'NA', 'year': 'NA'}

Now respond to the user request below:

"""

# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd()
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

# Initialize chat history
chat_history = ''

# Create a Flask web application
app = Flask(__name__)



# Function to complete chat input using OpenAI's GPT-3.5 Turbo
def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": f"{impersonated_role}. Conversation history: ''"},
            {"role": "user", "content": f"{user_input}. {explicit_input}"},
        ]
    )

    for item in output['choices']:
        chatgpt_output = item['message']['content']
        
    try:
        formatted_response = eval(chatgpt_output.replace("[","{").replace("]","}"))
        if(formatted_response['type']=='INVENTORY'):
            return_val = get_inventory(formatted_response['item'].lower())
            
            if(return_val == 'Could not connect'):
                chatgpt_output = "There are some errors"
            else:
                chatgpt_output = f"Total availablity for this item is {return_val}."
                
        elif(formatted_response['type']=='UNRELATED'):
            output = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                temperature=1,
                presence_penalty=0,
                frequency_penalty=0,
                max_tokens=2000,
                messages=[
                    {"role": "system", "content": f"Conversation history: ''"},
                    {"role": "user", "content": f"{user_input}. {explicit_input}"},
                ]
            )
            for item in output['choices']:
                chatgpt_output = item['message']['content']
        else:
            chatgpt_output = "Sorry this operation is not yet supported."
            
            
    except Exception as e:
        chatgpt_output = chatgpt_output

    return chatgpt_output

# Function to handle user chat input
def chat(user_input):
    global chat_history, name, chatgpt_output
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chatgpt_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
    chatgpt_output = f'{name}: {chatgpt_raw_output}'
    chat_history += chatgpt_output + '\n'
    with open(history_file, 'a') as f:
        f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output

# Function to get a response from the chatbot
def get_response(userText):
    return chat(userText)

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_response(userText))

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

# Run the Flask app
if __name__ == "__main__":
    app.run()
