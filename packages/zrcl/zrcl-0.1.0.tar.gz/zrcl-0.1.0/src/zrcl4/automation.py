from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import cached_property
import time
import typing
import numpy
import pygetwindow as gw
from PIL import Image
import screeninfo
from zrcl3_utils.pillow import load_base64_img
from zrcl3_utils.pygetwindow import activate_wnd
from zrcl3_utils.screeninfo import get_primary_monitor, wnd_on_monitor


def img_reg(token: "AutoToken"):
    from zrcl3_utils.pyscreeze import locate

    return locate(
        token.sourceImg,
        token.targetImg,
        _algo=token.cfg_imgAlgo,
        confidence=token.confidence,
    )


def ocr(token: "AutoToken"):
    from zrcl3_utils.easyocr import get_text_coordinates, EasyOCRMeta

    imagearr = numpy.array(token.targetImg)
    res: list[EasyOCRMeta] = get_text_coordinates(imagearr, token.cfg_ocrLang)
    token.ocrMatchResult = res
    if token.cfg_ocrMatchMethod == "fuzz":
        from thefuzz import process

        what = process.extract(token.text, res, scorer=process.fuzz.token_set_ratio)
        token.ocrMatchResult = what
        rect = what[0][0]

    else:
        records = []
        maxed = None
        for item in res:
            if token.cfg_ocrMatchMethod == "exact" and item["text"] != token.text:
                continue
            elif (
                token.cfg_ocrMatchMethod == "contains"
                and token.text not in item["text"]
            ):
                continue
            elif token.cfg_ocrMatchMethod == "startswith" and not item[
                "text"
            ].startswith(token.text):
                continue
            if maxed is None or item["confidence"] > maxed["confidence"]:
                maxed = item
            records.append((item, item["confidence"]))

        token.ocrMatchResult = records

        if not maxed:
            return None
        rect = maxed

    if rect["confidence"] < token.confidence:
        return None

    top_left = rect["top_left"]
    bottom_rght = rect["bottom_right"]
    # return as rect
    return (
        top_left[0],
        top_left[1],
        bottom_rght[0] - top_left[0],
        bottom_rght[1] - top_left[1],
    )


