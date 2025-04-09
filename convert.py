import argparse


def read_file(filename, separators):
    items = []
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

        start = 0
        for i in range(len(content)):
            if content[i] in separators:
                items.append(content[start:i])
                start = i + 1
        items.append(content[start:])
    return items


def intrprt_sep_parse(string):
    return string.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--file-name", required=True, help="The file name with data inside. Ex: file_name.txt")
    parser.add_argument("--separator", default='\n', help="Optional setting for separating different data values. Ex: \\n,./ to separate between newlines, commas, periods, and slashes.")
    parser.add_argument("--convert-to", required=True, choices=['h', 'd', 'b'], help="Convert data to other form based on choice. Ex: b for binary, h for hex, d for decimal.")
    
    args = parser.parse_args()

    file_contents = read_file(args.file_name, intrprt_sep_parse(args.separator))
    print(file_contents)