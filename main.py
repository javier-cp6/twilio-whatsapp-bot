from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search
import re
import random
from utils.bing_image import get_images

app = Flask(__name__)

@app.route("/", methods=["POST"])
def reply_whatsapp():
  print(request)
  response = MessagingResponse()

  search_results = []

  try:
    user_msg = request.values.get('Body', '').lower()
    user_msg = re.sub('[^a-zA-Z0-9 \n\.]', '', user_msg)
    q = user_msg

    for i in search(q, tld='co.in', num=10, stop=10, pause=0.5, lang="en"):
      search_results.append(i)

  except (ValueError, TypeError):
    return "Invalid request: invalid or missing NumMedia parameter", 400
  
  img_url = get_images(user_msg)

  response.message(f"🤖 Results for '{request.values.get('Body', '')}'")
  response.message("").media(img_url)
  response.message(search_results[random.randint(0,len(search_results)-1)])
    
  return str(response)

if __name__ == "__main__":
    app.run(debug=True)