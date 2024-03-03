from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import openai
from openai import OpenAI
from fpdf import FPDF
from django.http import HttpResponse
import os
import time
import requests
from .models import Submission
from django.conf import settings


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

        # Save the submission details to the database
        submission = Submission(user=request.user, title=title, cover_prompt=cover_prompt, content_prompt=content_text)
        submission.save()

        cover_img_url = get_image_url(cover_prompt)
        response = requests.get(cover_img_url)
        image_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.png')
        print(f"{image_path} is here")
        with open(image_path, 'wb') as f:
            f.write(response.content)

        body_text = generate_text_content(content_text=content_text)

        # Create a PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.image(image_path, x=0, y=0, w=pdf.w, h=pdf.h)
        pdf.set_text_color(255, 255, 255)

        pdf.set_font("Helvetica", size=62, style='B')
        pdf.set_y((pdf.h - 10) / 2)
        pdf.cell(0, 10, title, 0, 1, 'C')  # Centered title

        pdf.add_page()
        pdf.set_text_color(0, 0, 0)
        pdf.set_left_margin(20)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Helvetica", size=24, style='B')

        pdf.cell(0, 10, title, 0, 1, 'C')  # Title
        pdf.ln(10) 
        
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, txt=body_text)

        # Output the PDF directly to the browser
        response = HttpResponse(pdf.output(dest='S').encode('latin1'), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="your_document.pdf"'
        return response

    return render(request, 'generator.html')


@login_required
def user_history(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-timestamp')
    print(submissions)
    return render(request, 'history.html', {'submissions': submissions})