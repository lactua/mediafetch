from requests import get
from PIL import Image
from io import BytesIO
from subprocess import getoutput
from re import findall
from argparse import ArgumentParser
from .template import template

def mergeStrings(strings, gap):
    strings_lines = list(map(lambda s: s.split('\n'), strings))

    line_count = max(map(lambda s: len(s), strings_lines))
    max_line_lengths = [len(max(string_lines, key=len)) for string_lines in strings_lines]

    output = ""

    for line_index in range(line_count):
        line = ""
        for index, string_lines in enumerate(strings_lines):
            if len(string_lines) > line_index:
                line += string_lines[line_index] + (max_line_lengths[index] - len(string_lines[line_index]) + gap)*" "

        output += line + "\n"
    
    return output

def colorStrings(rgb, text):
    if isinstance(rgb, int):
        rgb = (rgb,)*3

    return f"\033[38;2;{'{:03};{:03};{:03}'.format(*rgb)}m{text}\033[0m"

def getRawImageFromURL(url):
    img_raw = BytesIO(get(url).content)
    return img_raw

def getAsciiImage(img_raw, width):
    img = Image.open(img_raw)

    min_size = min(img.width, img.height)

    img = img.crop(box=(
        (img.width - min_size) / 2,
        (img.height - min_size) / 2,
        (img.width + min_size) / 2,
        (img.height + min_size) / 2,
    ))

    img = img.resize((width, int(width/1.1)))

    width = img.width
    height = img.height

    pixels = img.getdata()

    string = ""
    for line in range(height):
        for column in range(width):
            string += colorStrings(pixels[line*width + column], '\uf0c8') + " "
        string = string.strip()
        string += "\n"

    return string.strip()

def getMetadata(app):
    out = getoutput(f"playerctl -p {app} metadata")

    pattern = "[a-zA-Z]+ [a-zA-Z]+:([a-zA-Z]+)[ ]+(.*)\n"
    regex = findall(pattern, out)

    metadata = {key: value for key, value in regex}

    return metadata

def getPosition(app):
    return float(getoutput(f"playerctl -p {app} position"))

def getStatus(app):
    return getoutput(f"playerctl -p {app} status")

def show(app, shown_infos, ascii_size, sep_gap):
    metadata = getMetadata(app)
    position = getPosition(app)
    status = getStatus(app)

    cover_raw = getRawImageFromURL(metadata['artUrl'])
    ascii_cover = getAsciiImage(cover_raw, ascii_size)

    infos = template(metadata, position, status)

    print(mergeStrings([ascii_cover, infos], sep_gap))


def parseArgs(**kwargs):
    
    parser = ArgumentParser()

    for key, args in kwargs.items():
        parser.add_argument(f"--{key}", **args)

    return parser.parse_args().__dict__

def main():
    args = parseArgs(
        app={"type": str, "required": True},
        sep_gap={"type": int, "default": 5},
        ascii_size={"type": int, "default": 20}
    )

    show(args['app'], ['title', 'artist', 'album'], args['ascii_size'], args['sep_gap'])

if __name__ == "__main__":
    main()