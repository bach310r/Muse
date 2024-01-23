from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import openai
from openai import OpenAI
from fpdf import FPDF
from django.http import HttpResponse
import os


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


# # Create your views here.
# def generator(request):
#     return render(request, "generator/generator.html")


@login_required
def generator(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cover_text = request.POST.get('cover')
        content_text = request.POST.get('content')

        # Use OpenAI to generate content (This is a simplified example)
        # Set up OpenAI API key
        openai.api_key = OPENAI_API_KEY

        # cover_image_response = openai.Image.create(prompt=cover_text, n=1)

        # Generate body of text

        client = OpenAI()

        content_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": content_text}
            ]
        )
        body_text = content_response.choices[0].message.content

        # Create a PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=title, ln=True, align='C')
        # Add the image and content to the PDF
        # Note: You'll need to handle the image response and convert it into a format that can be embedded into the PDF
        pdf.multi_cell(0, 10, txt=body_text) 

        # Output the PDF directly to the browser
        response = HttpResponse(pdf.output(dest='S').encode(
            'latin1'), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="your_document.pdf"'
        return response

    return render(request, 'generator/generator.html')
