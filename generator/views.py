from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import openai
from openai import OpenAI
from fpdf import FPDF
from django.http import HttpResponse
import os
import time
import requests



OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


def get_image_url(cover_prompt):

    client = OpenAI()

    response = client.images.generate(
        model="dall-e-2",
        prompt=cover_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url


def generate_text_content(content_text):

    client = OpenAI()

    content_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": content_text}
        ]
    )

    body_text = content_response.choices[0].message.content

    return body_text


@login_required
def generator(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cover_prompt = request.POST.get('cover')
        content_text = request.POST.get('content')

        cover_img_url = get_image_url(cover_prompt)


        response = requests.get(cover_img_url)
        with open('temp_image.png', 'wb') as f:
            f.write(response.content)

        body_text = generate_text_content(content_text=content_text)

        # Create a PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(200, 10, txt=title, ln=True, align='C')

        pdf.image('temp_image.png', x=10, y=20, w=100)

        pdf.multi_cell(0, 10, txt=body_text)

        # Output the PDF directly to the browser
        response = HttpResponse(pdf.output(dest='S').encode(
            'latin1'), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="your_document.pdf"'
        return response

    return render(request, 'generator.html')
