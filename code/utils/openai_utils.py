import os
import sys
import logging
import openai
from openai import AzureOpenAI, OpenAI
import base64
import requests
import json
from typing import List
from PIL import Image

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    stop_after_delay,
    after_log
)

from utils.logc import logc
from utils.bcolors import bcolors as bc
from env_vars import TENACITY_STOP_AFTER_DELAY, TENACITY_TIMEOUT, AZURE_OPENAI_VISION_API_VERSION, AZURE_VISION_ENDPOINT, AZURE_VISION_KEY
from utils.text_utils import recover_json
from opencensus.ext.azure.log_exporter import AzureLogHandler
from env_vars import APPLICATIONINSIGHTS_CONNECTION_STRING

# https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/gpt-4-turbo-with-vision-is-now-available-on-azure-openai-service/ba-p/4008456#:~:text=GPT%2D4%20Turbo%20with%20Vision%20can%20be%20accessed%20in%20the,Switzerland%20North%2C%20and%20West%20US.
# 
#  GPT-4 Turbo with Vision can be accessed in the following Azure regions: Australia East, Sweden Central, Switzerland North, and West US.

AZURE_OPENAI_KEY = os.environ.get('AZURE_OPENAI_KEY')
AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION')
AZURE_OPENAI_MODEL_VISION = os.environ.get('AZURE_OPENAI_MODEL_VISION')
OPENAI_API_BASE = f"https://{os.getenv('AZURE_OPENAI_RESOURCE')}.openai.azure.com/"
AZURE_OPENAI_MODEL = os.environ.get('AZURE_OPENAI_MODEL')

AZURE_OPENAI_EMBEDDING_MODEL= os.environ.get('AZURE_OPENAI_EMBEDDING_MODEL')
AZURE_OPENAI_EMBEDDING_API_BASE = f"https://{os.getenv('AZURE_OPENAI_EMBEDDING_MODEL_RESOURCE')}.openai.azure.com"
AZURE_OPENAI_EMBEDDING_MODEL_RESOURCE_KEY = os.environ.get('AZURE_OPENAI_EMBEDDING_MODEL_RESOURCE_KEY')
AZURE_OPENAI_EMBEDDING_MODEL_API_VERSION = os.environ.get('AZURE_OPENAI_EMBEDDING_MODEL_API_VERSION')



openai.log = "error"
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
logger = logging.getLogger(__name__)

# Add AzureLogHandler to the logger
if APPLICATIONINSIGHTS_CONNECTION_STRING:
    logger.addHandler(AzureLogHandler(connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING))

oai_client = AzureOpenAI(
    azure_endpoint = OPENAI_API_BASE, 
    api_key= AZURE_OPENAI_KEY,  
    api_version= AZURE_OPENAI_API_VERSION,
)


oai_emb_client = AzureOpenAI(
    azure_endpoint = AZURE_OPENAI_EMBEDDING_API_BASE, 
    api_key= AZURE_OPENAI_EMBEDDING_MODEL_RESOURCE_KEY,  
    api_version= AZURE_OPENAI_EMBEDDING_MODEL_API_VERSION,
)

gpt4_models_init = [
    {
        'AZURE_OPENAI_RESOURCE': os.environ.get('AZURE_OPENAI_RESOURCE'),
        'AZURE_OPENAI_KEY': os.environ.get('AZURE_OPENAI_KEY'),
        'AZURE_OPENAI_MODEL_VISION': os.environ.get('AZURE_OPENAI_MODEL_VISION'),
        'AZURE_OPENAI_MODEL': os.environ.get('AZURE_OPENAI_MODEL'),
    }
]
    
addtnl_gpt4_models = [
    {
        'AZURE_OPENAI_RESOURCE': os.environ.get(f'AZURE_OPENAI_RESOURCE_{x}'),
        'AZURE_OPENAI_KEY': os.environ.get(f'AZURE_OPENAI_KEY_{x}'),
        'AZURE_OPENAI_MODEL_VISION': os.environ.get('AZURE_OPENAI_MODEL_VISION'),
        'AZURE_OPENAI_MODEL': os.environ.get('AZURE_OPENAI_MODEL'),
    } 
    for x in range(1, 20)
]

gpt4_models = gpt4_models_init + addtnl_gpt4_models

gpt4_models = [m for m in gpt4_models if (m['AZURE_OPENAI_RESOURCE'] is not None) and (m['AZURE_OPENAI_RESOURCE'] != '')]


