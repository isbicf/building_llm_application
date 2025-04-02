from termcolor import colored

from ai_agent.toolbox import ToolBox
from ai_agent.ollama_model import OllamaModel
from ai_agent.tools import basic_calculator, reverse_string

agent_system_prompt_template = """
You are an intelligent AI assistant with access to specific tools. Your responses must ALWAYS be in this JSON format:
{{
    "tool_choice": "name_of_the_tool",
    "tool_input": "inputs_to_the_tool"
}}

TOOLS AND WHEN TO USE THEM:

1. basic_calculator: Use for ANY mathematical calculations
   - Input format: {{"num1": number, "num2": number, "operation": "add/subtract/multiply/divide"}}
   - Supported operations: add/plus, subtract/minus, multiply/times, divide
   - Example inputs and outputs:
     Input: "Calculate 15 plus 7"
     Output: {{"tool_choice": "basic_calculator", "tool_input": {{"num1": 15, "num2": 7, "operation": "add"}}}}

     Input: "What is 100 divided by 5?"
     Output: {{"tool_choice": "basic_calculator", "tool_input": {{"num1": 100, "num2": 5, "operation": "divide"}}}}

2. reverse_string: Use for ANY request involving reversing text
   - Input format: Just the text to be reversed as a string
   - ALWAYS use this tool when user mentions "reverse", "backwards", or asks to reverse text
   - Example inputs and outputs:
     Input: "Reverse of 'Howwwww'?"
     Output: {{"tool_choice": "reverse_string", "tool_input": "Howwwww"}}

     Input: "What is the reverse of Python?"
     Output: {{"tool_choice": "reverse_string", "tool_input": "Python"}}

3. no tool: Use for general conversation and questions
   - Example inputs and outputs:
     Input: "Who are you?"
     Output: {{"tool_choice": "no tool", "tool_input": "I am an AI assistant that can help you with calculations, reverse text, and answer questions. I can perform mathematical operations and reverse strings. How can I help you today?"}}

     Input: "How are you?"
     Output: {{"tool_choice": "no tool", "tool_input": "I'm functioning well, thank you for asking! I'm here to help you with calculations, text reversal, or answer any questions you might have."}}

STRICT RULES:
1. For questions about identity, capabilities, or feelings:
   - ALWAYS use "no tool"
   - Provide a complete, friendly response
   - Mention your capabilities

2. For ANY text reversal request:
   - ALWAYS use "reverse_string"
   - Extract ONLY the text to be reversed
   - Remove quotes, "reverse of", and other extra text

3. For ANY math operations:
   - ALWAYS use "basic_calculator"
   - Extract the numbers and operation
   - Convert text numbers to digits

Here is a list of your tools along with their descriptions:
{tool_descriptions}

Remember: Your response must ALWAYS be valid JSON with "tool_choice" and "tool_input" fields.
"""


class Agent:
    def __init__(self, tools, model_service, model_name, stop=None):
        """
        Initializes the agent with a list of tools and a model.

        Parameters:
        tools (list): List of tool functions.
        model_service (class): The model service class with a generate_text method.
        model_name (str): The name of the model to use.
        """
        self.tools = tools
        self.model_service = model_service
        self.model_name = model_name
        self.stop = stop

    def prepare_tools(self):
        """
        Stores the tools in the toolbox and returns their descriptions.

        Returns:
        str: Descriptions of the tools stored in the toolbox.
        """
        toolbox = ToolBox()
        toolbox.store(self.tools)
        tool_descriptions = toolbox.tools()
        return tool_descriptions

    def think(self, prompt):
        """
        Runs the generate_text method on the model using the system prompt template and tool descriptions.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        dict: The response from the model as a dictionary.
        """
        tool_descriptions = self.prepare_tools()
        agent_system_prompt = agent_system_prompt_template.format(tool_descriptions=tool_descriptions)

        # Create an instance of the model service with the system prompt

        if self.model_service == OllamaModel:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0,
                stop=self.stop
            )
        else:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0
            )

        # Generate and return the response dictionary
        agent_response_dict = model_instance.generate_text(prompt)
        return agent_response_dict

    def work(self, prompt):
        """
        Parses the dictionary returned from think and executes the appropriate tool.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        The response from executing the appropriate tool or the tool_input if no matching tool is found.
        """
        agent_response_dict = self.think(prompt)
        tool_choice = agent_response_dict.get("tool_choice")
        tool_input = agent_response_dict.get("tool_input")

        for tool in self.tools:
            if tool.__name__ == tool_choice:
                response = tool(tool_input)
                print(colored(response, 'cyan'))
                return

        print(colored(tool_input, 'cyan'))
        return


if __name__ == "__main__":
    """
    Instructions for using this agent:

    Example queries you can try:
    1. Calculator operations:
       - "Calculate 15 plus 7"
       - "What is 100 divided by 5?"
       - "Multiply 23 and 4"

    2. String reversal:
       - "Reverse the word 'hello world'"
       - "Can you reverse 'Python Programming'?"

    3. General questions (will get direct responses):
       - "Who are you?"
       - "What can you help me with?"

    Ollama Commands (run these in terminal):
    - Check available models:    'ollama list'
    - Check running models:      'ps aux | grep ollama'
    - List model tags:          'curl http://localhost:11434/api/tags'
    - Pull a new model:         'ollama pull mistral'
    - Run model server:         'ollama serve'
    """

    tools = [basic_calculator, reverse_string]

    # Uncomment below to run with OpenAI
    # model_service = OpenAIModel
    # model_name = 'gpt-3.5-turbo'
    # stop = None

    # Using Ollama with llama2 model
    model_service = OllamaModel
    model_name = "llama2"  # Can be changed to other models like 'mistral', 'codellama', etc.
    stop = "<|eot_id|>"

    agent = Agent(tools=tools, model_service=model_service, model_name=model_name, stop=stop)

    print("\nWelcome to the AI Agent! Type 'exit' to quit.")
    print("You can ask me to:")
    print("1. Perform calculations (e.g., 'Calculate 15 plus 7')")
    print("2. Reverse strings (e.g., 'Reverse hello world')")
    print("3. Answer general questions\n")

    while True:
        prompt = input("Ask me anything: ")
        if prompt.lower() == "exit":
            break

        agent.work(prompt)
