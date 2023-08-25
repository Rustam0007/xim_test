import os
import fitz
from pdf2png import convert_pdf_to_png
from barcodeReader import read_barcode_from_image
from collections import defaultdict


def extract_pdf_info(path, barcodeValue):
    doc = fitz.open(path)
    page = doc.load_page(0)
    text = page.get_text("text")

    pdf_info = {}

    lines = text.split('\n')
    for line_index, line in enumerate(lines):
        parts = line.split(':')
        if len(parts) != 2:
            continue
        key = parts[0].strip()
        value = parts[1].strip()

        if "tagged by" in key.lower():
            for i in lines:
                parts_qty = i.split(':')
                if parts_qty[0] == "Qty":
                    pdf_info[key] = {"scan_number": barcodeValue[0], "Qty": parts_qty[1].strip()}
                    break
            break

        if "notes" in key.lower():
            next_line_index = line_index + 1
            if next_line_index < len(lines):
                notes_line = lines[next_line_index]
                pdf_info[key] = notes_line

        else:
            pdf_info[key] = value
    return pdf_info


def compare_pdfs(first_pdf, second_pdf, barcode):
    assert extract_pdf_info(first_pdf, barcode) \
           == extract_pdf_info(second_pdf, barcode), f"File not compare!"


if __name__ == "__main__":
    pdf_file_path = "test_task.pdf"
    file_path_2 = "test_task2.pdf"
    page_number = 0  # Номер страницы (начиная с 0)
    output_folder = "./"  # Папка для сохранения изображений

    barcode_image_path = convert_pdf_to_png(pdf_file_path, page_number, output_folder)
    barcode_values = read_barcode_from_image(barcode_image_path)

    extracted_info = extract_pdf_info(pdf_file_path, barcode_values)
    with open("pdf_info.txt", "w") as file:
        for key, value in extracted_info.items():
            file.write(f"{key}: {value}\n")

    compare_pdfs(pdf_file_path, file_path_2, barcode_values)
    os.remove(barcode_image_path)


