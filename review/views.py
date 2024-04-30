from django.shortcuts import render
from selenium import webdriver
import cloudinary
import cloudinary.uploader
import requests
from django.views.decorators.http import require_http_methods
import json
from django.http import JsonResponse
from .models import Review
          
cloudinary.config( 
  cloud_name = "denojater", 
  api_key = "YOUR-API-KEY", 
  api_secret = "YOUR-API-SECRET" 
)
# Create your views here.
def take_screenshot(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options=options)

    browser.get(url)

    total_height = browser.execute_script("return document.body.parentNode.scrollHeight")

    browser.set_window_size(1200, total_height)

    screenshot = browser.get_screenshot_as_png()

    browser.quit()

    sanitized_url = url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '_')

    upload_response = cloudinary.uploader.upload(
        screenshot,
        folder="screenshots",
        public_id=f"{sanitized_url}.png",
        resource_type='image'
    )
    
    # print(upload_response)
    return upload_response['url']

def get_review(screenshot_url):
    url = "https://general-runtime.voiceflow.com/state/user/testuser/interact?logs=off"

    payload = {
        "action": {
            "type": "intent",
            "payload": {
                "query": screenshot_url,
                "intent": { "name": "review_intent" },
                "entities": []
            }
        },
        "config": {
            "tts": False,
            "stripSSML": True,
            "stopAll": True,
            "excludeTypes": ["block", "debug", "flow"]
        },
        "state": { "variables": { "x_var": 1 } }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "YOUR-VOICEFLOW-KEY"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    review_text = ""

    for item in data:
        if item['type'] == 'text' and 'payload' in item and 'slate' in item['payload'] and 'content' in item['payload']['slate']:
            review_text = item['payload']['slate']['content'][0]['children'][0]['text']
            break

    # print(review_text)
    return review_text

@require_http_methods(["POST"])
def submit_url(request):
    data = json.loads(request.body)
    domain = data.get('domain')

    website_screenshot = take_screenshot(domain)
    website_review = get_review(website_screenshot)

    new_review_object = Review.objects.create(
        site_url = domain,
        site_image_url = website_screenshot,
        feedback = website_review,
    )

    review_id = new_review_object.id

    response_data = {
        'website_screenshot': website_screenshot,
        'website_review': website_review,
        'review_id': review_id,
    }

    return JsonResponse(response_data)

@require_http_methods(["POST"])
def feedback(request):
    data = json.loads(request.body)
    review_id = data.get('id')
    type = data.get('type')

    try:
        review = Review.objects.get(id=review_id)
        review.user_rating = type
        review.save()

        return JsonResponse({"status": "success", "message": "Feedback submitted"})
    except Review.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Review not found"})
    
def index(request):
    return render(request, 'index.html')