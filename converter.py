# from pdf2image import convert_from_path
# import pytesseract as pt
# from docx import Document
# import cv2
# import os
#
# pdf_directory = r"C:\Users\parth\OneDrive\Desktop\codebase\projs\handwritingOCR\flask\uploads"
# pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
# if not pdf_files:
#     raise FileNotFoundError("No PDF files found in the specified directory!")
#
# pdf_filename = pdf_files[0]
# pdf_path = os.path.join(pdf_directory, pdf_filename)
#
# all_text = ""
#
#
# def get_text():
#     return all_text
#
#
# pages = convert_from_path(pdf_path, dpi=300)
#
# image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
# processed_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
#
# for i, page in enumerate(pages):
#     image_path = f"page{i + 1}.jpg"  # Temporary filename for each page
#     page.save(image_path, "JPEG")  # Save the page as a JPEG image
#
#     # OCR the image
#     text = pt.image_to_string(image_path)
#     print(f"Recognized Text from Page {i + 1}:\n{text}\n")
#
#     all_text += f"\n--- Page {i + 1} ---\n{text}"
#
# choice = input("Enter the output format (word/text): ").strip().lower()
#
# if choice == "word":
#     doc = Document()
#     doc.add_paragraph(all_text)
#     doc.save("output.docx")
#     print("Word file saved as 'output.docx'")
# elif choice == "text":
#     with open("output.txt", "w") as file:
#         file.write(all_text)
#     print("Text file saved as 'output.txt'")
# else:
#     print("Invalid choice. Please choose 'word' or 'text'.")
# Updated converter.py

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
