#coding:utf8
from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.
from stucampus.gobye.models import gpas
from datadeal import delSpace,getIndex,DivedeAll,divideInfo,getFailCourse,getCource,getAllCource,myFind,updateType,Compare,Sort
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def index(request):
    return render(request, 'gobye/login.html')

def result(request):
    if request.method =="POST":
        top_info = request.POST.get('select-course')
        bottom_info = request.POST.get('grade')
    
    all_text = top_info.decode('utf-8')+bottom_info.decode('utf-8') 
	# all_text = open('test.txt').read().decode('gb2312')
    #删除多余换行
    all_text = delSpace(all_text)

    if all_text.find(u'学号')==-1 or all_text.find(u'主修专业')==-1:
        #找不到学号或主修专业
        print "error1"

    #获取专业及年纪
    stu_num = all_text[all_text.find(u'学号')+3:all_text.find(u'姓名')-2]
    stu_grade = stu_num[:4]
    stu_major = all_text[all_text.find(u'主修专业')+5:all_text.find(u'序号')-1]
    while stu_major.find(' ')!=-1:
        stu_major = stu_major.replace(' ','')

    #获取所有选课结果
    result_pre = []#记录以前的成绩
    result_now = []#记录本学期选课
    getAllCource(all_text,result_now,result_pre)

    DivedeAll(result_now)
    DivedeAll(result_pre)

    #分析以前的成绩,判断挂科科目
    result_fail = []#储存挂科科目.注:result_fail[0]为课程名,result_fail[1]为选修或必修,2为学分
    creditNeed = [0.0,0.0,0.0,0.0]

    if len(result_fail)>0:
        print "挂科科目:"
        for i in result_fail:
            print "课程名:"+i[0]+"    学分类型:"+i[1]+"    学分:"+i[2]

    #与培养方案比较，计算需修学分

    final_result = Compare(stu_major,stu_grade,result_now,result_pre,result_fail,creditNeed)

    creditGet = getFailCourse(result_pre,result_fail)#creditGet[0]为必修已获取学分,creditGet[1]为选修已获取学分
    #区分公共必修，专业必修
    CourseP = []#公共必修
    CourseM = []#专业必修
    CoursePE = []#公共选修
    CourseME = []#专业选修

    if final_result==0:
        print "error2"
    else :
        print "主修专业:"+stu_major
        print "年级:"+stu_grade
        print "已修公共必修学分:"+str(creditGet[0])+"    已修公共选修学分:"+str(creditGet[1])+"      已修专业必修学分:"+str(creditGet[2])+"    已修专业选修学分:"+str(creditGet[3])
        print "需修公共必修学分:"+str(creditNeed[0])+"    需修公共选修学分:"+str(creditNeed[1])+"      需修专业必修学分:"+str(creditNeed[2])+"    需修专业选修学分:"+str(creditNeed[3])
        result_final = []
        for each_final in final_result:
            each_result = []
            each_result.append(each_final.id)
            each_result.append(each_final.profess_id)
            each_result.append(each_final.course_name)
            each_result.append(each_final.total_number)
            each_result.append(each_final.credit)
            each_result.append(each_final.credit_type)
            each_result.append(each_final.course_type)
            result_final.append(each_result)
            
        Sort(CourseP, CoursePE, CourseM, CourseME, result_final, 6, 0)
        Sort(CourseP, CoursePE, CourseM, CourseME, result_pre, 4, 1)
        Sort(CourseP, CoursePE, CourseM, CourseME, result_now, 4, 2)

 #       print '仍需公共必修课程:'
  #      for x in CourseP:
   #         print str(x[0])+' '+str(x[1])+' '+str(x[2])+' '+str(x[3])+' '+str(x[4])+' '+str(x[5])
    #    print '仍需专业必修课程:'
    #    for x in CourseM:
     #       print str(x[0])+' '+str(x[1])+' '+str(x[2])+' '+str(x[3])+' '+str(x[4])+' '+str(x[5])
      #  print '仍需公共选修课程:'
      #  for x in CoursePE:
      #      print str(x[0])+' '+str(x[1])+' '+str(x[2])+' '+str(x[3])+' '+str(x[4])+' '+str(x[5])
      #  print '仍需专业选修课程:'
      #  for x in CourseME:
      #      print str(x[0])+' '+str(x[1])+' '+str(x[2])+' '+str(x[3])+' '+str(x[4])+' '+str(x[5])

    lack = creditNeed[0] + creditNeed[1] + creditNeed[2] + creditNeed[3] - creditGet[0] - creditGet[1] - creditGet[2] - creditGet[3]

    return render(request, 'gobye/result.html',{'CourseP':CourseP,'CourseM':CourseM,'CoursePE':CoursePE,'CourseME':CourseME,'creditGet':creditGet,'creditNeed':creditNeed,'lack':lack})