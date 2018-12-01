import csv
import json
import matplotlib.pyplot as plt


def write_to_csv(new_line):
    with open('results.csv', mode='a', newline='',
              encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(new_line)


def create_user(info):
    user = {
        "first name": info[0],
        "last name": info[1],
        "gender": info[2],
        "lang": info[3],
        "answers": [
            info[4],
            info[5],
            info[6],
            info[7],
            info[8],
            info[9]
        ]
    }
    write_to_json(user)


def write_to_json(new_user):
    with open('users_and_results.json', 'r', encoding='utf-8') as file:
        users_list = json.load(file)

    users_list['users'].append(new_user)

    with open('users_and_results.json', 'w', encoding='utf-8') as file:
        json.dump(users_list, file, indent=2, ensure_ascii=False)


def creating_graph():
    users_count = 0
    lang_set = set()
    gender = {
        "male": 0,
        "female": 0,
        "other": 0,
    }
    with open('results.csv', 'r') as file:
        plots = csv.reader(file, delimiter=',')
        next(plots, None)
        for row in plots:
            users_count += 1
            lang_set.add(row[1])
            gender[row[0]] += 1
        fig, ax = plt.subplots()
        group_names = ['users', 'languages', 'Male', 'Female', 'Other']
        group_data = [users_count, len(lang_set), gender['male'],
                      gender['female'], gender['other']]
        ax.barh(group_names, group_data)
        fig.savefig('static/stats.png')


def get_json():
    with open('users_and_results.json', 'r', encoding='utf-8') as file:
        users_list = json.load(file)
    return json.dumps(users_list, indent=2, ensure_ascii=False)


def search(text, list):
    str = []
    with open('users_and_results.json', 'r', encoding='utf-8') as file:
        users_list = json.load(file)
        for element in users_list['users']:
            if (text in element['answers']) & (list[element['gender']]):
                str.append(element['first name'] + ' ' + element['last name'])
    return (str)
