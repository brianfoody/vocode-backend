from vocode.streaming.user_implemented_agent.restful_agent import RESTfulAgent
from vocode.streaming.models.agent import RESTfulAgentOutput, RESTfulAgentText, RESTfulAgentEnd
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# in memory store of conversations - a dict indexed by conversation_id with messages as an array of strings 
conversations = {}

def generate_initial_messages():
    return [
        {
            "role": "system",
            "content": "I want you to act as a helpful assistant for a web3 marketplace called EarnOS. Your name is Eva. Your goal is to help investors who land on the page understand how the platform can help them. We are currently seeking investment from strategic partners.",
        },
        {
            "role": "user",
            "content": f"""Earnifi is a web3 town centre that connects exciting web3 products with a growing customer base.

Companies can acquire users by giving rewards to Earnifi users who complete defined tasks.

This helps grow both the Earnifi customer base and the partners products.

Over time a community of users will build up around the Earnifi platform.

Highlight these benefits to the investor.

If they ask to speak to someone tell them they can contact Phil or Wayne to discuss.

Any question which strays outside the realm of web3 or Earnifi should be answered politely but then brought back to the topic of Earnifi.

Do not give any financial advice for example.

The investors chat will start from here. Please respond in Earnie's voice from here on out. Keep your responses short and concise.""",
        }
    ]

def get_or_initiate_conversation(conversation_id: str):
    if conversation_id not in conversations:
        conversations[conversation_id] = generate_initial_messages()
    
    return conversations[conversation_id]


def get_next_message(messages):
    print("getting next message")
    # OPENAI_API_KEY
    openai.api_key = os.getenv("OPENAI_API_KEY") 

    buffer = []

    for resp in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.6,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stream=True
        ):
            if 'content' in resp.choices[0].delta:
                token = resp.choices[0].delta.content
                buffer.append(token)


            # if "." in token:
            #     # print("flushing on period")
            #     sentence = "".join(buffer) + token
                
            #     yield(story_id, buffer)
                
            #     buffer = []
            # else:
            #     buffer.append(token)
    
    response = "".join(buffer) + token
    
    return {
        "role": "system",
        "content": response
    }


class YourAgent(RESTfulAgent):

    # input: the transcript from the Conversation that the agent must respond to
    async def respond(self, input: str, conversation_id: str) -> RESTfulAgentOutput:
        print(f"Received input: {input}")
        if "bye" in input.lower():
            print("ending")
            return RESTfulAgentEnd()  ## ends the conversation
        
        prev_messages = get_or_initiate_conversation(conversation_id)
        prev_messages.append({
            "role": "user",
            "content": input
        })
        
        next_message = get_next_message(prev_messages)

        prev_messages.append(next_message)
        
        conversations[conversation_id] = prev_messages
        response = next_message['content']
        print(f"Responding with")
        print(response)
        return RESTfulAgentText(response=response)  ## responds with the input received

agent = YourAgent()
agent.run(host="0.0.0.0", port=3001)
