import openai
import pyttsx3

class usher:
    class ai:

        def __init__(self, api_key):
            self.api_key = api_key

        def text(self, data, word_count):
            def clean_text(data):
                clean_text = str(data).strip()
                return clean_text
            
            openai.api_key = self.api_key
            try:
                response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt= data,
                    temperature=1,
                    max_tokens=word_count,
                    top_p=1,
                    frequency_penalty=0.2,
                    presence_penalty=0
                )

                text = response["choices"][0]["text"]
                text = clean_text(text)
                return text
            
            except openai.error.OpenAIError as e:
                print(e.error)

        def text_command(self, command, data, word_count):
            def clean_text(data):
                clean_text = str(data).strip()
                return clean_text

            command = command + ": "
            combined_data = command + data       
            openai.api_key = self.api_key

            try: 
                response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt= combined_data,
                    temperature=1,
                    max_tokens=word_count,
                    top_p=1,
                    frequency_penalty=0.2,
                    presence_penalty=0
                )

                text = response["choices"][0]["text"]
                text = clean_text(text)
                return text
            
            except openai.error.OpenAIError as e:
                print(e.error)



        def create_txt_file(self, filename, data):
            with open(filename, 'w') as f:
                f.write(data)
            print("File created successfully")
    
    class audio:

        def say(text_data):
            engine = pyttsx3.init()
            engine.say(text_data)
            engine.runAndWait()

        def save(text_data, mp3_output):
            engine = pyttsx3.init("sapi5")
            voices = engine.getProperty("voices")[0] 
            engine.setProperty('voice', voices)
            text = text_data
            engine.save_to_file(text, mp3_output)
            engine.runAndWait() # don't forget to use this line

    class txt:

        def save(text_data,filename):
            with open(filename, 'w') as f:
                f.write(text_data)
            print("File created successfully")

