from abc import ABC, abstractmethod
from openai import OpenAI
import google.generativeai as genai


class BaseLLM(ABC):

    def __init__(self, name, model_name):
        self.name = name
        self.model_name = model_name

    @abstractmethod
    def create_model(self, prompt) -> str:
        pass

    @abstractmethod
    def get_response(self, chat_session, prompt):
        pass


class GPT(BaseLLM):

    def __init__(self, model_name):
        super().__init__(name="GPT", model_name=model_name)
        self.client = OpenAI(
            #api_key=key  # put the key here
        )
        self.messages = []

    def create_model(self, prompt):

        # Inizializza la storia dei messaggi
        self.messages = []

        if prompt.system_message is not None:
            self.messages.append({"role": "system", "content": prompt.system_message})

        self.messages.append({"role": "user", "content":prompt.user_message})

        # Esegui la prima chiamata al modello
        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.messages,
            max_completion_tokens=32768
        )


        return self.messages

    def get_response(self, messages, prompt) -> str:

        # Aggiungi il messaggio utente
        self.messages.append({"role": "user", "content": prompt.user_message})

        # Invia la richiesta al modello con la storia aggiornata
        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.messages,
            max_completion_tokens=32768 #cambiare
        )

        # Estrai la risposta
        assistant_reply = chat_completion.choices[0].message.content

        # Aggiungi la risposta alla storia
        self.messages.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply

class DeepSeek(BaseLLM):

    def __init__(self, model_name):
        super().__init__(name="DeepSeek", model_name=model_name)

        self.client = OpenAI(
            #api_key="key", #put the key here
            base_url="https://api.deepseek.com")
        self.messages = []

    def create_model(self, prompt):

        # Inizializza la storia dei messaggi
        self.messages = []

        if prompt.system_message is not None:
            self.messages.append({"role": "system", "content": prompt.system_message})

        self.messages.append({"role": "user", "content":""})

        # Esegui la prima chiamata al modello
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model_name,
            temperature=0.0,
            max_tokens=32768,
            stream=False
            )


    def get_response(self, messages, prompt) -> str:

        # Aggiungi il messaggio utente
        self.messages.append({"role": "user", "content": prompt.user_message})

        # Invia la richiesta al modello con la storia aggiornata
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model_name,
            temperature=0.0,
            max_tokens=32768,
            stream=False
            )

        # Estrai la risposta
        assistant_reply = chat_completion.choices[0].message.content

        # Aggiungi la risposta alla storia
        self.messages.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply


class Gemini(BaseLLM):

    def __init__(self, model_name):
        super().__init__(name="Gemini", model_name=model_name)

    def create_model(self, prompt):
        #genai.configure(api_key=key) #put the key there
        generation_config = {
            "temperature": 0
        }

        if prompt.system_message is not None:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config,
                system_instruction=prompt.system_message
            )
        else:
            model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config
            )
        chat_session = model.start_chat(history=[])
        return chat_session

    def get_response(self ,chat_session, prompt) -> str:


        return chat_session.send_message(prompt.user_message).text