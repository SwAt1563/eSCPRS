from fastapi import APIRouter, Query, Path, Body, Cookie, Header, Response, status, HTTPException, Depends, Request, BackgroundTasks, WebSocket, WebSocketDisconnect
from typing import Annotated, Any, List, Union
from fastapi.encoders import jsonable_encoder
from core.ollama import get_ollama_chat
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from services.chatbots import  get_database_chat_template
import json

router = APIRouter()






# @router.post ("/ask_database_chat")
# async def database_chat(question: Annotated[Message, Body(..., title="User Question")]) -> Message:

#     if question.role != MessageRole.HUMAN or question.type != MessageType.DATABASE:
#         raise HTTPException(status_code=400, detail="Invalid message role or type")



#     llm_chat = get_ollama_chat(temperature=0.0)
#     prompt = get_database_chat_template()
#     parser = JsonOutputParser()
#     prompt = prompt.partial(format_instructions=parser.get_format_instructions())
#     chain = prompt | llm_chat | parser
#     try:
#         answer = await chain.ainvoke({'question': question.content}) # will return a int value
#     except Exception as e:
#         raise Message(content="0", role=MessageRole.AI, type=MessageType.DATABASE)
    
#     answer = str(answer['answer'])
#     return Message(content=answer, role=MessageRole.AI, type=MessageType.DATABASE)


# Endpoint for WebSocket connection
@router.websocket("/ask")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection
    await websocket.accept()

    try:
        while True:
            # Receive a message from the WebSocket client
            message = await websocket.receive_text()
            message = json.loads(message)
            question = message['question']
            answer = question
            response = json.dumps({"answer": answer})
            await websocket.send_text(response)
    except WebSocketDisconnect:
        pass

