## GitCrawler


Do you find it hard to search for talents who have amazing development skills? Gitcrawler is the perfect solution for you. All you need to do is to use. All you need to do is to enter the username of the person, decide what kind of service you want to use, decide if you want a personalized email of the result. Then hit enter and you are done!🔥

## Technologies used:

## Backend:

### Fast API

- OpenAI API(For embeddings and fetching the results)

- Pinecone API(For similarity search)

- Chroma(For similarity search)

- Github API(To fetch github repository and user informations)

- Gmail API(For Sending automated email)


## Front end:

### React JS

- Tailwind CSS(For rapid development- reused the codes from Tailblocks)

## How it works:


You will get similar interface like this:

![Alt text](<Screenshot from 2023-07-02 18-59-40.png>)

Now enter the username. 

Select whether you want chroma or pinecone for similarity search.

click on the button "CLICK FOR EMAIL" if you want a personalized email of the result.

You will have something like this: 

![Alt text](<Screenshot from 2023-07-02 19-24-29-1.png>)

Hit "CLICK HERE"

![Alt text](<Screenshot from 2023-07-02 19-24-29.png>)

Wait for couple of minutes if you want to see the results in the interface. Otherwise, you will get a personalized email if you have chosen it.

You will get a detailed analysis like this:

![Alt text](<Screenshot from 2023-07-02 19-35-18.png>)

Click on the link if you want to visit the repository too.

Want more? Check your email 📨. You will get details about the user as well as the codes in the repository.


## HOW TO RUN IN LOCAL SYSTEM?

Clone the repository.

RUN 

```
cd backend
```

Start virtaul enviornment by running:

```
virtualenv .venv
```

Activate virtual environment:

```
source .venv/bin/activate
```

Next install the dependencies:

```
pip install -r requirements.txt
```

Next you need to expoert few environment variables:
```
export OPEN_AI_KEY=YOUR_API_KEY

export GITHUB_ACCESS_TOKEN=YOUR_GITHUB_ACCESS_TOKEN

export PINECONE_API_KEY=YOUR_PINECONNECT_API_KEY

export PINECONE_API_ENV=PINECONE_API_ENVIRONMENT

export SENDER_EMAIL=YOUR_EMAIL_ADDRESS

export EMAIL_API_PASSWORD=YOUR_PASSWORD_SDK_FOR_THE_EMAIL
```


Run the application:

```
python3 main.py
```

Now create a separate terminal instance and hit 

```
cd frontend
```

Next install the dependencies:

```
yarn install
```

Start the frontend in development mode:

```
yarn start
```

You are done!



## scope of impovements:

This is 10% of its total potential. There are lots of things we can improve in the project to make it more efficient and bug free with more powerful features:

- Currently I have restricted the number of files that can be travered to be 5 and the number of repositories to be 15. We can increase that but it would take significant amount of time to crawl and give the results. All the APIs have limits of requests and there are associated costs.
- More types of embeddings can be added.
- We can have better summarization of the repositories if we set the max token to higher number. But it will come up with higher cost. 
- More try excpetion blocks should be present for error handling. 
- Email should be authenticated to prevent spamming or malicious works. 
- I have tested with free versions of pinecone sdks. They have limitations of one index only. We should not upsert contents which is not empty otherwise open ai would give       results baseed on previous data too. Either we need to deltete the index or need to delted the  vectors after each operations. I foud later one to be cheaper to use and have better performance.
- We are relying on Open AI response heavily. If there is anything wrong in the response then response in UI part would be heavily affected. 
- All API keys have limits of usages. 
- User experience could have been much better. Due to time constrants they are not implemented yet.


