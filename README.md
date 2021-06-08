# Ask-A-QuesBot
A chatbot which can instantly answer questions on the paragraph which is provided to it.

## Inspiration
We know that no one likes to read large paragraphs of text to find something they need quickly. Hence, we built a chatbot which can quickly answer questions based on the paragraph provided to it. Users can enter text from their personal documents or can simply copy and paste an entire wikipedia article. Then users simply have to enter their questions and the chatbot will answer them.

## What it does
The chatbot uses transfer learning. We have are using HayStack which takes any text as an input and can answer any question based on the paragraph. The language model used is RoBERTa. Entered text is also stored in a PostgreSQL database with its SHA-256 hash as the primary key

## How we built it
We have used Python, Flask, SocketIO and HayStack to build this. On frontend we have used SocketIO to communicate data back and forth to the server. On the backend, the server is hosted using Eventlet and Nginx as a reverse proxy.

## Challenges we ran into
We weren't able to access the project remotely from the VM, as it uses Socket IO. After reading a lot of tutorials online, we figured out that we can only use Eventlet to deploy a Socket IO application. This was the trickiest and most time consuming part.

## Accomplishments that we're proud of
We are proud that we were able to host our project on the cloud, as that seemed too difficult. We are also proud that we were able to set up a custom domain with SSL.

## What we learned
We learned about cloud computing, adding custom domains and SSL to a virtual machine. We also learned how to secure our virtual machine by using SSH keys and fail2ban.

## What's next for Ask-A-QuesBot
We are trying to get the application to run concurrently so that multiple users can use it at the same time. Right now, only one user at a time can use the application

## How to run it on your PC
Note: As of now, we have only tested it on Linux. Other operating systems may not be supported
1. Clone the repo
2. Activate your virtual environment (if you are using one) and run pip install -r req.txt
3. Install PostgreSQL, create a database and a user and add the appropriate credentials in `main.py` on line 27
4. Run `python main.py` and wait for the server to start. First start may take longer as the language model needs to be downloaded.
5. Navigate to `localhost:5000` in your browser and start using the application!
6. If you want to reload the earlier entered text, copy the SHA-256 hash which is shown on the chat screen when you submit the text. Then navigate to `localhost:5000/passage/{hash}`