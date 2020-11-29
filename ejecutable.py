class Ejecutable:
    def __init__(self, file):
        self.file = file
        self.number = 0

    def write_in_document(self, operator='', code=''):
        if self.number == 1:
            self.file.write('{},{},{},{},{},{},\n'.format(
                '_P', 'I', 'I', '1', '0', '#'))
            self.file.write('{} {} {}\n'.format('@', '', ''))
        self.file.write('{} {} {}\n'.format(str(self.number), operator, code))
