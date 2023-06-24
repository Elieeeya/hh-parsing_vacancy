import json

# Открываем файл QA.json
with open('QA.json', 'r') as file:
    data = json.load(file)

# Инициализируем счетчик навыков
total_skills = 0
skills_count = {}

# Перебираем каждый элемент в файле
for item in data:
    # Проверяем, существует ли ключ "skills" в текущем элементе
    if 'skills' in item:
        skills = item['skills']
        total_skills += len(skills)  # Увеличиваем общий счетчик навыков

        # Перебираем каждый навык в списке навыков
        for skill in skills:
            skills_count[skill] = skills_count.get(skill, 0) + 1  # Увеличиваем счетчик для данного навыка

# Сортируем навыки по возрастанию
sorted_skills = sorted(skills_count.items(), key=lambda x: x[1])

# Выводим результаты в процентном соотношении
for skill, count in sorted_skills:
    percentage = (count / total_skills) * 100
    print(f'{skill}: {percentage:.2f}%')
