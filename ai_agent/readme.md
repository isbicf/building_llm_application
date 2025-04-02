# Setup
- Install requirements\
  E.g. pip install -r .\ai_agent\requirements.txt
- Setup Ollama
  - Download [Ollama](https://ollama.com/) (Meta's language model), and install it
  - Check if installed
    ```
    ollama --version
    ``` 
  - Install the llama2 model
    ```
    # Install
    ollama pull llama2
    
    # Check if installed 
    ollama list  
    ```

# Run
```
# Start Ollama server
ollama serve

# Run the agent
python -m ai_agent.agent
```

# TroubleShooting
1. Llama2 not found.
   - Error message
     ```
     REQUEST RESPONSE <Response [404]>
     Traceback (most recent call last):
       File "<frozen runpy>", line 198, in _run_module_as_main
       File "<frozen runpy>", line 88, in _run_code
       File "C:\Dale\Projects\learning_llm_app\ai_agent\agent.py", line 202, in <module>
         agent.work(prompt)
         ~~~~~~~~~~^^^^^^^^
       File "C:\Dale\Projects\learning_llm_app\ai_agent\agent.py", line 137, in work
         agent_response_dict = self.think(prompt)
       File "C:\Dale\Projects\learning_llm_app\ai_agent\agent.py", line 124, in think
         agent_response_dict = model_instance.generate_text(prompt)
       File "C:\Dale\Projects\learning_llm_app\ai_agent\ollama_model.py", line 55, in generate_text
         response = request_response_json['response']
                    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
     KeyError: 'response'
     ```
   - Resolution - Start Ollama server install llama2 model
     ```
     ollama serve   # start server
     ollama pull llama2   # install model
     ```

# Reference
- [Vipra's Medium](https://medium.com/@vipra_singh/ai-agents-introduction-part-1-fbec7edb857d)
- [Vipra's GitHub](https://github.com/vsingh9076/AI-Agents)


