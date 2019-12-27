import os
import ahocorasick

class questionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.paper_path=os.path.join(cur_dir, './paper_search/paper_graph/dict/paper.txt')
        self.journal_path = os.path.join(cur_dir, './paper_search/paper_graph/dict/journal.txt')
        self.author_path = os.path.join(cur_dir, './paper_search/paper_graph/dict/author.txt')
        self.unit_path = os.path.join(cur_dir, './paper_search/paper_graph/dict/unit.txt')

        self.paper_words = [i.strip() for i in open(self.paper_path, encoding='UTF-8') if i.strip()]  # .strip()除去首尾的空格
        self.journal_words = [i.strip() for i in open(self.journal_path, encoding='UTF-8') if i.strip()]
        self.author_words = [i.strip() for i in open(self.author_path, encoding='UTF-8') if i.strip()]
        self.unit_words = [i.strip() for i in open(self.unit_path, encoding='UTF-8') if i.strip()]

        self.build_actree()#创建 ac自动机
        #问句疑问词  六类问题
        self.work_qwds=['工作','单位']#作者--单位
        self.publish_qwds=['发表过','写过','写的']#作者--论文
        self.belongto_qwds=['是谁','发表的']#论文--作者
        self.subject_qwds=['学科','哪一类']#论文--学科
        self.journal_qwds=['刊物','期刊']#论文--期刊
        self.carry_qwds=['刊登']#期刊--论文
        self.atoa_qwds=['共同','协作']#作者--作者



    def build_actree(self):#创建ac自动机
        self.actree = ahocorasick.Automaton()
        for index, word in enumerate(self.paper_words):
            self.actree.add_word(word, (index, word,'paper'))
        for index, word in enumerate(self.journal_words):
            self.actree.add_word(word, (index, word,'journal'))
        for index, word in enumerate(self.author_words):
            self.actree.add_word(word, (index, word,'author'))
        for index, word in enumerate(self.unit_words):
            self.actree.add_word(word, (index, word,'unit'))
        self.actree.make_automaton()
        return
    def classifer_main(self,question):
        data={}
        #收集问句当中所涉及到的实体类型

        wds=self.check_types(question)
        author_count=0
        types=[]
        for i in wds:
            types.append(i[1])
            if i[1]=='author':
                author_count+=1
        question_types=[]
        if self.check_words(self.work_qwds, question) and ('author' in types):
            question_type = '作者--单位'
            question_types.append(question_type)
        if self.check_words(self.publish_qwds, question) and ('author' in types):
            question_type = '作者--论文'
            question_types.append(question_type)
        if self.check_words(self.belongto_qwds, question) and ('paper' in types):
            question_type = '论文--作者'
            question_types.append(question_type)
        if self.check_words(self.subject_qwds, question) and ('paper' in types):
            question_type = '论文--学科'
            question_types.append(question_type)
        if self.check_words(self.journal_qwds, question) and ('paper' in types):
            question_type = '论文--期刊'
            question_types.append(question_type)
        if self.check_words(self.carry_qwds, question) and ('journal' in types):
            question_type = '期刊--论文'
            question_types.append(question_type)
        if author_count==2 and self.check_words(self.atoa_qwds, question):
            question_type='作者--作者'
            question_types.append(question_type)
        data['wds'] = wds
        data['question_types']=question_types
        return data


    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

    def check_types(self, question):
        wds = []
        for i in self.actree.iter(question):
            word = i[1][1]#i[1][0]为index   i[1][1]为words
            category=i[1][2]
            wds.append([word,category])
        # 附加功能：可能出现一个词分成几个部分，把这个部分过滤掉
        stop_wds = []
        for wd1 in wds:
            for wd2 in wds:
                if wd1[0]in wd2[0] and wd1[0] != wd2[0]:
                    stop_wds.append(wd1)
        final_wds = [i for i in wds if i not in stop_wds]
        #final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}返回指定键的值，如果值不在字典中返回default值

        return final_wds


if __name__=='__main__':
    q = questionClassifier()
    q.classifer_main('石油机械刊登过哪些论文')
