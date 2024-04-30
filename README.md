This is the source code for an AI Portfolio Site Reviewer. 


The techstack used are Python(Django), HTML, TailwindCSS & Javascript.<br><br>

To run this locally, run these commands:
```html
git clone https://github.com/tomitokko/ai-portfolio-reviewer
```

```html
cd ai-portfolio-reviewer
```
<be>

Now run this command below and open http://127.0.0.1:8000/ in your browser to view this project

```html
python3 manage.py runserver
```
<br><br>
Here is a quick image display for the whole application
<img width="1440" alt="image" src="https://res.cloudinary.com/denojater/image/upload/v1714516439/ylqioaftej9opoqfiaql.webp"><hr>

VoiceFlow Code to query OpenAI Vision:

```
{
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Take a good look at the image, it is a full screenshot of a portfolio website. Analyse the image I have provided and give me a full detailed review of the portfolio website. Everything from the good and bad, and also things to improve on. Go into details."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "{last_utterance}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 1000
}
```