class ChatCompletionAgent:
    def __init__(self, client):
        self.client = client

    @retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_delay(TENACITY_STOP_AFTER_DELAY), after=after_log(logger, logging.ERROR))
    def get_chat_completion(self, messages: List[dict], model=AZURE_OPENAI_MODEL, client = oai_client, temperature=0.2):
        logging.debug(f"Calling OpenAI APIs with {len(messages)} messages - Model: {model} - Endpoint: {client._base_url}")
        try:
            response = client.chat.completions.create(model=model, temperature=temperature, messages=messages, timeout=TENACITY_TIMEOUT)
            logging.info(f"Successfully called get_chat_completion with response: {response}")
            return response
        except Exception as e:
            logging.error(f"Error in get_chat_completion: {str(e)}", exc_info=True)
            raise
            
    @retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(5), retry_error_callback=lambda e: isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 429, after=after_log(logger, logging.ERROR))
    def get_chat_completion_with_json(self, messages: List[dict], model=AZURE_OPENAI_MODEL, temperature=0.2):
        try:
            logger.debug(f"Calling OpenAI APIs with {len(messages)} messages - Model: {model} - Endpoint: {self.client._base_url}")
            print(f"\nCalling OpenAI APIs with {len(messages)} messages - Model: {model} - Endpoint: {self.client._base_url}\n{bc.ENDC}")
            print(f"Messages: {messages}")
            return self.client.chat.completions.create(model=model, temperature=temperature, messages=messages, response_format={"type": "json_object"}, timeout=TENACITY_TIMEOUT)
        except Exception as e:
            print(f"Error in get_chat_completion_with_json: {e}")
            raise e
        
    def ask_LLM(self, prompt, temperature=0.2, model_info=None):
        if model_info is not None:
            client = AzureOpenAI(
                azure_endpoint=f"https://{model_info['AZURE_OPENAI_RESOURCE']}.openai.azure.com",
                api_key=model_info['AZURE_OPENAI_KEY'],
                api_version=AZURE_OPENAI_API_VERSION,
            )
        else:
            client = oai_client

        messages = [
            {"role": "system", "content": "You are a helpful assistant, who helps the user with their query."},
            {"role": "user", "content": prompt}
        ]

        result = self.get_chat_completion(messages, temperature=temperature, client=client)
        return result.choices[0].message.content

    def ask_LLM_with_JSON(self, prompt, temperature=0.2, model_info=None):
        if model_info is not None:
            logger.debug(f"Using model info: {model_info}")
            client = AzureOpenAI(
                azure_endpoint=f"https://{model_info['AZURE_OPENAI_RESOURCE']}.openai.azure.com",
                api_key=model_info['AZURE_OPENAI_KEY'],
                api_version=AZURE_OPENAI_API_VERSION,
            )
        else:
            logger.debug(f"Using default model")
            client = oai_client

        messages = [
            {"role": "system", "content": "You are a helpful assistant, who helps the user with their query. You are designed to output JSON."},
            {"role": "user", "content": prompt}
        ]

        result = self.get_chat_completion_with_json(messages, temperature=temperature, client=client)
        return result.choices[0].message.content


class EmbeddingAgent:
    def __init__(self, client):
        self.client = client

    @retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_delay(TENACITY_STOP_AFTER_DELAY), after=after_log(logger, logging.ERROR))
    def get_embeddings(self, text, embedding_model=AZURE_OPENAI_EMBEDDING_MODEL, client=oai_emb_client):
        logger.info(f"Calling OpenAI Embedding APIs with text: {text} - Model: {embedding_model} - Endpoint: {client._base_url}")
        return client.embeddings.create(input=[text], model=embedding_model, timeout=TENACITY_TIMEOUT).data[0].embedding

