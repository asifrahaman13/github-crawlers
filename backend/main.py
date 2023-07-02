
import uvicorn
from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from data import fetch_github, convert_to_pdf
from embeddings import embeddings
from msgsend import send_email

# Initialize the fast API
app = FastAPI()


headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://trackapi.nutritionix.com/docs/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'accept': 'application/json',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# Added multiple origins to remove the cors errors which we may encounter later

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:8000/api",
    "http://192.168.140.47:3001/frontend-repo",
    "http://192.168.140.47:3001/frontend-repo/",
    "http://192.168.140.47:3001",
    "http://192.168.140.47:3001/",
    "https://64a178ed0103a8595d4991db--calm-trifle-e24af9.netlify.app/",
    "https://64a178ed0103a8595d4991db--calm-trifle-e24af9.netlify.app"
]



# Middleware to pass on the cors error and to check the credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the data model to define the data types of the json data we will accept.
class YourDataModel(BaseModel):
    username: str
    email_id: str
    service: str

# Function to fetch all the codes of the repositories of the person

def fetching(username,email_id,service):
    fetching_info=fetch_github(username)
    convert_to_pdf(username)
    responses = embeddings(username, service)
    if(len(email_id))!=0:
        send_email(username,email_id, responses,fetching_info, responses)
    return responses

@app.post("/postdata")
async def your_endpoint(your_data: YourDataModel):
    # Access the JSON data within the endpoint
    username = your_data.username
    email_id = your_data.email_id
    service = your_data.service
    # Process the data as needed
    # Example: Return a response message with the received data
    msg = fetching(username,email_id,service)
    return {"response1": f"{msg[0]}", "response2": f"{msg[1]}"}


# API to access the index page of the web application
@app.get("/hello")
async def index():
    response = Response(content="Hello, World!", media_type="text/plain")
    return response

# Driving code of the file.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Lalit2005
# VanRoy
# priyanshu9588
# abir-taheer