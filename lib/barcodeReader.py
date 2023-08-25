import cv2
from pyzbar.pyzbar import decode

def read_barcode_from_image(image_path):
    image = cv2.imread(image_path)
    barcodes = decode(image)

    barcode_values = []
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_values.append(barcode_data)

    return barcode_values
