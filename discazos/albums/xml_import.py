# -*- encoding: utf-8 -*-

import xml.dom.minidom
from xml.parsers.expat import ExpatError 

CREATOR_XML_CURRENT_VER = "0.3"

class InvalidXMLFile(Exception):
    pass

class UnsupportedCreatorVersion(Exception):
    pass

class DiscazosCreatorXML(object):

    @classmethod
    def load_from_file(cls, xml_file):
        importTool = cls()
        try:
            importTool.xmlTree = xml.dom.minidom.parse(xml_file)
            importTool.check_file_version()
            return importTool
        except ExpatError:
            raise InvalidXMLFile("The file supplied is not a valid XML file.")
    
    def check_file_version(self):
        creatorXml = self.xmlTree.getElementsByTagName("discazos-disc-creator")[0]
        version = creatorXml.getAttribute("version")
        if version != CREATOR_XML_CURRENT_VER:
             raise UnsupportedCreatorVersion("El archivo XML provisto fue creado " \
                                             "con una versión actualmente no " \
                                             "soportada de Discazos Creator.")
        return True
    
    def get_audiofile_size(self):
        audiofileXml = self.xmlTree.getElementsByTagName("audiofile")[0]
        return audiofileXml.getAttribute("size")
    
    def get_album_title(self):
        albumXml = self.xmlTree.getElementsByTagName("album")[0]
        return albumXml.getAttribute("title")
    
    def get_discs_info(self):
        discsXml = self.xmlTree.getElementsByTagName("disc")
        discs = []
        for discXml in discsXml:
            #save the disc info
            disc = {}
            disc['number'] = discXml.getAttribute("number")
            disc['title'] = discXml.getAttribute("title")
            #save the tracks info
            tracks = []
            tracksXml = discXml.getElementsByTagName("track")
            for trackXml in tracksXml:
                discTrack = {}
                discTrack['number'] = trackXml.getAttribute("number");
                artistXml = trackXml.getElementsByTagName("artist")[0]
                discTrack['artist'] = artistXml.getAttribute("name")
                songXml = trackXml.getElementsByTagName("song")[0]
                discTrack['song'] = songXml.getAttribute("name")
                discTrack['length'] = trackXml.getAttribute("length")
                tracks.append(discTrack)
            discs.append((disc, tracks))
        return discs
