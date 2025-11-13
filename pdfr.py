import pdfplumber
from pdfplumber.table import TableSettings


class Grade:
    def __init__(self, sinf, tur):
        self.sinf = sinf
        self.tur = tur
        self.target = self.sinf + 1 if self.tur == "green" else self.sinf

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
        sinf = input("Sinf: ") or 10
        tur = input("Sinf turi: ") or "Blue"
        return cls(sinf, tur)


def main():
    grade = Grade.get()
    with pdfplumber.open("timetable.pdf") as pdf:
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

        for day in [monday, tuesday, wednesday, thursday, friday]:
            # print(day)
            for i in range(1, len(day)):
                if not day[i]:
                    continue
                else:
                    attributes = normalize_attributes(day[i].split("\n"))
                    print(i, attributes)


def normalize_attributes(attributes):
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


def is_continuation(attributes):
    if len(attributes) < 3:
        return True
    elif not any(char.isidigit() for char in attributes[0]):
        return True
    else:
        return False


def merge_(day): ...


if __name__ == "__main__":
    main()
