import pandas as pd
from io import StringIO

header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>TRACKS 18.01 KML.kml</name>
	<open>1</open>
	<Style id="s_ylw-pushpin">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ff1451d6</color>
		</LineStyle>
		<PolyStyle>
			<color>ff0e319a</color>
			<fill>0</fill>
		</PolyStyle>
	</Style>
	<Style id="s_ylw-pushpin_hl">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ff1451d6</color>
		</LineStyle>
		<PolyStyle>
			<color>ff0e319a</color>
			<fill>0</fill>
		</PolyStyle>
	</Style>
	<Style id="s_ylw-pushpin0">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ffdfdfdf</color>
		</LineStyle>
		<PolyStyle>
			<color>ffebebeb</color>
			<fill>0</fill>
		</PolyStyle>
	</Style>
	<Style id="s_ylw-pushpin_hl0">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ffdfdfdf</color>
		</LineStyle>
		<PolyStyle>
			<color>ffebebeb</color>
			<fill>0</fill>
		</PolyStyle>
	</Style>
	<StyleMap id="m_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#s_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#s_ylw-pushpin_hl</styleUrl>
		</Pair>
	</StyleMap>
	<StyleMap id="m_ylw-pushpin0">
		<Pair>
			<key>normal</key>
			<styleUrl>#s_ylw-pushpin0</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#s_ylw-pushpin_hl0</styleUrl>
		</Pair>
	</StyleMap>
"""
ending = """</Document>
</kml>
"""


def gen_placemark(is_valid, coords, track_id, name):
    placemark = "<Placemark>/n" + "<name>{} {}</name>\n".format(track_id, name)
    placemark += "<styleUrl>{}</styleUrl>\n".format(("#m_ylw-pushpin0" if is_valid else "#m_ylw-pushpin"))
    placemark += """<LineString>
<extrude>1</extrude>
<altitudeMode>relativeToGround</altitudeMode>
<coordinates>\n"""
    placemark += coords + """\n</coordinates>
</LineString>
</Placemark>"""
    return placemark


def gen_folder(is_valid, file):
    folder = """<Folder>
    <name>""" + ("good tracks" if is_valid else "bad tracks") + "</name>\n"
    # cycle
    data = pd.read_csv(StringIO(file), sep=' ', header=None,
                       names=['time', 'id', 'latitude', 'longitude', 'elevation', 'code', 'name'])
    grouped = data.groupby('id')
    for track_id, track in grouped:
        coords = ""
        for _, row in track.iterrows():
            coords += "{},{},{} ".format(row['longitude'], row['latitude'], row['elevation'])
        folder += gen_placemark(is_valid, coords, track_id, track.iloc[0]['name'])
    folder += "</Folder>\n"
    return folder


def gen_kml(goodTracksFile, badTracksFile):
    return header + gen_folder(True, goodTracksFile) + gen_folder(False, badTracksFile) + ending
