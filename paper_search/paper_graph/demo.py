import os
import binascii
from py2neo import Graph,Node
class PaperGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])  # join()方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
        self.data_path = os.path.join(cur_dir, 'data/paper.sql')
        self.g= Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="klhklh7878.")
        self.count=0

    def read(self):
        paper_list=[]
        author_list=[]
        unit_list=[]
        journal_list=[]
        journal_judge=[]
        subject_list = []

        #关系边
        rels_unit=[]
        rels_journal=[]
        rels_author=[]
        rels_subject=[]
        for data in open(self.data_path, encoding='UTF-8'):
            paper_dict={}
            journal_dict={}
            data = data.replace(
                "INSERT INTO `` (`id`, `PAPER_ID`, `name`, `authors`, `authors_code`, `first_organization`, `unit`, `organization`, `first_author`, `first_author_unit`, `first_author_baidu`, `first_author_code`, `second_author`, `second_author_unit`, `second_author_baidu`, `second_author_code`, `third_author`, `third_author_unit`, `third_author_baidu`, `third_author_code`, `fourth_author`, `fourth_author_unit`, `fourth_author_baidu`, `fourth_author_code`, `keywords`, `abstract`, `citations`, `downloads`, `classification_str`, `classification`, `zw_paper_code`, `zw_subject_code`, `subject_code`, `subject_code_old`, `year`, `area_code`, `journal_name`, `journal_no`, `journal_quality`, `journal_url`, `url`, `flag`, `unit_type`) VALUES ",
                "")
            data = data.replace(");", ")").replace("(","[").replace(")","]")
            data = data.replace("NULL", "None")
            li = eval(data)
            if li[25]:
                li[25]=hex(li[25]).replace('0x','')
                li[25]=str(binascii.a2b_hex(li[25]), encoding="utf-8")#修修改改字符串 创建好了每条论文信息列表
            '''paper_dict['id']=li[0]
            paper_dict['paper_id'] = li[1]
            paper_dict['name'] = li[2]
            paper_dict['keywords'] = li[24]
            paper_dict['abstract'] = li[25]
            paper_dict['url'] = li[40]
            self.build_paper_node(paper_dict)#创建论文节点'''
            paper_list.append(li[2])
            if li[3]:#创建作者节点
                cnt=li[3].split(';')
                author_list +=cnt
                for author in cnt:
                    rels_author.append([li[2],author])

            if li[6]:#创建单位节点
                unit_list.append(li[6])
            if li[9]:
                unit_list.append(li[9])
                rels_unit.append([li[8],li[9]])
            if li[13]:
                unit_list.append(li[13])
                rels_unit.append([li[12], li[13]])
            if li[17]:
                unit_list.append(li[17])
                rels_unit.append([li[16], li[17]])
            if li[21]:
                unit_list.append(li[21])
                rels_unit.append([li[20], li[21]])
            if li[36]:#有两个沦为没有journal 判断非None
                if li[36] not in journal_judge:#利用journal_judge判断是否重复
                    journal_dict['name'] = li[36]
                    journal_dict['quality'] = li[38]
                    journal_dict['url'] = li[39]
                    journal_judge.append(li[36])
                    journal_list.append(journal_dict)
                rels_journal.append([li[2],li[36]])
            subject_list.append(li[32])
            rels_subject.append([li[2],li[32]])

        f_paper=open('paper.txt', 'w+', encoding='UTF-8')
        f_author = open('author.txt', 'w+', encoding='UTF-8')
        f_unit = open('unit.txt', 'w+', encoding='UTF-8')
        f_journal = open('journal.txt', 'w+', encoding='UTF-8')

        '''f_paper.write('\n'.join(set(paper_list)))
        f_author.write('\n'.join(set(author_list)))
        f_unit.write('\n'.join(set(unit_list)))
        f_journal.write('\n'.join(set(journal_judge)))'''


        #self.build_author_node(set(author_list))
        #self.build_unit_node(set(unit_list))
        #self.build_journal_node(journal_list)
        #self.build_subject_node(set(subject_list))
        self.create_relationship('Author', 'Unit', rels_unit, 'unit', '所属单位')
        #self.create_relationship('Paper', 'Author', rels_author, 'write', '作者')
        #self.create_relationship('Paper', 'Journal', rels_journal, 'journal', '所属刊物')
        #self.create_relationship('Paper', 'Subject', rels_subject, 'subject', '学科')

    def build_paper_node(self,paper_dict):
        node = Node("Paper", id=paper_dict['id'], paper_id=paper_dict['paper_id'],
                    name=paper_dict['name'], keywords=paper_dict['keywords'],
                    abstract=paper_dict['abstract'],url=paper_dict['url']
                    )
        self.g.create(node)
        self.count += 1
        print('build_paper_node {}'.format(self.count))
        return
    def build_author_node(self,author_list):
        count=0
        for author in author_list:
            node=Node("Author",name=author)
            self.g.create(node)
            count+=1
            print('build_author_node {}'.format(count))
    def build_unit_node(self,unit_list):
        count = 0
        for unit in unit_list:
            node = Node("Unit", name=unit)
            self.g.create(node)
            count += 1
            print('build_unit_node {}'.format(count))
    def build_journal_node(self,journal_list):
        count = 0
        for journal in journal_list:
            node = Node("Journal", name=journal['name'],
                        quality=journal['quality'],url=journal['url'])
            self.g.create(node)
            count += 1
            print('build_journal_node {}'.format(count))
    def build_subject_node(self,subject_list):
        count = 0
        for subject in subject_list:
            node = Node("Subject", name=subject)
            self.g.create(node)
            count += 1
            print('build_subject_node {}'.format(count))
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return
#str(binascii.a2b_hex("e4bda0e5a5bde5958a"), encoding="utf-8")
#INSERT INTO `` (`id`, `PAPER_ID`, `name`, `authors`, `authors_code`, `first_organization`, `unit`, `organization`, `first_author`, `first_author_unit`, `first_author_baidu`, `first_author_code`, `second_author`, `second_author_unit`, `second_author_baidu`, `second_author_code`, `third_author`, `third_author_unit`, `third_author_baidu`, `third_author_code`, `fourth_author`, `fourth_author_unit`, `fourth_author_baidu`, `fourth_author_code`, `keywords`, `abstract`, `citations`, `downloads`, `classification_str`, `classification`, `zw_paper_code`, `zw_subject_code`, `subject_code`, `subject_code_old`, `year`, `area_code`, `journal_name`, `journal_no`, `journal_quality`, `journal_url`, `url`, `flag`, `unit_type`)