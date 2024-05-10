from promptmodel import FunctionModel
import asyncio

print("fetch prompt test")

fm = FunctionModel("UserMessageFeatureSelector")
config = fm.get_config()
print(config)

print("ASYNC fetch prompt test")

async def async_test():
    fm = FunctionModel("UserMessageFeatureSelector")
    config = fm.get_config()
    print(config)
    
asyncio.run(async_test())

print("FunctionModel test")

fm = FunctionModel("UserMessageFeatureSelector")
res = fm.run({
    "user_message": "hello",
    "previous_conversation": "",
    "choices": "True, False",
    "event_name": "Say Hi",
    "description": "",
    "conversation_description": "",
})

from pprint import pprint
pprint(res.api_response)

print(res.raw_output)

print("ASYNC FunctionModel test")

async def async_test():
    fm = FunctionModel("UserMessageFeatureSelector")
    res = fm.run({
        "user_message": "hello",
        "previous_conversation": "",
        "choices": "True, False",
        "event_name": "Say Hi",
        "description": "",
        "conversation_description": "",
    })
    pprint(res.api_response)
    print(res.raw_output)

asyncio.run(async_test())

print("Double Async FunctionModel test")

async def async_test():
    fm = FunctionModel("UserMessageFeatureSelector")
    res = await fm.arun({
        "user_message": "hello",
        "previous_conversation": "",
        "choices": "True, False",
        "event_name": "Say Hi",
        "description": "",
        "conversation_description": "",
    })
    pprint(res.api_response)
    print(res.raw_output)

asyncio.run(async_test())