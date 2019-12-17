from py2neo import Graph
class sql_answer:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="klhklh7878.")
        self.num_limit = 20
    def ans_main(self,sqls):
        answers=[]
        for sql in sqls:
            question_type=sql[0]
            keyword=sql[1]
            sql_str=sql[2]

            if question_type=='作者--单位':
                res=self.g.run(sql_str).data()

                if res:
                    li=[]
                    for dict in res:
                        li.append(dict['u.name'])
                    answers.append('{0}的单位是{1}。'.format(keyword,',\n'.join(li)))
                else :
                    answers.append('没有找到{}的单位'.format(keyword))
            elif question_type=='作者--论文':
                res = self.g.run(sql_str).data()

                if res:
                    li = []
                    for dict in res:
                        li.append(dict['p.name'])
                    answers.append('{0}发表过的论文有{1}。'.format(keyword, ',\n'.join(li)))
                else:
                    answers.append('没有找到{}发表过的论文'.format(keyword))
            elif question_type == '论文--作者':
                res = self.g.run(sql_str).data()

                if res:
                    li = []
                    for dict in res:
                        li.append(dict['a.name'])
                    answers.append('{0}的作者有{1}。'.format(keyword, ',\n'.join(li)))
                else:
                    answers.append('暂无{}的作者信息'.format(keyword))
            elif question_type == '论文--学科':
                res = self.g.run(sql_str).data()

                if res:
                    li = []
                    for dict in res:
                        li.append(dict['s.name'])
                    answers.append('{0}的所属学科是{1}。'.format(keyword, ',\n'.join(li)))
            elif question_type == '论文--期刊':
                res = self.g.run(sql_str).data()

                if res:
                    li = []
                    for dict in res:
                        li.append(dict['j.name'])
                    answers.append('{0}所属期刊是{1}。'.format(keyword, ',\n'.join(li)))
                else:
                    answers.append('暂无{}所属的期刊信息'.format(keyword))
            elif question_type == '期刊--论文':
                res = self.g.run(sql_str).data()

                if res:
                    li = []
                    for dict in res:
                        li.append(dict['p.name'])
                    answers.append('{0}期刊发布过的论文有{1}。'.format(keyword, ',\n'.join(li)))
        return answers