from ctypes import HRESULT
from ctypes import POINTER
from ctypes import c_int
from dataclasses import dataclass
from typing import Any

from comtypes import COMMETHOD  # type: ignore
from comtypes import GUID
from comtypes import CoInitialize
from comtypes import COMError
from comtypes import IUnknown
from comtypes import client
from comtypes.persist import IPropertyBag

from opencv_cam_idx.moniker import IEnumMoniker


class clsids:
    CLSID_FilterGraph = "{E436EBB3-524F-11CE-9F53-0020AF0BA770}"
    CLSID_SystemDeviceEnum = "{62BE5D10-60EB-11d0-BD3B-00A0C911CE86}"
    CLSID_SampleGrabber = "{C1F400A0-3F08-11d3-9F0B-006008039E37}"
    CLSID_CaptureGraphBuilder2 = "{BF87B6E1-8C27-11d0-B3F0-00AA003761C5}"
    CLSID_VideoRendererDefault = "{6BC1CFFA-8FC1-4261-AC22-CFB4CC38DB50}"
    CLSID_NullRender = "{C1F400A4-3F08-11D3-9F0B-006008039E37}"
    CLSID_VideoMixingRenderer = "{B87BEB7B-8D29-423f-AE4D-6582C10175AC}"
    CLSID_SmartTee = "{CC58E280-8AA1-11d1-B3F1-00AA003761C5}"


class DeviceCategories:
    VideoInputDevice = "{860bb310-5d01-11d0-bd3b-00a0c911ce86}"
    AudioInputDevice = "{33d9a762-90c8-11d0-bd43-00a0c911ce86}"
    VideoCompressor = "{33d9a760-90c8-11d0-bd43-00a0c911ce86}"
    AudioCompressor = "{33d9a761-90c8-11d0-bd43-00a0c911ce86}"
    LegacyAmFilter = "{083863F1-70DE-11d0-BD40-00A0C911CE86}"


class ICreateDevEnum(IUnknown):
    _case_insensitive_ = True
    _iid_ = GUID("{29840822-5B84-11D0-BD3B-00A0C911CE86}")
    _idlflags_ = []

    _methods_ = [
        COMMETHOD(
            [],
            HRESULT,
            "CreateClassEnumerator",
            (["in"], POINTER(GUID), "clsidDeviceClass"),
            (["out"], POINTER(POINTER(IEnumMoniker)), "ppEnumMoniker"),
            (["in"], c_int, "dwFlags"),
        )
    ]


@dataclass
class Camera:
    idx: int
    friendly_name: str
    device_path: str
    description: str


def find_cameras():
    # Reference
    # https://learn.microsoft.com/en-us/windows/win32/directshow/selecting-a-capture-device

    CoInitialize()  # fixes CoInitialize has not been called
    system_device_enum: Any = client.CreateObject(
        clsids.CLSID_SystemDeviceEnum, interface=ICreateDevEnum
    )
    filter_enumerator = system_device_enum.CreateClassEnumerator(
        GUID(DeviceCategories.VideoInputDevice), dwFlags=0
    )
    cameras: list[Camera] = []
    idx = 0
    while True:
        try:
            moniker, _ = filter_enumerator.Next(1)
            property_bag = moniker.BindToStorage(
                0, 0, GUID("{55272A00-42CB-11CE-8135-00AA004BB851}")
            ).QueryInterface(IPropertyBag)
            try:
                friendly_name = property_bag.Read(
                    "FriendlyName", pErrorLog=None
                )
            except COMError:
                friendly_name = ""

            try:
                device_path = property_bag.Read("DevicePath", pErrorLog=None)
            except COMError:
                device_path = ""

            try:
                description = property_bag.Read("Description", pErrorLog=None)
            except COMError:
                description = ""

            cameras.append(
                Camera(
                    idx=idx,
                    friendly_name=friendly_name,
                    device_path=device_path,
                    description=description,
                )
            )
            idx += 1
        except ValueError:
            break
    return cameras
