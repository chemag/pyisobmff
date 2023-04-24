# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint
from .box import read_bytes
from .box import read_utf8string


# ISO/IEC 14496-12:2022, Section 7.2.6.5
class ES_Descriptor:
    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        self.ES_ID = read_uint(file, 2)
        byte1 = read_uint(file, 1)
        self.streamDependenceFlag = (byte1 >> 7) & 0x01
        self.URL_Flag = (byte1 >> 6) & 0x01
        self.OCRstreamFlag = (byte1 >> 5) & 0x01
        self.length_size = byte1 & 0x1F
        if self.streamDependenceFlag:
            self.dependsOn_ES_ID = read_uint(file, 2)
        if self.URL_Flag:
            self.URLlength = read_uint(file, 1)
            self.URLstring = read_utf8string(file, self.URLlength)
        if self.OCRstreamFlag:
            self.OCR_ES_Id = read_uint(file, 2)
        # TODO(chema): implement the rest
        # DecoderConfigDescriptor decConfigDescr
        # if (ODProfileLevelIndication == 0x01:
        #    # no SL extension
        #    SLConfigDescriptor slConfigDescr
        # else:
        #    # SL extension is possible
        #    SLConfigDescriptor slConfigDescr;
        # IPI_DescrPointer ipiPtr[0 .. 1];
        # IP_IdentificationDataSet ipIDS[0 .. 255];
        # IPMP_DescriptorPointer ipmpDescrPtr[0 .. 255];
        # LanguageDescriptor langDescr[0 .. 255];
        # QoS_Descriptor qosDescr[0 .. 1];
        # RegistrationDescriptor regDescr[0 .. 1];
        self.rem = read_bytes(file, self.max_offset - file.tell())

    def contents(self):
        # a non-Box class has no parent
        tuples = ()
        tuples += (("ES_ID", self.ES_ID),)
        tuples += (("streamDependenceFlag", self.streamDependenceFlag),)
        tuples += (("URL_Flag", self.URL_Flag),)
        tuples += (("OCRstreamFlag", self.OCRstreamFlag),)
        tuples += (("length_size", self.length_size),)
        if self.streamDependenceFlag:
            tuples += (("dependsOn_ES_ID", self.dependsOn_ES_ID),)
        if self.URL_Flag:
            tuples += (("URLlength", self.URLlength),)
            tuples += (("URLstring", self.URLstring),)
        if self.OCRstreamFlag:
            tuples += (("OCR_ES_Id", self.OCR_ES_Id),)
        tuples += (("rem", self.rem),)
        return tuples


# ISO/IEC 14496-12:2022, Section 6.2.2
class ObjectDescriptorBox(FullBox):
    box_type = b"iods"
    # TODO(chema): not clear how to implement ObjectDescriptor
    # ISO/IEC 14496-1:2014 Section 7.2.6.3
    # class ObjectDescriptor extends ObjectDescriptorBase : bit(8) tag=ObjectDescrTag {
    #   bit(10) ObjectDescriptorID;
    #   bit(1) URL_Flag;
    #   const bit(5) reserved=0b1111.1;
    #   if (URL_Flag) {
    #     bit(8) URLlength;
    #     bit(8) URLstring[URLlength];
    #   } else {
    #     ES_Descriptor esDescr[1 .. 255];
    #     OCI_Descriptor ociDescr[0 .. 255];
    #     IPMP_DescriptorPointer ipmpDescrPtr[0 .. 255];
    #     IPMP_Descriptor ipmpDescr [0 .. 255];
    #   }
    #   ExtensionDescriptor extDescr[0 .. 255];
    # }
