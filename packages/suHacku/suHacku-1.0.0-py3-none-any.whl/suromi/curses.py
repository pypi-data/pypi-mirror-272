class curso:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"\n{self.name} | [{self.duration}] hrs | [!URL] {self.link}"

courser = [
    curso("intro a linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    curso("intro al hacking etico", 53, "https://hack4u.io/cursos/introduccion-al-hacking/"),
    curso("personalizacion de entorno linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/")
]


def list_curse():
    for i in courser:
        print(i)

def search_curse(name):
    for i in courser:
        if i.name == name:
            return(i)
    return None