@dataclass
class AutoToken:
    text: str = None
    image: typing.Union[Image.Image, str, numpy.ndarray] = None

    wnd: typing.Union[str, gw.Window] = None
    monitor: typing.Union[screeninfo.Monitor, int] = None
    region: typing.Tuple[typing.Union[int, float], ...] = None
    image2: typing.Union[Image.Image, str, numpy.ndarray] = None

    confidence: float = 0.8

    cfg_imgAlgo: typing.Literal["cv2", "pillow"] = "pillow"
    cfg_ocrLang: typing.List[str] = field(default_factory=lambda: ["en"])
    cfg_ocrMatchMethod: typing.Literal["startswith", "contains", "fuzz", "exact"] = (
        "fuzz"
    )

    onImgProcess: typing.Callable = None
    preProcessCallback: typing.Callable = None
    postProcessCallback: typing.Callable = None
    ocrMethod: typing.Callable = ocr
    imgMethod: typing.Callable = img_reg

    ocrMatchResult: typing.List[dict] = None
    result: typing.Tuple[float, float] = None

    def __post_init__(self):
        if not self.text and not self.image:
            raise ValueError("Either 'text' or 'image' must be set")

        if self.monitor and isinstance(self.monitor, int):
            self.monitor = screeninfo.get_monitors()[self.monitor]

        if self.wnd and isinstance(self.wnd, str):
            self.wnd = gw.getWindowsWithTitle(self.wnd)[0]

    @staticmethod
    def __prep_img(img):
        if isinstance(img, Image.Image):
            return img
        elif isinstance(numpy, numpy.ndarray):
            return Image.fromarray(img)
        elif isinstance(img, str) and img.startswith("data:image/png;base64,"):
            return load_base64_img(img)
        elif isinstance(img, str):
            return Image.open(img)
        else:
            raise ValueError("Invalid image type")

    @cached_property
    def sourceImg(self):
        if self.text:
            return None

        return self.__prep_img(self.image)

    @property
    def targetImg(self):
        if self.image2:
            return self.__prep_img(self.image2)

        # screenshot
        import pyscreeze

        if self.wnd:
            activate_wnd(self.wnd)
        ss = pyscreeze.screenshot(
            region=self.interestedRegion,
            allScreens=True if not self.wnd or self.wndInNonPrimaryMonitor else False,
        )
        if self.onImgProcess:
            self.onImgProcess(ss)
        return ss

    @property
    def regionIsRect(self):
        return len(self.region) == 4

    @property
    def regionAsInts(self):
        return tuple(map(int, self.region))

    @property
    def wndInNonPrimaryMonitor(self):
        if not self.wnd:
            return None

        return wnd_on_monitor(self.wnd) != get_primary_monitor()

    @property
    def monitorCenterPoint(self):
        if not self.monitor:
            return None
        assert isinstance(self.monitor, screeninfo.Monitor)
        return (
            self.monitor.x + self.monitor.width / 2,
            self.monitor.y + self.monitor.height / 2,
        )

    @property
    def interestedRegion(self):
        if self.wnd and not self.monitor:
            self.monitor = wnd_on_monitor(self.wnd)

        match (self.wnd, self.monitor, self.region):
            case (None, None, None):
                primary = get_primary_monitor()
                return (primary.x, primary.y, primary.width, primary.height)
            case (wnd, _, None):
                return (wnd.left, wnd.top, wnd.width, wnd.height)
            case (wnd, _, region) if self.regionIsRect:
                return (wnd.left + region[0], wnd.top + region[1], region[2], region[3])
            case (wnd, _, region) if not self.regionIsRect:
                # treat as width and height in center
                return (
                    wnd.left + wnd.width / 2 - region[0] / 2,
                    wnd.top + wnd.height / 2 - region[1] / 2,
                    region[0],
                    region[1],
                )
            case (None, None, region) if not self.regionIsRect:
                self.monitor = get_primary_monitor()
                return (
                    self.monitorCenterPoint[0] - region[0] / 2,
                    self.monitorCenterPoint[1] - region[1] / 2,
                    region[0],
                    region[1],
                )
            case (None, None, region):
                return region
            case (None, screeninfo.Monitor(_), region) if not self.regionIsRect:
                return (
                    self.monitorCenterPoint[0] - region[0] / 2,
                    self.monitorCenterPoint[1] - region[1] / 2,
                    region[0],
                    region[1],
                )
            case (None, screeninfo.Monitor(_), region) if self.regionIsRect:
                return (
                    self.monitorCenterPoint[0] - region[0] / 2,
                    self.monitorCenterPoint[1] - region[1] / 2,
                    region[2],
                    region[3],
                )
            case (None, monitor, None):
                return (monitor.x, monitor.y, monitor.width, monitor.height)

            case _:
                raise ValueError("Invalid combination of parameters")

    def _execute(self):
        if self.preProcessCallback:
            self.preProcessCallback(self)
        if self.text:
            res = self.ocrMethod(self)
        else:
            res = self.imgMethod(self)
        if self.postProcessCallback:
            self.postProcessCallback(self, res)
        if not res:
            return None

        # relative to interested region
        iregion = self.interestedRegion
        return (res[0] + iregion[0], res[1] + iregion[1])

    def __call__(self, **kwds):
        return self._execute()


def waitFor(token: AutoToken, timeout: float = 10.0, interval: float = 1.1):
    currentTime = time.time()
    while time.time() - currentTime < timeout:
        if not token():
            time.sleep(interval)
        else:
            break

    return token.result


@contextmanager
def repeatWith(token: AutoToken, times: int = 1):
    for _ in range(times):
        yield token()
    return token.result


_cached_memorized_wnd = {}


def memorizedWnd(token: AutoToken):
    raise NotImplementedError
