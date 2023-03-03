# Discord-Bot for Github Repos
This Bot monitors your Github repos and posts information about changes in your Discord channel.  
It uses the **PyGithub** and **discord.py** modules for interacting with the API.  

## How to run
This is a microservice for running on K8s.  
Do the configuration in the ```k8s_stack.yaml```.  
Then apply the Kubernetes Manifest: ```kubectl apply -f k8s_stack.yaml```.  

## Running locally
```
python runner.py
```