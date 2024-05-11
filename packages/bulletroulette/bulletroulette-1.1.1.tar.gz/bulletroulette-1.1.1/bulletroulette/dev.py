from os.path import dirname

with open(f"{dirname(__file__)}/../README.md", "r", encoding="utf-8") as fh:
    readmetxt = fh.read()
with open(f"{dirname(__file__)}/../LICENSE", "r", encoding="utf-8") as fh:
    licensetxt = fh.read()

def run():
    def readme():print(readmetxt)
    def license():print(licensetxt)
    while True:
        exec(input("(roulette)>>> "))