#!/usr/bin/env python
# coding: UTF-8 
# author: Cmoon
# date: 2023/3/11 下午2:20

import json
import time
from datetime import datetime
from enum import Enum, auto
from typing import List, Tuple, Iterator, Sequence
from dataclasses import dataclass, field
import cv2
import numpy as np
from ultralytics.engine.results import Results
from functools import update_wrapper, wraps, cached_property
import logging


class TimeUnit(Enum):
    MS = auto()
    S = auto()

    @staticmethod
    def from_string(unit_str):
        return {
            'ms': TimeUnit.MS,
            's': TimeUnit.S,
        }.get(unit_str.lower(), None)


class Timer:
    START_MESSAGE = "============================== {} 开始计时 ===================================="
    END_MESSAGE = "============================== {} 运行耗时：{:.4f}{} =============================="

    def __init__(self, func=None, *, name=None, unit="ms", log=None):
        self.func = func
        self.name = name or (func.__name__ if func else '')
        self.unit = TimeUnit.from_string(unit)
        self.start_time = None
        self.set_log_level(log)
        if func:
            update_wrapper(self, func)

    def set_log_level(self, log_level):
        if log_level:
            log_level = log_level.lower()
            self.log_level = getattr(logging, log_level.upper(), None)
            logging.basicConfig(level=self.log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        else:
            self.log_level = None

    def log(self, message):
        if self.log_level is not None:
            logging.log(self.log_level, message)
        else:
            print(message)

    @classmethod
    def timer(cls, unit='ms', name=None, log=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                with cls(func, name=name, unit=unit, log=log):
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def __call__(self, *args, **kwargs):
        self._start_timing()
        result = self.func(*args, **kwargs)
        self._stop_timing()
        return result

    def __enter__(self):
        self._start_timing()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_timing()

    def _start_timing(self):
        self.start_time = time.perf_counter()
        self.log(self.START_MESSAGE.format(self.name))

    def _stop_timing(self):
        time_cost = time.perf_counter() - self.start_time
        unit_str, multiplier = ("s", 1) if self.unit == TimeUnit.S else ("ms", 1000)
        time_cost *= multiplier
        self.log(self.END_MESSAGE.format(self.name, time_cost, unit_str))

    def format_message(self, message_template, *args):
        return message_template.format(*args)


class Utils:
    @staticmethod
    def xyxy2cnt(xyxy: List[int]) -> List[int]:
        """
        xyxy坐标转中心点坐标

        :param xyxy: [x,y,x,y]
        :return: [x,y]
        """
        center = [int((xyxy[0] + xyxy[2]) / 2), int((xyxy[1] + xyxy[3]) / 2)]
        return center

    @staticmethod
    def show_image(name, img):
        try:
            cv2.imshow(name, img)
            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        except KeyboardInterrupt:
            cv2.destroyAllWindows()

    @staticmethod
    def show_stream(name, img):
        try:
            cv2.imshow(name, img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        except KeyboardInterrupt:
            cv2.destroyAllWindows()

    @staticmethod
    def plot_masks(img0, mask):
        img = img0.copy()
        if type(mask) is list:
            for result in mask:
                msk1 = result.mask.astype(np.bool_)
                color = np.array([0, 0, 255], dtype=np.uint8)
                img[msk1] = img[msk1] * 0.7 + color * 0.3

        else:
            msk1 = mask.astype(np.bool_)
            color = np.array([0, 0, 255], dtype=np.uint8)
            img[msk1] = img[msk1] * 0.7 + color * 0.3

        return img

    @staticmethod
    def calc_roi(size, roi):
        size = [pix for pix in size for _ in range(2)]
        roi_range = [pixel * propotion for pixel, propotion in zip(size, roi)]
        roi_point = [[int(roi_range[0]), int(roi_range[2])], [int(roi_range[1]), int(roi_range[3])]]
        return roi_range, roi_point

    @staticmethod
    def in_roi(point: List[int], size: List[int], roi: Sequence[float]) -> bool:
        """
        判断物品中心点是否在设定的画面范围内

        :param xs: 一张图像上检测到的物品中心坐标
        :param range: 画面中心多大范围内的检测结果被采用
        :return:bool
        """
        roi_range, _ = Utils.calc_roi(size, roi)
        return roi_range[0] <= point[0] <= roi_range[1] and roi_range[2] <= point[1] <= roi_range[3]


@dataclass
class YoloObject:
    """
    单个物体检测结果数据类型
    :param raw_data: 原始检测结果
    :param json_data: json格式的检测结果
    :param dict_data: dict格式的检测结果
    :param name: 物体名称
    :param box: 物体位置
    :param center: 物体中心点
    :param conf: 置信度
    :param id: 追踪id
    :param img0: 原图
    :param img: 检测结果图
    :param mask: 物体mask
    :param points: 关键点坐标
    """

    raw_data: Results = field(init=True, repr=False)
    _json_data: str = field(init=False, repr=False, default=None)
    _dict_data: dict = field(init=False, repr=False, default=None)
    _name: str = field(init=False, repr=False, default=None)
    _box: List[float] = field(init=False, repr=False, default=None)
    _center: List[int] = field(init=False, repr=False, default=None)
    _conf: float = field(init=False, repr=False, default=None)
    _id: int = field(init=False, repr=False, default=None)
    _img0: np.ndarray = field(init=False, repr=False, default=None)
    _img: np.ndarray = field(init=False, repr=False, default=None)
    _mask: np.ndarray = field(init=False, repr=False, default=None)
    _points: List[Tuple[float, float]] = field(init=False, repr=False, default=None)

    @cached_property
    def json_data(self) -> json:
        return self.raw_data.tojson()

    @cached_property
    def dict_data(self) -> dict:
        return json.loads(self.json_data)[0]

    @cached_property
    def name(self) -> str:
        return self.dict_data["name"]

    @cached_property
    def box(self) -> List[float]:
        return [self.dict_data["box"].get(key) for key in ["x1", "y1", "x2", "y2"]]

    @cached_property
    def center(self) -> List[float]:
        return [int((self.box[0] + self.box[2]) / 2), int((self.box[1] + self.box[3]) / 2)]

    @cached_property
    def conf(self) -> float:
        return self.dict_data["confidence"]

    @cached_property
    def id(self) -> int:
        return self.dict_data.get("tracker_id", 1)

    @cached_property
    def img0(self) -> np.ndarray:
        return self.raw_data.orig_img

    @cached_property
    def img(self) -> np.ndarray:
        return self.raw_data.plot()

    @cached_property
    def img_shape(self) -> Tuple[int, int]:
        return self.raw_data.orig_shape[::-1]

    @cached_property
    def mask(self) -> np.ndarray:
        segment = self.dict_data.get("segments")
        if not segment:
            raise ValueError("No segment data. Ensure using a segment model.")
        x_coords = segment.get('x', [])
        y_coords = segment.get('y', [])
        if not x_coords or not y_coords:
            raise ValueError("Segment data is incomplete.")
        points = np.array(list(zip(x_coords, y_coords)), dtype=np.int32)
        _mask = np.zeros((480, 640), dtype=np.uint8)
        cv2.fillPoly(_mask, [points.reshape((-1, 1, 2))], color=(255, 255, 255))
        return _mask

    @cached_property
    def points(self) -> List[Tuple[float, float]]:
        keypoints = self.dict_data.get("keypoints")
        if not keypoints:
            raise ValueError("No pose data. Ensure using a pose model.")
        x_coords = keypoints.get('x', [])
        y_coords = keypoints.get('y', [])
        if not x_coords or not y_coords:
            raise ValueError("Pose data is incomplete.")
        return list(zip(x_coords, y_coords))

    def show_img0(self, stream=False):
        if stream:
            Utils.show_stream("img0", self.img0)
        else:
            Utils.show_image("img0", self.img0)

    def show_img(self, stream=False):
        if stream:
            Utils.show_stream(self.name, self.img)
        else:
            Utils.show_image(self.name, self.img)

    def show_mask(self, stream=False):
        if stream:
            Utils.show_stream(f"{self.name}_mask", self.mask)
        else:
            Utils.show_image(f"{self.name}_mask", self.mask)

    def __sub__(self, other):
        if not isinstance(other, YoloObject):
            raise TypeError("Subtraction can only be performed between two YoloObject instances.")
        return np.sqrt((self.center[0] - other.center[0]) ** 2 + (self.center[1] - other.center[1]) ** 2)

    def __lt__(self, other):
        if not isinstance(other, YoloObject):
            raise TypeError("'<' not supported between instances of 'YoloObject' and other types.")
        return self.center[0] < other.center[0]

    def __eq__(self, other):
        if not isinstance(other, YoloObject):
            return False
        return self.name == other.name

    def __bool__(self):
        return bool(self.raw_data)

    def __str__(self):
        return f"YoloObject({self.json_data})"

    def __repr__(self):
        return self.__str__()


@dataclass
class YoloResult:
    """
    单帧检测结果数据类型
    :param raw_result: 原始检测结果
    :param timestamp: 时间戳
    :param json_result: json格式的检测结果
    :param img0: 原图
    :param img: 检测结果图
    :param img_shape: 原图大小
    :param objects: YoloObject列表
    """
    raw_result: Results = field(init=True, repr=False)
    timestamp: datetime = field(init=False, default_factory=datetime.now)
    _json_result: str = field(init=False, default=None)
    _img0: np.ndarray = field(init=False, repr=False, default=None)
    _img: np.ndarray = field(init=False, repr=False, default=None)
    _img_shape: Tuple[int, int] = field(init=False, repr=False, default=None)
    _objects: List[YoloObject] = field(init=False, repr=False, default=None)

    @cached_property
    def json_result(self) -> json:
        return self.raw_result.tojson()

    @cached_property
    def img0(self) -> np.ndarray:
        return self.raw_result.orig_img

    @cached_property
    def img(self) -> np.ndarray:
        return self.raw_result.plot()

    @cached_property
    def img_shape(self) -> Tuple[int, int]:
        return self.raw_result.orig_shape[::-1]

    @cached_property
    def mask(self) -> np.ndarray:
        try:
            segments = self.raw_result.masks.xy
        except AttributeError:
            raise ValueError("No segment data. Ensure using a segment model.")
        _mask = np.zeros((480, 640), dtype=np.uint8)
        for segment in segments:
            x_coords = segment[:, 0]
            y_coords = segment[:, 1]
            points = np.array(list(zip(x_coords, y_coords)), dtype=np.int32)
            cv2.fillPoly(_mask, [points.reshape((-1, 1, 2))], color=(255, 255, 255))
        return _mask

    @cached_property
    def objects(self) -> List[YoloObject]:
        return [YoloObject(raw_data=result) for result in self.raw_result]

    def show_img0(self, stream=False):
        if stream:
            Utils.show_stream("img0", self.img0)
        else:
            Utils.show_image("img0", self.img0)

    def show_img(self, stream=False):
        if stream:
            Utils.show_stream("img_plot", self.img)
        else:
            Utils.show_image("img_plot", self.img)

    def show_mask(self, stream=False):
        if stream:
            Utils.show_stream("mask", self.mask)
        else:
            Utils.show_image("mask", self.mask)

    def __iter__(self) -> Iterator[YoloObject]:
        return iter(self.objects)

    def __getitem__(self, index: int) -> YoloObject:
        return self.objects[index]

    def __len__(self) -> int:
        return len(self.objects)

    def __bool__(self):
        return bool(self.objects)

    def __contains__(self, item):
        return any(obj.name == item for obj in self.objects)

    def __str__(self):
        return f"YoloResult({self.json_result}, \n'timestamp': {self.timestamp})"

    def __repr__(self):
        return self.__str__()
