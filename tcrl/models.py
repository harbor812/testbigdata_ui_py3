from django.db import models,connection

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    nickname=models.CharField(max_length=500)

    def __unicode__(self):
        return self.username

class testbigdata(models.Manager):
    def bug_count(self,st):
        cursor = connection.cursor()
        cursor.execute("""SELECT count(*) FROM bug WHERE bug_status = %s""", [st])
        row=cursor.fetchone()
        return row[0]
    def jenkins_count(self,):
        cursor = connection.cursor()
        cursor.execute("""SELECT count(commitcode) FROM jenkins_source""")
        row=cursor.fetchone()
        return row[0]
    def jenkins_count(self,):
        cursor = connection.cursor()
        cursor.execute("""SELECT count(commitcode) FROM jenkins_source""")
        row=cursor.fetchone()
        return row[0]
    def bug_7count(self,st):
        datem = '%Y/%m/%d'
        cursor = connection.cursor()
        cursor.execute("""select date_format(date,%s),count(*) from bug where bug_status=%s and DATE_SUB(CURDATE(), INTERVAL 7 DAY) <=date(date) GROUP BY date_format(date,%s)""",[datem,st,datem])
        row=cursor.fetchall()
        return row
    def jenkins_7count(self,):
        datem = '%Y/%m/%d'
        cursor = connection.cursor()
        cursor.execute("""select date_format(date,%s),count(*) from jenkins_source where  DATE_SUB(CURDATE(), INTERVAL 7 DAY) <=date(date) GROUP BY date_format(date,%s)""",[datem,datem])
        row=cursor.fetchall()
        return row
    def fenci_30count(self,st):
        cursor = connection.cursor()
        cursor.execute("""select keyword,sum(count_num) as sm,GROUP_CONCAT(DISTINCT bug_id) as bug_id from day_keywords where object_id =%s and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <=date(day) GROUP BY keyword ORDER BY sm desc LIMIT 10 """,[st])
        row=cursor.fetchall()
        return row
    def fencicommitcode_30count(self,st):
        cursor = connection.cursor()
        cursor.execute("""select keyword,sum(count_num) as sm,GROUP_CONCAT(DISTINCT bug_id) as bug_id,count(commitcode) as commitcode,GROUP_CONCAT(DISTINCT commitcode)  from keywords where object_id =%s and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <=date(startdate)   GROUP BY keyword having sm != commitcode ORDER BY sm desc LIMIT 10 """,[st])
        row=cursor.fetchall()
        return row

    def bug_detail(self,st,st1):
        sql='select bug_id,bug_name,bug_status,date,type,sub_type from bug where bug_id  in (%s) and bug_status=%s'%(st,st1)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def bugname_detail(self,st,st1,st2):
        sql='select bug_id,bug_name,bug_status,date,type,sub_type from bug where %s and sub_type=%s and bug_status=%s'%(st,st1,st2)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def bugmore_detail(self,st):
        sql='select bug_id,bug_name,bug_status,date,type,sub_type from bug where bug_status=%s'%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def jenkins_detail(self,st):
        sql='select commitcode,change_name,change_source,date,object_id from jenkins_source where commitcode  in (%s)'%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def jenkins1_detail(self,st):
        sql='select commitcode,change_name,change_source,date,object_id  from jenkins_source where change_name =%s'%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def jenkinsmore_detail(self):
        sql="""select commitcode,change_name,change_source,date,object_id  from jenkins_source"""
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def changename_analyze(self,st):
        sql="""SELECT DISTINCT js.object_id,js.change_name,cl.level_name,cl.add_count,cl.del_count,cl.result_count,cl.bug_count,ct.keyword,ct.keyword_count,cbp.bug_probability,cbp.sum_bug,cbp.count_changename from jenkins_source as js
            LEFT JOIN changename_level as cl on js.change_name=cl.change_name and js.object_id=cl.object_id
            LEFT JOIN changename_topkeyword as ct on js.change_name=ct.change_name and js.object_id=ct.object_id
            LEFT JOIN changename_bug_probability as cbp on js.change_name=cbp.change_name and js.object_id=cbp.object_id where DATE_SUB(CURDATE(), INTERVAL 90 DAY) <=date(js.date)
            %s"""%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def commitcode_bug(self,st):
        sql="""select change_name,sum(new_bug_count) as sm_bug,count(change_name) as cn_name,ROUND(sum(new_bug_count)/count(change_name)*100,1) as con,GROUP_CONCAT(DISTINCT bug_new_id) as bug_id
                from changename_statistics   
                where object_id = %s and DATE_SUB(CURDATE(), INTERVAL 90 DAY) <=date(create_date) and change_name not like '%%.css'
                GROUP BY change_name ORDER BY con desc LIMIT 10"""%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def day_statistics_search_detail(self,st):
        sql="""select date,commit_count,change_count,change_totlecount,add_count,del_count,bug_new_count,bug_fix_count,bug_close_count,object_id from day_statistics where %s ORDER BY date desc  """%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def bug_search_detail(self,st):
        sql="""select bug_id,bug_name,bug_status,date,type,sub_type from bug where %s ORDER BY date desc  """%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def jenkins_search_detail(self,st):
        sql="""select commitcode,change_name,change_source,date,object_id  from jenkins_source where %s ORDER BY date desc  """%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
class bug(models.Model):
  bug_status = models.CharField(max_length=50)
  objects = testbigdata()