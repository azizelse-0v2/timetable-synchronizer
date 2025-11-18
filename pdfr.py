import pdfplumber
from pdfplumber.table import TableSettings


class Grade:
    def __init__(self, sinf, tur):
        self.sinf = sinf
        self.tur = tur
        self.target = (self.sinf - 5) * 2 + (0 if self.tur == "blue" else 1)

    def __str__(self):
        return f"{self.sinf} {self.tur}"

    @property
    def sinf(self):
        return self._sinf

    @sinf.setter
    def sinf(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError("Must be int!")
        else:
            if value < 5 or value > 11:
                raise ValueError("Must be between 5 and 11!")
            else:
                self._sinf = value

    @property
    def tur(self):
        return self._tur

    @tur.setter
    def tur(self, value):
        if not isinstance(value, str):
            raise ValueError("Must be str!")
        value = value.lower().strip()
        if value not in ("blue", "green"):
            raise ValueError("Must be blue or green!")
        self._tur = value

    @classmethod
    def get(cls):
        sinf = input("Sinf: ")
        tur = input("Sinf turi: ")
        return cls(sinf, tur)


def main():
    grade = Grade.get()
    days = extract_pdf_info("timetable.pdf", grade)
    output_info(days)


def output_info(days):
    for day_index in range(len(days)):
        day = days[day_index]
        for lesson_index, lesson in enumerate(
            day, start=1
        ):  # day = {"lesson_info":list(), "double_lesson":bool}
            print(lesson_index, lesson["lesson_info"], lesson["double_lesson"])
        print("---------------------------------")


def extract_pdf_info(pathway, grade):
    with pdfplumber.open(pathway) as pdf:
        page = pdf.pages[grade.target]

        table_settings = {
            "vertical_strategy": "lines",
            "horizontal_strategy": "lines",
            "intersection_x_tolerance": 10,
            "intersection_y_tolerance": 10,
            "snap_x_tolerance": 3,
            "snap_y_tolerance": 3,
            "join_x_tolerance": 15,
            "join_y_tolerance": 15,
            "edge_min_length": 20,
            "min_words_vertical": 3,
            "min_words_horizontal": 3,
        }

        # Extract table data (not for drawing)
        tables = page.extract_tables(table_settings)

        monday, tuesday, wednesday, thursday, friday = [], [], [], [], []
        for table in tables:
            for row in table:
                for lst, val in zip(
                    [monday, tuesday, wednesday, thursday, friday], row[1:6]
                ):
                    lst.append(val)

        days = [monday, tuesday, wednesday, thursday, friday]

        for day_index in range(len(days)):
            day = days[day_index]
            day = extract_day_info(day)
            days[day_index] = day
    return days


def extract_day_info(day):
    day = clean_day(day)
    day = multiline_processing(day)
    day = merge_day(day)
    return day


def multiline_processing(day):
    for i in range(len(day)):
        lesson = day[i]
        attrs = multiline_lesson_handling(lesson.split("\n"))
        day[i] = "\n".join(attrs)
    return day


def merge_day(day):
    merged = []
    i = 0
    while i < len(day):
        current_parts = day[i].split("\n")
        double = False

        if i + 1 < len(day):
            next_parts = day[i + 1].split("\n")

            # Merge logic preserving rooms and teachers
            if len(current_parts) in (1, 2):
                # Room is always first of current_parts
                room = current_parts[0]

                # Subject(s): combine current and next
                subject_middle = (
                    " ".join(current_parts[1:] + next_parts[:-1])
                    if len(current_parts) > 1
                    else next_parts[:-1]
                )
                subject = (
                    " ".join(subject_middle).strip()
                    if isinstance(subject_middle, list)
                    else subject_middle
                )

                # Teacher: last element of next_parts
                teacher = next_parts[-1] if next_parts else ""

                # Merge into normalized list
                merged_text = [room, subject, teacher]
                double = True
                i += 2
                merged.append({"lesson_info": merged_text, "double_lesson": double})
                continue

        # Single lesson, keep as-is
        merged_text = current_parts
        merged.append({"lesson_info": merged_text, "double_lesson": double})
        i += 1

    return merged


def clean_day(day):
    cleaned = []
    for lesson in day:
        text = str(lesson).strip()
        if (
            text
            in (
                "L U N C H",
                "B R E A K",
                "S N A C K B R E A K",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
            )
            or not lesson
        ):
            continue
        cleaned.append(lesson)
    return cleaned


def multiline_lesson_handling(attributes):
    if len(attributes) > 3:
        attributes = [
            attribute.strip()
            for attribute in attributes
            if attribute and attribute.strip()
        ]
        middle = " ".join(attributes[1:-1])
        return [attributes[0], middle, attributes[-1]]
    else:
        return attributes


if __name__ == "__main__":
    main()
