import pdfplumber

class Grade():
    def __init__(self, sinf, tur):
        self.sinf=sinf
        self.tur=tur
        self.target=self.sinf+1 if self.tur=="green" else self.sinf
    
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
            self._sinf=value
    
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
        self._tur=value

    @classmethod
    def get(cls):
        sinf = input("Sinf(ex.10): ")
        tur = input("Sinf turi(ex.blue): ")
        return cls(sinf, tur)

def main():
    grade = Grade.get()
    # reader = PdfReader("timetable.pdf")
    # words=[]
    # text = reader.pages[grade.target].extract_text()
    # for word in text.split():
    #     words.append(word)
    # print(words)

if __name__=="__main__":
    main()

