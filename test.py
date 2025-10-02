import google.genai as genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Hello Gemini!"]
)
print(response.text)
