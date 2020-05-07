import glob
import json
import os

class mergecoco(object):
    def __init__(self, labelme_json=[], save_json_path="./coco.json"):
        """
        """
        self.labelme_json = labelme_json
        self.save_json_path = save_json_path
        self.images = []
        self.categories = []
        self.annotations = []
        self.labels = []
        self.annID = 1
        self.imgID = 0

        self.save_json()

    def data_transfer(self):
        for num, json_file in enumerate(self.labelme_json):
            with open(json_file, "r") as fp:
                data = json.load(fp)
                for dimage in data["images"]:
                    self.images.append(self.image(dimage))
                    self.imgID += 1
                for category in data["categories"]:
                    if category["name"] not in self.labels:
                        self.labels.append(category["name"])
                        self.categories.append(self.category(category["name"]))
                for annotation in data["annotations"]:
                    self.annotations.append(self.annotation(annotation))
                    self.annID += 1

    def image(self, data):
        image = {}
        height = data["height"]
        width = data["width"]
        image["height"] = height
        image["width"] = width
        image["id"] = self.imgID
        image["file_name"] = data["file_name"]

        self.height = height
        self.width = width

        return image

    def category(self, label):
        category = {}
        category["supercategory"] = label
        category["id"] = len(self.categories)
        category["name"] = label
        return category

    def annotation(self, data):

        annotation = {}
        annotation["segmentation"] = data["segmentation"]
        annotation["iscrowd"] = 0
        annotation["area"] = data["area"]

        for image in self.images:
            if image["file_name"] == data["image_name"]:
                annotation["image_id"] = image["id"]


        annotation["bbox"] = data["bbox"]

        for category in self.categories:
            if category["name"] == data["category_name"]:
                annotation["category_id"] = category["id"]

        annotation["id"] = self.annID
        return annotation

    def data2coco(self):
        data_coco = {}
        data_coco["images"] = self.images
        data_coco["categories"] = self.categories
        data_coco["annotations"] = self.annotations
        return data_coco

    def save_json(self):
        print("save coco json")
        self.data_transfer()
        self.data_coco = self.data2coco()

        print(self.save_json_path)
        os.makedirs(
            os.path.dirname(os.path.abspath(self.save_json_path)), exist_ok=True
        )
        #json.dump(self.data_coco, open(self.save_json_path, "w"), indent=4)
        json.dump(self.data_coco, open(self.save_json_path, "w"), separators=(',', ':'))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="labelme annotation to coco data json file."
    )
    parser.add_argument(
        "labelme_images",
        help="Directory to labelme images and annotation json files.",
        type=str,
    )
    parser.add_argument(
        "--output", help="Output json file path.", default="trainval.json"
    )
    args = parser.parse_args()
    labelme_json = glob.glob(os.path.join(args.labelme_images, "*.json1"))
    mergecoco(labelme_json, args.output)
