# -*- coding: utf-8 -*-
from .box import FullBox


# ISO/IEC 14496-12:2022, Section 6.2.2
class ObjectDescriptorBox(FullBox):
    box_type = "iods"
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
