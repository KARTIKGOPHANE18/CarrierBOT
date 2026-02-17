from google import genai

API_KEY = "AIzaSyDKtPorzTyO3hZcSPIyzHJdUn2Tb0FBH4s"

client = genai.Client(api_key=API_KEY)

for model in client.models.list():
    print(model.name)

