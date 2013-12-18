
## TODO: look at the BRAT source code to see what their parser looks like,
##       could be that we're missing edge cases

import dbutils

class BratAnnotation:
    def __init__(self, annotation_line, text_id, username):
        self.text_id = int(text_id)
        self.username = username
        annnotation_type, markup, word = annotation_line.strip().split('\t')
        label, start, end = markup.split()

        self.label = label
        self.start = int(start)
        self.end = int(end)

    def insert(self, cursor):
        dbutils.insert_into_table(
                cursor=cursor,
                table='text_annotations',
                columns=['text_id','start_pos','end_pos','annotation_type','annotator'],
                values=[self.text_id, self.start, self.end, self.label, self.username])
        

