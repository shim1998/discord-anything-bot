import string

Genshin_Characters = [
    'Childe',
    'Nahida',
    'Keqing',
    'Ayato',
    'Beidou',
    'Mona',
    'Lisa',
    'Bennett',
    'Ganyu',
    'Kazuha',
    'Candace',
    'Kokomi',
    'Baizhu',
    'Fischl',
    'Heizou',
    'Barbara',
    'Lumine',
    'Zhongli',
    'Sayu',
    'Arlecchino',
    'Sandrone',
    'Aether',
    'Klee',
]


def get_list():
    lines_list = []
    with open('tweets.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            new_lines = line.translate(str.maketrans('', '', string.punctuation))
            new_lines = new_lines.split()
            new_lines = new_lines[:-1]
            new_lines = [word if word not in Genshin_Characters else -1 for word in new_lines]
            lines_list.append(new_lines)
    return lines_list
