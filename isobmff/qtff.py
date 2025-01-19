# -*- coding: utf-8 -*-
from .box import Box
from .box import ContainerBox
from .box import FullBox
from .iinf import ItemReferenceBox
from .utils import read_fixed_size_string
from .utils import read_sint
from .utils import read_uint


# QuickTime Tags
# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeWide(Box):
    box_type = b"wide"


# QuickTime ImageDesc Tags
# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeStereoscopic3D(Box):
    box_type = b"st3d"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeSphericalVideo(Box):
    box_type = b"sv3d"


# QuickTime ItemRef Tags
# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class AuxiliaryImageRef(ItemReferenceBox):
    box_type = b"auxl"


# QuickTime ItemRef Tags
# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class DerivedImageRef(ItemReferenceBox):
    box_type = b"dimg"


# QuickTime ItemRef Tags
# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class ThumbnailRef(ItemReferenceBox):
    box_type = b"thmb"


# QuickTime ItemRef/TrackRef Tags
# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeContentDescribes(Box):
    box_type = b"cdsc"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeChapterListTrackID(Box):
    box_type = b"chap"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeElementaryStreamTrack(Box):
    box_type = b"mpod"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeTimeCode(Box):
    box_type = b"tmcd"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeItemList(Box):
    box_type = b"ilst"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeChapterList(Box):
    box_type = b"chpl"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeTags(Box):
    box_type = b"TAGS"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeTx3g(Box):
    box_type = b"tx3g"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeUserName(Box):
    box_type = b"name"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeIndependentAndDisposableSamples(Box):
    box_type = b"sdtp"


# QuickTime SampleTable Tags
# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeSampleToGroup(Box):
    box_type = b"sbgp"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeSamplePaddingBits(Box):
    box_type = b"padb"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeGenMediaHeader(Box):
    box_type = b"gmhd"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeVideoFieldOrder(Box):
    box_type = b"fiel"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeCodeVersion(Box):
    box_type = b"cver"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeAudibleTags(Box):
    box_type = b"tags"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeTrackAperture(Box):
    box_type = b"tapt"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimePlayMode(Box):
    box_type = b"SDLN"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeInformation(Box):
    box_type = b"\xa9inf"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeFormat(Box):
    box_type = b"\xa9fmt"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeRequirements(Box):
    box_type = b"\xa9req"


# QuickTime ItemList Tags
# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeProductVersion(Box):
    box_type = b"VERS"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeEncoderID(Box):
    box_type = b"\xa9enc"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeStartTimecode(Box):
    box_type = b"\xa9TIM"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeStartTimeScale(Box):
    box_type = b"\xa9TSC"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeStartTimeSampleSize(Box):
    box_type = b"\xa9TSZ"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeGPSCoordinates(Box):
    box_type = b"\xa9xyz"


# QuickTime UserData Tags
# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeHintInfo(Box):
    box_type = b"hnti"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeSamsungSmta(Box):
    box_type = b"smta"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeRicohRMKN(Box):
    box_type = b"RMKN"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimePreviewImage(Box):
    box_type = b"RTHU"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeContentCreateDate(Box):
    box_type = b"@day"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeMake(Box):
    box_type = b"@make"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeModel(Box):
    box_type = b"@mod"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeSamsungSec(Box):
    box_type = b"@sec"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeSoftwareVersion(Box):
    box_type = b"@swr"


# https://metacpan.org/dist/Image-ExifTool/view/lib/Image/ExifTool/TagNames.pod
class QuickTimeGPSCoordinates2(Box):
    box_type = b"@xyz"


# ISO Base Media File Format and Apple HEVC Stereo Video, version 0.9 (beta)


# aligned(8) class VideoExtendedUsageBox extends Box('vexu') {
#   RequiredBoxTypesBox(); // optional if no required boxes specified
#   StereoViewBox(); // optional
#   Box()[]; // other optional boxes with FreeSpaceBox() reserved for its expected use
# }
class VideoExtendedUsageBox(Box):
    box_type = b"vexu"

    def read(self, file):
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# aligned(8) class StereoViewBox extends Box('eyes') {
#   RequiredBoxTypesBox(); // as needed
#   StereoViewInformationBox();
#   HeroStereoEyeDescriptionBox(); // optional
#   Box()[]; // other optional boxes
# }
class StereoViewBox(Box):
    box_type = b"eyes"

    def read(self, file):
        self.box_list = self.read_box_list(file)

    def contents(self):
        tuples = super().contents()
        for idx, box in enumerate(self.box_list):
            tuples += ((f"box[{idx}]", box.contents()),)
        return tuples


