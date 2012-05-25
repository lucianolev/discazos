import xml.dom.minidom

def import_disc_info(xml_file):
    xmlTree = xml.dom.minidom.parse(xml_file)
    discsXml = xmlTree.getElementsByTagName("disc")
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