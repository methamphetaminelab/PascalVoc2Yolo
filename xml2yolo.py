import os
import xml.etree.ElementTree as ET

def convert_pascalvoc_to_yolo(xml_folder, yolo_folder):
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_path = os.path.join(xml_folder, filename)
            yolo_path = os.path.join(yolo_folder, os.path.splitext(filename)[0] + ".txt")
            convert_single_file(xml_path, yolo_path)

def convert_single_file(xml_path, yolo_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    image_width = int(root.find("size/width").text)
    image_height = int(root.find("size/height").text)

    with open(yolo_path, "w") as yolo_file:
        for obj in root.findall("object"):
            class_name = obj.find("name").text

            if class_name == "enemy": # Class Name
                bbox = obj.find("bndbox")
                xmin = float(bbox.find("xmin").text)
                ymin = float(bbox.find("ymin").text)
                xmax = float(bbox.find("xmax").text)
                ymax = float(bbox.find("ymax").text)

                x_center = (xmin + xmax) / (2.0 * image_width)
                y_center = (ymin + ymax) / (2.0 * image_height)
                width = (xmax - xmin) / image_width
                height = (ymax - ymin) / image_height

                yolo_file.write(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

if __name__ == "__main__":
    xml_folder = "train"  # Pascal VOC XML Folder
    yolo_folder = "yolo"  # YOLO Save Folder

    if not os.path.exists(yolo_folder):
        os.makedirs(yolo_folder)

    convert_pascalvoc_to_yolo(xml_folder, yolo_folder)
