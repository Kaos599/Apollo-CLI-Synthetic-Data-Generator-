import os
import google.generativeai as genai

class GeminiGenAIModel:
    def __init__(self, api_key=None, model_name="gemini-pro", temperature=1, top_p=0.95, top_k=40, max_output_tokens=8192):
        
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=self.api_key)

        self.model_name = model_name
        self.generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "response_mime_type": "application/json", 
        }
        self.model = genai.GenerativeModel(model_name=self.model_name, generation_config=self.generation_config)
        self.chat_session = self.model.start_chat(history=[]) 


    def generate_data(self, prompt, num_samples):
        generated_data = []
        for _ in range(num_samples):
            response = self.chat_session.send_message(prompt)
            try:
                
                response_json = json.loads(response.text)
                generated_data.append(response_json) 
            except json.JSONDecodeError:
                
                generated_data.append({"text_response": response.text}) 
        return generated_data