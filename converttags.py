class ConvertTags:
    """
    Replace targeted tags in source file, and generate a result file.
    """

    def __init__(self, sourcefile, resultfile):
        self.sourcefile = sourcefile
        self.resultfile = resultfile

    def replace_tags(self, tags_dic):
        """
        :param tags_dic: a dic of pairs of old:new words
        :return: True
        """
        # open files
        file2 = open(self.resultfile, "w", encoding='utf-8')
        for line in open(self.sourcefile, encoding='utf-8'):
            for old, new in tags_dic.items():
                line = line.replace(old, new)
            file2.write(line)
        file2.close()
        return True

# For reference:
# from converttags import ConvertTags
# converting = ConvertTags('test_iob.txt', 'test_result.txt')
# replacewords = {'B-PERSON':'B-PER', 'I-PERSON':'I-PER'}
# converting.replace_tags(replacewords)