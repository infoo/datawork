import jieba
from datawork.other.sqltool import SqlTool, getConnection


# jieba 分词工具
class SegTool(object):

    def __init__(self):
        pass

    @staticmethod
    def cut(text):
        return jieba.cut_for_search(text)

    @staticmethod
    def cut_and_insert_to_seg(text):
        segs = jieba.cut_for_search(text)
        db = SqlTool(getConnection())
        for seg in segs:
            db.insert_seg(seg)