# aligned(8) class RequiredBoxTypesBox extends FullBox('must', 0, 0 ) {
#   unsigned int(32) required_box_types[];
# }
class RequiredBoxTypesBox(FullBox):
    box_type = b"must"

    def read(self, file):
        self.required_box_types = []
        while file.tell() < self.max_offset:
            self.required_box_types.append(read_sint(file, 4))

    def contents(self):
        tuples = super().contents()
        for idx, val in enumerate(self.required_box_types):
            tuples += ((f"required_box_types[{idx}]", val),)
        return tuples


# aligned(8) class StereoViewInformationBox extends FullBox('stri', 0, 0) {
#   unsigned int(4) reserved; // reserved, set to 0
#   unsigned int(1) eye_views_reversed;
#   unsigned int(1) has_additional_views;
#   unsigned int(1) has_right_eye_view; // video contains a right-eye view
#   unsigned int(1) has_left_eye_view; // video contains a left-eye view
# }
class StereoViewInformationBox(FullBox):
    box_type = b"stri"

    def read(self, file):
        byte = read_uint(file, 1)
        self.reserved = (byte >> 4) & 0b1111
        self.eye_views_reversed = (byte >> 3) & 0b1
        self.has_additional_views = (byte >> 2) & 0b1
        self.has_right_eye_view = (byte >> 1) & 0b1
        self.has_left_eye_view = (byte >> 0) & 0b1

    def contents(self):
        # a non-Box class has no parent
        tuples = ()
        tuples += (("eye_views_reversed", self.eye_views_reversed),)
        tuples += (("has_additional_views", self.has_additional_views),)
        tuples += (("has_right_eye_view", self.has_right_eye_view),)
        tuples += (("has_left_eye_view", self.has_left_eye_view),)


# aligned(8) class HeroStereoEyeDescriptionBox extends FullBox('hero', 0, 0) {
#   unsigned int(8) hero_eye_indicator; // 0 = none, 1 = left, 2 = right, >= 3 reserved
# }
class HeroStereoEyeDescriptionBox(FullBox):
    box_type = b"hero"

    def read(self, file):
        self.hero_eye_indicator = read_uint(file, 1)

    def contents(self):
        # a non-Box class has no parent
        tuples = ()
        tuples += (("hero_eye_indicator", self.hero_eye_indicator),)


# https://github.com/FFmpeg/FFmpeg/commit/8e7ca22b36e7727d0778d8604b29f81ca1202f19
class HorizontalFieldOfViewBox(Box):
    box_type = b"hfov"

    def read(self, file):
        self.horizontal_field_of_view = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("horizontal_field_of_view", self.horizontal_field_of_view),)
        return tuples


# other stereo-related boxes
class CAMSUnknown(ContainerBox):
    box_type = b"cams"


class CMFYUnknown(ContainerBox):
    box_type = b"cmfy"


class ProjUnknown(ContainerBox):
    box_type = b"proj"


class BlinUnknown(FullBox):
    box_type = b"blin"

    def read(self, file):
        self.stereo_baseline = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("stereo_baseline", self.stereo_baseline),)
        return tuples


class DadjUnknown(FullBox):
    box_type = b"dadj"

    def read(self, file):
        self.stereo_horizontal_disparity_adjustment = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (
            (
                "stereo_horizontal_disparity_adjustment",
                self.stereo_horizontal_disparity_adjustment,
            ),
        )
        return tuples


class PrjiUnknown(FullBox):
    box_type = b"prji"

    def read(self, file):
        self.spherical_mapping_projection = read_fixed_size_string(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (
            (
                "spherical_mapping_projection",
                self.spherical_mapping_projection,
            ),
        )
        return tuples
