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
        row =cursor.fetchone()
        return row[0]
    def jenkins_count(self,):
        cursor = connection.cursor()
        cursor.execute("""SELECT count(commitcode) FROM jenkins_source""")
        row =cursor.fetchone()
        return row[0]
    def jenkins_count(self,):
        cursor = connection.cursor()
        cursor.execute("""SELECT count(commitcode) FROM jenkins_source""")
        row =cursor.fetchone()
        return row[0]
    def bug_7count(self,st):
        datem = '%Y/%m/%d'
        cursor = connection.cursor()
        cursor.execute("""select date_format(date,%s),count(*) from bug where bug_status=%s and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <=date(date) GROUP BY date_format(date,%s)""",[datem,st,datem])
        row=cursor.fetchall()
        return row
    def jenkins_7count(self,):
        datem = '%Y/%m/%d'
        cursor = connection.cursor()
        cursor.execute("""select date_format(date,%s),count(*) from jenkins_source where  DATE_SUB(CURDATE(), INTERVAL 30 DAY) <=date(date) GROUP BY date_format(date,%s)""",[datem,datem])
        row =cursor.fetchall()
        return row
    def buglevel30_count(self):
        sql ="""select ifnull(level_id,4) as lv_id,count(*) from bug where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <=date(date) and bug_status= '新建' GROUP BY LEVEL_id  order by lv_id"""
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
    def bugtagl30_count(self):
        sql ="""select tag_name,count(*) from bug where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <=date(date) and tag_name is not null GROUP BY tag_name """
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
    def onlinebug30_count(self,):
        cursor = connection.cursor()
        cursor.execute("""select count(*) from bug where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <=date(date) and bug_status = '新建' and is_miss=1""")
        row =cursor.fetchone()
        return row[0]

    def fenci_30count(self,st):
        cursor = connection.cursor()
        cursor.execute("""select tag_name,count(*) as cn,GROUP_CONCAT(DISTINCT bug_id) from bug where sub_type=%s and bug_status='新建' and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <=date(date) GROUP BY tag_name ORDER BY cn desc """,[st])
        row =cursor.fetchall()
        return row
    def fencicommitcode_30count(self,st):
        cursor = connection.cursor()
        cursor.execute("""select keyword,sum(count_num) as sm,GROUP_CONCAT(DISTINCT bug_id) as bug_id,count(commitcode) as commitcode,GROUP_CONCAT(DISTINCT commitcode)  from keywords where object_id =%s and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <=date(startdate)   GROUP BY keyword having sm != commitcode ORDER BY sm desc LIMIT 10 """,[st])
        row =cursor.fetchall()
        return row

    def bug_detail(self,st,st1):
        sql ='select bug.bug_id,bug.bug_name,bug.bug_status,bug.date,bug.type,object_name.object_name,bug.level_id from bug,object_name where bug.sub_type=object_name.object_id and bug_id  in (%s) and bug_status=%s'%(st,st1)
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
    def bugname_detail(self,st,st1,st2):
        sql ='select bug.bug_id,bug.bug_name,bug.bug_status,bug.date,bug.type,object_name.object_name,bug.level_id from bug,object_name where %s and bug.sub_type=object_name.object_id  and sub_type=%s and bug_status=%s'%(st,st1,st2)
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
    def bugmore_detail(self,st,st1):
        sql ='select bug.bug_id,bug.bug_name,bug.bug_status,bug.date,bug.type,object_name.object_name,bug.level_id from bug,object_name where bug.sub_type=object_name.object_id and  bug_status=%s %s'%(st,st1)
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
    def jenkins_detail(self,st):
        sql ='select commitcode,change_name,change_source,date,object_id from jenkins_source where commitcode  in (%s)'%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
    def jenkins1_detail(self,st):
        sql ='select commitcode,change_name,change_source,date,object_id  from jenkins_source where change_name =%s'%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def jenkinsmore_detail(self):
        sql ="""select commitcode,change_name,change_source,date,object_id  from jenkins_source"""
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
    def changename_analyze(self,st):
        sql ="""SELECT DISTINCT js.object_id,js.change_name,cl.level_name,cl.add_count,cl.del_count,cl.result_count,cl.bug_count,ct.keyword,ct.keyword_count,cbp.bug_probability,cbp.sum_bug,cbp.count_changename from jenkins_source as js
            LEFT JOIN changename_level as cl on js.change_name=cl.change_name and js.object_id=cl.object_id
            LEFT JOIN changename_topkeyword as ct on js.change_name=ct.change_name and js.object_id=ct.object_id
            LEFT JOIN changename_bug_probability as cbp on js.change_name=cbp.change_name and js.object_id=cbp.object_id where DATE_SUB(CURDATE(), INTERVAL 90 DAY) <=date(js.date)
            %s"""%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        return row
    def commitcode_bug(self,st):
        sql ="""select change_name,sum(new_bug_count) as sm_bug,count(change_name) as cn_name,ROUND(sum(new_bug_count)/count(change_name)*100,1) as con,GROUP_CONCAT(DISTINCT bug_new_id) as bug_id
                from changename_statistics   
                where object_id = %s and DATE_SUB(CURDATE(), INTERVAL 90 DAY) <=date(create_date) and change_name not like '%%.css'
                GROUP BY change_name ORDER BY con desc LIMIT 10"""%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        return row
    def day_statistics_search_detail(self,st):
        sql ="""select day_statistics.date,day_statistics.commit_count,day_statistics.change_count,day_statistics.change_totlecount,day_statistics.add_count,day_statistics.del_count,day_statistics.bug_new_count,day_statistics.bug_fix_count,day_statistics.bug_close_count,object_name.object_name from day_statistics,object_name where day_statistics.object_id = object_name.object_id and %s ORDER BY day_statistics.date desc  """%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row=cursor.fetchall()
        return row
    def bug_search_detail(self,st):
        sql ="""select bug.bug_id,bug.bug_name,bug.bug_status,bug.date,bug.type,object_name.object_name,is_miss,ifnull(bug.level_id,4) from bug,object_name where bug.sub_type=object_name.object_id and %s ORDER BY bug.date desc  """%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
    def jenkins_search_detail(self,st):
        sql ="""select jenkins_source.commitcode,jenkins_source.change_name,jenkins_source.change_source,jenkins_source.date,object_name.object_name  from jenkins_source,object_name where jenkins_source.object_id=object_name.object_id and %s ORDER BY jenkins_source.date desc  """%(st)
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
    def search_object_name(self):
        sql ="""select object_id,object_name from object_name """
        cursor = connection.cursor()
        cursor.execute(sql)
        row =cursor.fetchall()
        return row
class bug(models.Model):
  bug_status = models.CharField(max_length=50)
  objects = testbigdata()