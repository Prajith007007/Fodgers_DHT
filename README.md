# Fodger's DHT

Fodger's DHT  is a distributed micro service, that enables nodes to club their computing power, disks and bandwidth together, to have a safe, secured, community powered cloud platform, where they can upload/download have access to their nodes.

Currently this project focuses on building a decentralized photo storage flask app, responsible for uploading / downloading your personal photos in the decentralized cloud, without any worry of other people having access to your photos.

## Installation

This Project is heavily dependant on python, (flask framework), so once you clone its ,important that you install all the necessary modules inthe requirements.txt file, ideally the following command would work

```bash
pip3 -r install <requirements.txt>
```
You would also require ngrok, rpm inorder to effectively connect with the chain of nodes in our official production network, although it is not required for development.

```
Download and setup [ngrok](https://ngrok.com/download)
```

## Usage

```bash
cd into the main project where app.py is there

flask run --port=3001

```
If you are in production mode, make sure you use ngrok to expose 3001 port

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Code Contributors
This project exists thanks to all the people who contribute. 
<a href="https://github.com/Prajith007007/Fodgers_DHT/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=Prajith007007/Fodgers_DHT"/>
</a>

## Getting Started

We maintain a trello board, to track major RFE, and once we get a owner for a specific task, we create a tracker issue in github and handle it accordingly.

Join trello board, and pick a card ;-) https://trello.com/invite/b/RiiWgGu9/f2d0bb4922960ce320eba4a1b6f9fa56/init-fodgers-dht.

