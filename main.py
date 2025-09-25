from bs4 import BeautifulSoup
from parse.html_storage import html


def parse_kbt_schedule(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    rows = soup.find_all('tr')

    groups = []
    if rows:
        first_row_cells = rows[0].find_all(['td', 'th'])
        groups = [cell.get_text(strip=True) for cell in first_row_cells[1:]]  # пропускаем "время"

    result = {}

    for row in rows[1:]:
        cells = row.find_all('td')
        if not cells:
            continue

        time_slot = cells[0].get_text(strip=True)

        for i, group in enumerate(groups):
            if i + 1 < len(cells):  # проверяем границы
                lesson = cells[i + 1].get_text(strip=True)

                if group not in result:
                    result[group] = {}

                if lesson:
                    result[group][time_slot] = lesson

    return result


html = html
schedule = parse_kbt_schedule(html)

print("📅 Расписание на 25 сентября - Колледж бизнес-технологий\n")

for group, lessons in schedule.items():
    print(f"👥 Группа: {group}")
    print("-" * 50)

    for time in sorted(lessons.keys(), key=int):
        lesson_info = lessons[time]
        if 'ауд.' in lesson_info or 'Ауд.' in lesson_info:
            parts = lesson_info.split('ауд.' if 'ауд.' in lesson_info else 'Ауд.')
            subject_teacher = parts[0].strip()
            classroom = 'ауд.' + parts[1].strip() if len(parts) > 1 else ''
            print(f"   {time} пара: {subject_teacher} | {classroom}")
        else:
            print(f"   {time} пара: {lesson_info}")

    print()