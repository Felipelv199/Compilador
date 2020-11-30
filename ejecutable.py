class Ejecutable:
    def __init__(self, file):
        self.file = file

    def write_in_document_tags(self, tags):
        while True:
            if len(tags) == 0:
                break
            self.file.write('{}\n'.format(tags.pop(0)))
        self.file.write('@\n')

    def write_in_document_instructions(self, instructions):
        while True:
            if len(instructions) == 0:
                break
            self.file.write('{}\n'.format(instructions.pop(0)))
