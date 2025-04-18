from PIL import Image
from pillow_heif import register_heif_opener
import argparse
import webbrowser


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image.getexif().get_ifd(0x8825)


def get_geotagging(exif):
    geo_tagging_info = {}
    if not exif:
        raise ValueError("No EXIF metadata found")
    else:
        gps_keys = ['GPSVersionID', 'GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude',
                    'GPSAltitudeRef', 'GPSAltitude', 'GPSTimeStamp', 'GPSSatellites', 'GPSStatus', 'GPSMeasureMode',
                    'GPSDOP', 'GPSSpeedRef', 'GPSSpeed', 'GPSTrackRef', 'GPSTrack', 'GPSImgDirectionRef',
                    'GPSImgDirection', 'GPSMapDatum', 'GPSDestLatitudeRef', 'GPSDestLatitude', 'GPSDestLongitudeRef',
                    'GPSDestLongitude', 'GPSDestBearingRef', 'GPSDestBearing', 'GPSDestDistanceRef', 'GPSDestDistance',
                    'GPSProcessingMethod', 'GPSAreaInformation', 'GPSDateStamp', 'GPSDifferential']

        for k, v in exif.items():
            try:
                geo_tagging_info[gps_keys[k]] = str(v)
            except IndexError:
                pass
        return geo_tagging_info


if __name__ == '__main__':
    register_heif_opener()

    parser = argparse.ArgumentParser()
    parser.add_argument("--file-name", required=True, help="Enter .heic file here.")
    args = parser.parse_args()

    my_image = args.file_name
    image_info = get_exif(my_image)
    results = get_geotagging(image_info)
    print(results)


    if input("Open in Google Maps? (y/*): ").lower() == 'y':
        latitude = results["GPSLatitude"].strip('()').split(',')
        longitude = results["GPSLongitude"].strip('()').split(',')
        lat = float(latitude[0]) + float(latitude[1])/60 + float(latitude[2])/3600
        lon = float(longitude[0]) + float(longitude[1])/60 + float(longitude[2])/3600

        url = f"https://www.google.com/maps/search/?api=1&query={lat}{results["GPSLatitudeRef"]},{lon}{results["GPSLongitudeRef"]}"
        webbrowser.open(url)

