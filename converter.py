from pdf2image import convert_from_path
import pytesseract as pt
from docx import Document
import os


def process_pdf(pdf_path, output_format="text"):
    """
    Process a single PDF file and return extracted text or save output.
    :param pdf_path: Path to the PDF file.
    :param output_format: Output format ("word" or "text").
    :return: Extracted text.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file '{pdf_path}' does not exist.")

    all_text = ""

    # Convert PDF pages to images
    pages = convert_from_path(pdf_path, dpi=300)

    for i, page in enumerate(pages):
        # Save each page as a temporary image
        image_path = f"page_{i + 1}.jpg"
        page.save(image_path, "JPEG")

        # Perform OCR
        text = pt.image_to_string(image_path)
        all_text += f"\n--- Page {i + 1} ---\n{text}"

        # Clean up temporary image
        os.remove(image_path)

    # Save output based on format
    if output_format == "word":
        doc = Document()
        doc.add_paragraph(all_text)
        word_output_path = "output.docx"
        doc.save(word_output_path)
        return all_text, word_output_path
    elif output_format == "text":
        text_output_path = "output.txt"
        with open(text_output_path, "w") as file:
            file.write(all_text)
        return all_text, text_output_path
    else:
        return all_text, None 
