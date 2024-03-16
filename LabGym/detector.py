"""
Copyright (C)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)#fulltext.

For license issues, please contact:

Dr. Bing Ye
Life Sciences Institute
University of Michigan
210 Washtenaw Avenue, Room 5403
Ann Arbor, MI 48109-2216
USA

Email: bingye@umich.edu
"""

import json
import os
import shutil
from pathlib import Path

import cv2
import torch

from LabGym.tools import DetectronImportError

try:
    from detectron2 import model_zoo
    from detectron2.checkpoint import DetectionCheckpointer
    from detectron2.config import get_cfg
    from detectron2.data import (
        DatasetCatalog,
        MetadataCatalog,
        build_detection_test_loader,
    )
    from detectron2.data.datasets import register_coco_instances
    from detectron2.engine import DefaultPredictor, DefaultTrainer
    from detectron2.evaluation import COCOEvaluator, inference_on_dataset
    from detectron2.utils.visualizer import Visualizer
except ImportError:
    raise DetectronImportError

DETECTOR_FOLDER = Path(__file__).resolve().parent / "detectors"


class Detector:
    """A Detector model.

    Attributes:
        path:
            The path to the Detector.
        animal_names:
            The names of the animals associated with this Detector.
    """

    def __init__(self, name: str | None = None, path: str | None = None) -> None:
        if name is None and path is not None:
            self.path = Path(path)
            if not self.path.is_dir():
                raise ValueError("Detector path must be a directory.")
        elif name is not None and path is None:
            self.path = DETECTOR_FOLDER / name
        else:
            raise ValueError("Must specify either name or path, but not both.")

    def __str__(self) -> str:
        """Return the name of the Detector."""
        return self.path.name

    @property
    def animal_names(self) -> list[str]:
        """The names of the animals associated with this Detector."""
        animal_mapping = self.path / "model_parameters.txt"
        with open(animal_mapping) as f:
            model_parameters = f.read()
        return json.loads(model_parameters)["animal_names"]

    def train(
        self,
        annotation_path: str,
        training_images_path: str,
        max_num_iterations: int,
        inference_size: int,
    ) -> None:
        """Train this Detector.

        Args:
            annotation_path:
                The path to the .json annotation file in COCO format.
            training_images_path:
                The path to the folder containing the training images.
            max_num_iterations:
                The maximum number of iterations to do while training.
            inference_size:
                ???
        """
        # We are re-training this model, so remove the current catalog files (I think?)
        if "LabGym_detector_train" in DatasetCatalog.list():
            DatasetCatalog.remove("LabGym_detector_train")
            MetadataCatalog.remove("LabGym_detector_train")
        register_coco_instances("LabGym_detector_train", {}, annotation_path, training_images_path)

        datasetcat = DatasetCatalog.get("LabGym_detector_train")
        metadatacat = MetadataCatalog.get("LabGym_detector_train")
        classnames = metadatacat.thing_classes

        model_parameters_dict = {}
        model_parameters_dict["animal_names"] = []
        with open(annotation_path) as annotation:
            annotation_data = json.load(annotation)

        for category in annotation_data["categories"]:
            # Ignore RoboFlow's default category, which has an ID of 0 (I think?)
            if category["id"] > 0:
                model_parameters_dict["animal_names"].append(category["name"])
        formatted_animal_names = ",".join(model_parameters_dict["animal_names"])
        print(f"Animal names in annotation files: {formatted_animal_names}")

        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.OUTPUT_DIR = str(self.path)
        cfg.DATASETS.TRAIN = ("LabGym_detector_train",)
        cfg.DATASETS.TEST = ()
        cfg.DATALOADER.NUM_WORKERS = 4
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = int(len(classnames))
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        cfg.SOLVER.MAX_ITER = max_num_iterations
        cfg.SOLVER.BASE_LR = 0.001
        cfg.SOLVER.WARMUP_ITERS = int(max_num_iterations * 0.1)
        cfg.SOLVER.STEPS = (
            int(max_num_iterations * 0.4),
            int(max_num_iterations * 0.8),
        )
        cfg.SOLVER.GAMMA = 0.5
        cfg.SOLVER.IMS_PER_BATCH = 4
        cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        cfg.INPUT.MIN_SIZE_TEST = int(inference_size)
        cfg.INPUT.MAX_SIZE_TEST = int(inference_size)
        cfg.INPUT.MIN_SIZE_TRAIN = (int(inference_size),)
        cfg.INPUT.MAX_SIZE_TRAIN = int(inference_size)

        os.makedirs(cfg.OUTPUT_DIR)
        trainer = DefaultTrainer(cfg)
        trainer.resume_or_load(False)
        trainer.train()

        model_parameters = os.path.join(cfg.OUTPUT_DIR, "model_parameters.txt")

        model_parameters_dict["animal_mapping"] = {}
        model_parameters_dict["inferencing_framesize"] = int(inference_size)

        for i in range(len(classnames)):
            model_parameters_dict["animal_mapping"][i] = classnames[i]

        with open(model_parameters, "w") as f:
            f.write(json.dumps(model_parameters_dict))

        predictor = DefaultPredictor(cfg)
        model = predictor.model
        DetectionCheckpointer(model).resume_or_load(os.path.join(cfg.OUTPUT_DIR, "model_final.pth"))
        model.eval()

        config = os.path.join(cfg.OUTPUT_DIR, "config.yaml")
        with open(config, "w") as f:
            f.write(cfg.dump())

    def test(self, annotation_path: str, testing_images_folder: str, results_folder: str) -> None:
        """Test this Detector with the given testing images.

        Args:
            annotation_path:
                The path to the .json annotation file in COCO format.
            testing_images_folder:
                The path to the folder containing the testing images.
            results_folder:
                The folder to store the testing results.
        """
        if "LabGym_detector_test" in DatasetCatalog.list():
            DatasetCatalog.remove("LabGym_detector_test")
            MetadataCatalog.remove("LabGym_detector_test")
        register_coco_instances("LabGym_detector_test", {}, annotation_path, testing_images_folder)
        datasetcat = DatasetCatalog.get("LabGym_detector_test")

        animalmapping = os.path.join(self.path, "model_parameters.txt")
        with open(animalmapping) as f:
            model_parameters = f.read()
        animal_names = json.loads(model_parameters)["animal_names"]
        dt_infersize = int(json.loads(model_parameters)["inferencing_framesize"])
        print("The total categories of animals / objects in this Detector: " + str(animal_names))
        print("The inferencing framesize of this Detector: " + str(dt_infersize))
        cfg = get_cfg()
        cfg.merge_from_file(str(self.path / "config.yaml"))
        cfg.MODEL.WEIGHTS = str(self.path / "model_final.pth")
        cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        predictor = DefaultPredictor(cfg)

        for d in datasetcat:
            im = cv2.imread(d["file_name"])
            outputs = predictor(im)
            v = Visualizer(im[:, :, ::-1], MetadataCatalog.get("LabGym_detector_test"), scale=1.2)
            out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            cv2.imwrite(
                os.path.join(results_folder, os.path.basename(d["file_name"])),
                out.get_image()[:, :, ::-1],
            )

        evaluator = COCOEvaluator("LabGym_detector_test", cfg, False, output_dir=results_folder)
        val_loader = build_detection_test_loader(cfg, "LabGym_detector_test")
        inference_on_dataset(predictor.model, val_loader, evaluator)
        mAP = evaluator._results["bbox"]["AP"]
        print(f"The mean average precision (mAP) of the Detector is: {mAP:.4f}" + "%.")

        print("Detector testing completed!")

    def delete(self) -> None:
        """Permanently delete this detector."""
        shutil.rmtree(str(self.path))


def get_detector_names() -> list[str]:
    """Return the names of all saved detectors."""
    ignore = ["__pycache__", "__init__", "__init.py__"]
    return [path.name for path in DETECTOR_FOLDER.glob("*") if path.is_dir() and path.name not in ignore]


def get_annotation_class_names(annotation_path: str) -> list[str]:
    """Return a list of class names associated with the annotation file.

    Args:
        annotation_path: The absolute path to the COCO annotation file.

    Raises:
        FileNotFoundError: The annotation file doesn't exist (this should
            be taken care of by the file selection GUI).
    """
    with open(annotation_path) as f:
        info = json.load(f)
    classnames = []
    for category in info["categories"]:
        if category["id"] > 0:
            classnames.append(category["name"])
    return classnames