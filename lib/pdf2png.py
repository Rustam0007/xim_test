from pdf2image import convert_from_path


def convert_pdf_to_png(pdf_file_path, page_number, output_folder):
    images = convert_from_path(pdf_file_path, first_page=page_number + 1, last_page=page_number + 1)

    if images:
        image = images[0]
        output_path = f"{output_folder}/barcode_{page_number + 1}.png"
        image.save(output_path, "PNG")
        return output_path
    else:
        return None