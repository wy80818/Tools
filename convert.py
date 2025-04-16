import argparse


def read_file(filename, separators):
    items = []
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        start = 0
        for i in range(len(content)):
            if content[i] in separators:
                items.append(reformat_item(content[start:i].strip()))
                start = i + 1
        if i > start:
            items.append(reformat_item(content[start:i+1].strip()))
        
    print_items(items)
    return items


def print_items(items):
    print("Detected items: ")
    for i, item in enumerate(items):
        print(item, end=", ")
    print()


def reformat_item(item):
    if item[:2] == '0x' or item[:2] == '0b':
        return item[2:]
    return item


def intrprt_sep_parse(string):
    return string.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')


def convert_file_contents(items, conv_from, conv_to):
    try:  
        for i in range(len(items)):
            if conv_from == 'b':
                if conv_to == 'd':
                    items[i] = str(int(items[i], 2))
                elif conv_to == 'h': 
                    items[i] = str(hex(int(items[i], 2)))
            elif conv_from == 'h':
                if conv_to == 'd':
                    items[i] = str(int(items[i], 16))
                elif conv_to == 'b':
                    items[i] = str(bin(int(items[i], 16)))
            else:
                if conv_to == 'h':
                    items[i] = str(hex(int(items[i])))
                elif conv_to == 'b':
                    items[i] = str(bin(int(items[i])))
    except ValueError:
        return f"{items[i]} could not be converted!"

    return "Completed conversion"


def write_file(conv_option, filename, items):
    if filename.startswith("b_") or filename.startswith("d_") or filename.startswith("h_"):
        filename = filename[2:]
        
    new_name = conv_option + "_" + filename
    with open(new_name, "w", encoding="utf-8") as file:
        for i in range(len(items)):
            if i < len(items) - 1:
                file.write(f"{items[i]}\n")
            else:
                file.write(f"{items[i]}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--file-name", required=True, help="The file name with data inside. Ex: file_name.txt")
    parser.add_argument("--separator", default='\n', help="Optional setting for separating different data values. Ex: \\n,./ to separate between newlines, commas, periods, and slashes.")
    parser.add_argument("--convert-from", required=True, choices=['d', 'h', 'b'], help="The data you are converting FROM. Ex: Ex: b for binary, h for hex, d for decimal.")
    parser.add_argument("--convert-to", required=True, choices=['d', 'h', 'b'], help="The data you are converting TO. Ex: b for binary, h for hex, d for decimal.")

    args = parser.parse_args()

    file_contents = read_file(args.file_name, intrprt_sep_parse(args.separator))

    print(convert_file_contents(file_contents, args.convert_from, args.convert_to))

    write_file(args.convert_to, args.file_name, file_contents)

