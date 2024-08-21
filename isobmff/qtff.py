# -*- coding: utf-8 -*-
from .box import Box
from .iinf import ItemReferenceBox


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
