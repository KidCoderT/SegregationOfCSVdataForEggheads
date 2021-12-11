import csv
from collections import Counter


def simplify_data(data_list):
    new_list = data_list.copy()
    for index in range(len(new_list)):
        new_list[index] = new_list[index][1:-1]
        try:
            new_list[index] = int(new_list[index])
        except:
            pass
    return new_list


def clean_list(data_list):
    copy_data = data_list.copy()
    for item in copy_data:
        duplicate_dict = Counter(item[7:-1])
        if duplicate_dict[''] > 1:
            copy_data.pop(copy_data.index(item))
    return copy_data


def get_data(start, end, list_of_items, header):
    segregated_data = []

    header_fields = []
    for data in header[0:7]:
        header_fields.append(data)
    for data in header[start:end]:
        header_fields.append(data)

    header_fields.pop(0)
    segregated_data.append(simplify_data(header_fields))

    for i in range(len(list_of_items)):
        lines = []
        for data in list_of_items[i][0:7]:
            lines.append(data)
        for data in list_of_items[i][start:end]:
            lines.append(data)

        lines.pop(0)

        segregated_data.append(simplify_data(lines))

    return segregated_data


def write_to_csv(file_name, data):
    with open(f'result/{file_name}', 'w', newline='', encoding='utf-8') as csv_file:
        if len(data) > 0:
            # creating a csv dict writer object
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            writer.writerows(data)
        else:
            csv_file.truncate(0)


def convert_to_dict(list_of_items):
    if len(list_of_items) > 1:
        list_of_dict = []

        keys = list_of_items[0]
        items = list_of_items.copy()
        items.pop(0)

        dictionary = {}
        for item in items:
            for i in range(len(item)):
                dictionary[keys[i]] = item[i]
            list_of_dict.append(dictionary)
            dictionary = {}

        return list_of_dict
    else:
        return []


with open('data.csv', newline='', encoding='utf-8') as csv_file:
    text = csv.reader(csv_file, csv.excel, quotechar='|')
    lines_list = []
    for i in text:
        lines_list.append(i)

    header = lines_list.pop(0)

    parents_response_list = convert_to_dict(clean_list((clean_list(clean_list(get_data(8, 22, lines_list, header))))))
    write_to_csv("parents.csv", parents_response_list)

    children_response_list = convert_to_dict(clean_list(clean_list(get_data(22, 32, lines_list, header))))
    write_to_csv("kids.csv", children_response_list)

    teachers_response_list = convert_to_dict(clean_list(clean_list(clean_list(get_data(32, 39, lines_list, header)))))
    write_to_csv("teachers.csv", teachers_response_list)

    others_response_list = convert_to_dict(clean_list(clean_list(clean_list(get_data(39, -1, lines_list, header)))))
    write_to_csv("others.csv", others_response_list)