class ImageProcessingAgent:
    vision_system_prompt = """You are a helpful assistant that uses its vision capabilities to process images, and answer questions around them. 
"""
    def __init__(self, vision_client):
        self.vision_client = vision_client

    def get_image_base64(self, image_path):
        logger.info(f"Converting image to base64: {image_path}")
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode('ascii')

    def convert_png_to_jpg(self, image_path):
        logger.info(f"Converting PNG to JPG: {image_path}")
        if os.path.splitext(image_path)[1].lower() == '.png':
            with Image.open(image_path) as img:
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                new_image_path = os.path.splitext(image_path)[0] + '.jpg'
                img.save(new_image_path, 'JPEG')
                return new_image_path
        else:
            return None

    @retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(10), after=after_log(logger, logging.DEBUG))
    def call_gpt4v(self, imgs, gpt4v_prompt="describe the attached image", prompt_extension="", temperature=0.2, model_info=None, enable_ai_enhancements=False):
        logger.info(f"Calling GPT4V with images: {imgs} - Prompt: {gpt4v_prompt} - Prompt Extension: {prompt_extension} - Temperature: {temperature}")
        if model_info is None:
            api_base = OPENAI_API_BASE
            deployment_name = AZURE_OPENAI_MODEL_VISION
            api_key = AZURE_OPENAI_KEY
        else:
            api_base = f"https://{model_info['AZURE_OPENAI_RESOURCE']}.openai.azure.com/"
            deployment_name = model_info['AZURE_OPENAI_MODEL_VISION']
            api_key = model_info['AZURE_OPENAI_KEY']

        base_url = f"{api_base}openai/deployments/{deployment_name}"
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }

        img_arr = []
        img_msgs = []

        if isinstance(imgs, str):
            img_arr = [imgs]
            image_path_or_url = imgs
        else:
            img_arr = imgs
            image_path_or_url = imgs[0]
        logger.info(f"Start of GPT4V Call to process file(s) {img_arr} with model: {api_base}")
        logc(f"Start of GPT4V Call to process file(s) {img_arr} with model: {api_base}")

        for image_path_or_url in img_arr:
            image_path_or_url = os.path.abspath(image_path_or_url)
            try:
                if os.path.splitext(image_path_or_url)[1] == ".png":
                    image_path_or_url = self.convert_png_to_jpg(image_path_or_url)

                image = f"data:image/jpeg;base64,{self.get_image_base64(image_path_or_url)}"
            except:
                image = image_path_or_url

            img_msgs.append({
                "type": "image_url",
                "image_url": {
                    "url": image
                }
            })

        if prompt_extension != "":
            final_prompt = gpt4v_prompt + '\n' + prompt_extension + '\n'
        else:
            final_prompt = gpt4v_prompt

        content = [
            {
                "type": "text",
                "text": final_prompt
            }
        ]

        content = content + img_msgs

        data = {
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": self.vision_system_prompt},
                {"role": "user", "content": content}
            ],
            "max_tokens": 4095
        }

        if enable_ai_enhancements:
            endpoint = f"{base_url}/extensions/chat/completions?api-version={AZURE_OPENAI_VISION_API_VERSION}"

            data['dataSources'] = [
                {
                    "type": "AzureComputerVision",
                    "parameters": {
                        "endpoint": AZURE_VISION_ENDPOINT,
                        "key": AZURE_VISION_KEY
                    }
                }]
            
            data['enhancements'] = {
                "ocr": {
                    "enabled": True
                },
                "grounding": {
                    "enabled": True
                }
            }
        else:
            endpoint = f"{base_url}/chat/completions?api-version={AZURE_OPENAI_VISION_API_VERSION}"

        print("endpoint", endpoint)
        response = requests.post(endpoint, headers=headers, data=json.dumps(data), timeout=300)
        result = recover_json(response.text)['choices'][0]['message']['content']
        description = f"Image was successfully explained, with Status Code: {response.status_code}"
        logc(f"End of GPT4V Call to process file(s) {img_arr} with model: {api_base}")
        logger.info(f"End of GPT4V Call to process file(s) {img_arr} with model: {api_base}")
        return result, description

class Coordinator:
    def __init__(self):
        self.chat_agent = ChatCompletionAgent(oai_client)
        self.embedding_agent = EmbeddingAgent(oai_emb_client)
        self.image_agent = ImageProcessingAgent(oai_client)

    def handle_request(self, request_type, *args, **kwargs):
        logger.info(f"Handling request: {request_type}")
        if request_type == "get_chat_completion":
            return self.chat_agent.get_chat_completion(*args, **kwargs)
        elif request_type == "get_chat_completion_with_json":
            return self.chat_agent.get_chat_completion_with_json(*args, **kwargs)
        elif request_type == "ask_LLM":
            return self.chat_agent.ask_LLM(*args, **kwargs)
        elif request_type == "ask_LLM_with_JSON":
            return self.chat_agent.ask_LLM_with_JSON(*args, **kwargs)
        elif request_type == "get_embeddings":
            return self.embedding_agent.get_embeddings(*args, **kwargs)
        elif request_type == "call_gpt4v":
            return self.image_agent.call_gpt4v(*args, **kwargs)
        else:
            raise ValueError("Unknown request type")

# Example usage
coordinator = Coordinator()

