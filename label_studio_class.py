# Description: This file contains the class for the label studio object
from typing import Dict, Any, List


class Value:
    def __init__(self, x: float, y: float, width: float, height: float, rotation: float, rectanglelabels: List[str]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.rectanglelabels = rectanglelabels

    def __repr__(self):
        return f"Value(x={self.x}, y={self.y}, width={self.width}, height={self.height}, rotation={self.rotation}, rectanglelabels={self.rectanglelabels})"

    def __str__(self):
        return f"Value(x={self.x}, y={self.y}, width={self.width}, height={self.height}, rotation={self.rotation}, rectanglelabels={self.rectanglelabels})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height and self.rotation == other.rotation and self.rectanglelabels == other.rectanglelabels

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height, self.rotation, self.rectanglelabels))

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "rotation": self.rotation,
            "rectanglelabels": self.rectanglelabels
        }

    @staticmethod
    def from_dict(value_dict: Dict[str, Any]):
        return Value(x=value_dict["x"], y=value_dict["y"], width=value_dict["width"], height=value_dict["height"],
                     rotation=value_dict["rotation"], rectanglelabels=value_dict["rectanglelabels"])


class Result:
    def __init__(self, original_width: int, original_height: int, image_rotation: int, value: Dict[str, Any], id: str,
                 from_name: str, to_name: str, type: str, origin: str):
        self.original_width = original_width
        self.original_height = original_height
        self.image_rotation = image_rotation
        self.value = value
        self.id = id
        self.from_name = from_name
        self.to_name = to_name
        self.type = type
        self.origin = origin

    def __repr__(self):
        return f"Result(original_width={self.original_width}, original_height={self.original_height}, image_rotation={self.image_rotation}, value={self.value}, id={self.id}, from_name={self.from_name}, to_name={self.to_name}, type={self.type}, origin={self.origin})"

    def __str__(self):
        return f"Result(original_width={self.original_width}, original_height={self.original_height}, image_rotation={self.image_rotation}, value={self.value}, id={self.id}, from_name={self.from_name}, to_name={self.to_name}, type={self.type}, origin={self.origin})"

    def __eq__(self, other):
        return self.original_width == other.original_width and self.original_height == other.original_height and self.image_rotation == other.image_rotation and self.value == other.value and self.id == other.id and self.from_name == other.from_name and self.to_name == other.to_name and self.type == other.type and self.origin == other.origin

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((
            self.original_width, self.original_height, self.image_rotation, self.value, self.id, self.from_name,
            self.to_name, self.type, self.origin))

    def to_dict(self):
        return {
            "original_width": self.original_width,
            "original_height": self.original_height,
            "image_rotation": self.image_rotation,
            "value": self.value,
            "id": self.id,
            "from_name": self.from_name,
            "to_name": self.to_name,
            "type": self.type,
            "origin": self.origin
        }

    @staticmethod
    def from_dict(result_dict: Dict[str, Any]):
        return Result(original_width=result_dict["original_width"], original_height=result_dict["original_height"],
                      image_rotation=result_dict["image_rotation"], value=result_dict["value"], id=result_dict["id"],
                      from_name=result_dict["from_name"], to_name=result_dict["to_name"], type=result_dict["type"],
                      origin=result_dict["origin"])


class Prediction:
    def __init__(self, model_version: str, score: float, result: Dict[str, Any]):
        self.model_version = model_version
        self.score = score
        self.result = result

    def __repr__(self):
        return f"Prediction(model_version={self.model_version}, score={self.score}, result={self.result})"

    def __str__(self):
        return f"Prediction(model_version={self.model_version}, score={self.score}, result={self.result})"

    def __eq__(self, other):
        return self.model_version == other.model_version and self.score == other.score and self.result == other.result

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.model_version, self.score, self.result))

    def to_dict(self):
        return {
            "model_version": self.model_version,
            "score": self.score,
            "result": self.result
        }

    @staticmethod
    def from_dict(prediction_dict: Dict[str, Any]):
        return Prediction(model_version=prediction_dict["model_version"], score=prediction_dict["score"],
                          result=prediction_dict["result"])


class Detection:
    """
    Detection class format {
        "predictions": [
            {
                "model_version": "yolov",
                "score": 0.5,
                "result": [
                    {
                        "original_width": 1251,
                        "original_height": 932,
                        "image_rotation": 0,
                        "value": {
                            "x": 45.80335731414868,
                            "y": 74.2489270386266,
                            "width": 8.073541167066347,
                            "height": 5.472103004291846,
                            "rotation": 0,
                            "rectanglelabels": [
                                "logo"
                            ]
                        },
                        "id": "logo",
                        "from_name": "label",
                        "to_name": "image",
                        "type": "rectanglelabels",
                        "origin": "manual"
                    }
                ]
            }
        ],
        "data": {
            "image": "/data/local-files/?d=fanatics-20240412/0d11b86c-bc64-11ed-888b-4235db585945-back-crop.jpg"
        },
        "id": "0d11b86c-bc64-11ed-888b-4235db585945-back-crop.jpg"
    }
    """

    def __init__(self, predictions: List[Dict[str, Any]], data: Dict[str, Any], id: str):
        self.predictions = predictions
        self.data = data
        self.id = id

    def __repr__(self):
        return f"Detection(predictions={self.predictions}, data={self.data}, id={self.id})"

    def __str__(self):
        return f"Detection(predictions={self.predictions}, data={self.data}, id={self.id})"

    def __eq__(self, other):
        return self.predictions == other.predictions and self.data == other.data and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.predictions, self.data, self.id))

    def to_dict(self):
        return {
            "predictions": self.predictions,
            "data": self.data,
            "id": self.id
        }

    @staticmethod
    def from_dict(detection_dict: Dict[str, Any]):
        return Detection(predictions=detection_dict["predictions"], data=detection_dict["data"],
                         id=detection_dict["id"])
