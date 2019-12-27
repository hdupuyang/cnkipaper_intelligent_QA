class question_transfer_sql:
    def transfer_main(self,data):
        wds=data['wds']
        question_types=data['question_types']
        #词的分类
        paper_wds=[]
        journal_wds = []
        author_wds = []
        unit_wds = []
        sqls=[]
        for wd in wds:
            if wd[1]=='paper':
                paper_wds.append(wd[0])
            elif wd[1]=='journal':
                journal_wds.append(wd[0])
            elif wd[1]=='author':
                author_wds.append(wd[0])
            elif wd[1]=='unit':
                unit_wds.append(wd[0])
        for type in question_types:
            if type=='作者--单位':
                for wd in author_wds:
                    sql="match q=(a:Author{{name:'{}'}})-[]->(u:Unit) return u.name".format(wd)
                    sqls.append([type, wd,sql])
            elif type=='作者--论文':
                for wd in author_wds:
                    sql = "match q=(p:Paper)-[]->(a:Author{{name:'{}'}}) return p.name".format(wd)
                    sqls.append([type, wd,sql])
            elif type == '论文--作者':
                for wd in paper_wds:
                    sql = "match q=(p:Paper{{name:'{}'}})-[]->(a:Author) return a.name".format(wd)
                    sqls.append([type, wd,sql])
            elif type == '论文--学科':
                for wd in paper_wds:
                    sql = "match q=(p:Paper{{name:'{}'}})-[]->(s:Subject) return s.name".format(wd)
                    sqls.append([type, wd, sql])
            elif type == '论文--期刊':
                for wd in paper_wds:
                    sql = "match q=(p:Paper{{name:'{}'}})-[]->(j:Journal) return j.name".format(wd)
                    sqls.append([type, wd,sql])
            elif type == '期刊--论文':
                for wd in journal_wds:
                    sql = "match q=(p:Paper)-[]->(j:Journal{{name:'{}'}}) return p.name".format(wd)
                    sqls.append([type, wd, sql])
            elif type == '作者--作者':
                wd=[]
                for wd1 in author_wds:
                    for wd2 in author_wds:
                        wd=[wd1,wd2]


        return sqls