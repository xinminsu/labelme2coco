import glob
import json
import os


class id2name(object):
    def __init__(self, labelme_json=[]):
        """
        """
        self.labelme_json = labelme_json
        self.annotations = []

        self.data_transfer()

    def data_transfer(self):
        for num, json_file in enumerate(self.labelme_json):
            with open(json_file, "r") as fp:
                savefile = json_file+"1"
                data = json.load(fp)
                self.annotations = []
                self.id2name(data, savefile)

    def annotation(self, annotat_ori, images, categories):
        annotation = {}

        annotation["segmentation"] = annotat_ori["segmentation"]
        annotation["iscrowd"] = annotat_ori["iscrowd"]
        annotation["area"] = annotat_ori["area"]

        for image in images:
            if image["id"] == annotat_ori["image_id"]:
                annotation["image_name"] = image["file_name"]

        annotation["bbox"] = annotat_ori["bbox"]

        for category in categories:
            if category["id"] == annotat_ori["category_id"]:
                annotation["category_name"] = category["name"]

        annotation["id"] = annotat_ori["id"]
        return annotation


    def id2name(self,data, savefile):
        data_coco = {}
        data_coco["images"] = data["images"]
        data_coco["categories"] = data["categories"]

        for annotation in data["annotations"]:
            self.annotations.append(self.annotation(annotation, data["images"], data["categories"]))

        data_coco["annotations"] = self.annotations

        os.makedirs(
            os.path.dirname(os.path.abspath(savefile)), exist_ok=True
        )
        json.dump(data_coco, open(savefile, "w"), indent=4)

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

    args = parser.parse_args()
    labelme_json = glob.glob(os.path.join(args.labelme_images, "*.json"))
    id2name(labelme_json)
