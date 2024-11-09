from fastapi import APIRouter, Query, Path, Body, Cookie, Header, Response, status, HTTPException, Depends, Request, BackgroundTasks, WebSocket, WebSocketDisconnect
from typing import Annotated, Any, List, Union
from fastapi.encoders import jsonable_encoder
from core.ollama import get_ollama_chat
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from services.chatbots import  get_database_chat_template, get_readme_template
import json
from services.queries import invoke_function

router = APIRouter()



@router.post("/ask")
async def database_chat(question: str):
    # Initialize the chat model and parser
    llm_chat = get_ollama_chat(temperature=0.0)
    prompt = get_database_chat_template()
    parser = JsonOutputParser()
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())

    # Create the chain for processing the question
    chain = prompt | llm_chat | parser

    try:
        # Get the function response, which should be an integer
        response = await chain.ainvoke({'question': question})
    except Exception as e:
        # Log and raise an HTTP exception if there is an issue in the chain
        raise HTTPException(status_code=500, detail=f"Error invoking database chain: {str(e)}")

    try:
        # Call the function with the response from the previous chain
        database_response = await invoke_function(response)
    except Exception as e:
        # Log and raise an HTTP exception if there is an issue with invoking the function
        raise HTTPException(status_code=500, detail=f"Error invoking function with response: {str(e)}")

    # Generate a README-style response based on the database response
    readme_prompt = get_readme_template()
    readme_chain = readme_prompt | llm_chat

    try:
        # Get the formatted readme-style response
        readme_response = await readme_chain.ainvoke({'question': question, 'response': database_response})
        answer = readme_response.content
    except Exception as e:
        # Log and raise an HTTP exception if there is an issue generating the readme response
        raise HTTPException(status_code=500, detail=f"Error generating readme-style response: {str(e)}")

    # Return the final answer
    return {"answer": answer}


@router.websocket("/ask")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection
    await websocket.accept()

    llm_chat = get_ollama_chat(temperature=0.0)
    prompt = get_database_chat_template()
    parser = JsonOutputParser()
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    chain = prompt | llm_chat | parser

    # Handle receiving questions and sending answers via WebSocket
    try:
        while True:
            # Receive a message from the WebSocket client
            message = await websocket.receive_text()
            message = json.loads(message)
            question = message.get("question")

            if not question:
                await websocket.send_text(json.dumps({"error": "No question provided"}))
                continue

            # Get the response from the chain processing
            try:
                response = await chain.ainvoke({'question': question})
            except Exception as e:
                await websocket.send_text(json.dumps({"error": f"Error invoking database chain: {str(e)}"}))
                continue

            try:
                # Call the function with the response from the previous chain
                database_response = await invoke_function(response)
            except Exception as e:
                await websocket.send_text(json.dumps({"error": f"Error invoking function with response: {str(e)}"}))
                continue

            # Generate a README-style response based on the database response
            readme_prompt = get_readme_template()
            readme_chain = readme_prompt | llm_chat

            try:
                # Get the formatted readme-style response
                readme_response = await readme_chain.ainvoke({'question': question, 'response': database_response})
                answer = readme_response.content
            except Exception as e:
                await websocket.send_text(json.dumps({"error": f"Error generating readme-style response: {str(e)}"}))
                continue

            # Send the answer back to the client
            response = json.dumps({"answer": answer})
            await websocket.send_text(response)

    except WebSocketDisconnect:
        # Handle client disconnection
        pass