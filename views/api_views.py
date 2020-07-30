# coding=utf-8
import logging
import traceback
import json

from django.conf import settings

from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone

from apps.classroom.models import Classroom, Homework, StudentHomework
from apps.institution.models import InstStudent, InstCourse, InstTeacher
from apps.role.models import Teacher, Student
from apps.course.models import Ware

from lib.wx.base import WeixinMiniBase, WXBizDataCrypt

from yuwen.utils import get_datetime_without_sec


logger = logging.getLogger(__name__)

class TestView(View):
    def get(self, request):
        data = {'hello': 'world'}
        return JsonResponse(data)

class ClassroomView(View):
    def get(self, request):
        resp = {"code": 0}
        try:
            tid = request.GET.get('teacherId')

            classrooms = Classroom.objects.filter(teacher__id=tid)
        
            data = []
            for classroom in classrooms:
                data.append(classroom.toDict())

            resp['data'] = data
        except Exception as e:
            logger.error(e)
            resp.update(code=1000, info='服务器出错误了，请重试！')
        finally:
            return JsonResponse(resp, json_dumps_params={'ensure_ascii':False})

class ClassroomInfoView(View):
    def get(self, request):
        resp = {"code": 0}
        try:
            cid = request.GET.get('classroomId')
            classroom = Classroom.objects.get(id=cid)

            data = classroom.toDict()
            resp['data'] = data
        except Exception as e:
            logger.error(e)
            resp.update(code=1000, info='没有此班级')
        finally:
            return JsonResponse(resp, json_dumps_params={'ensure_ascii':False})

class ClassroomStudents(View):
    def get(self, request):
        resp = {"code": 0}
        try:
            cid = request.GET.get('classroomId')
            classroom = Classroom.objects.get(id=cid)

            students = []
            for student in classroom.students.all():
                students.append(student.toDict())        

            resp['data'] = students
        except Exception as e:
            logger.error(e)
            resp.update(code=1000, info='班级不存在')
        finally:
            return JsonResponse(resp, json_dumps_params={'ensure_ascii':False})

class HomeworkView(View):
    def get(self, request):
        resp = {"code": 0}
        try:
            cid = request.GET.get('classroomId')
            homeworks = Homework.objects.filter(classroom__id=cid)

            data = []
            for homework in homeworks:
                item = homework.toDict()

                sh = StudentHomework.objects.filter(homework=homework, is_upload=True)
                item['doneCount'] = sh.count()
                item['needJudgeCount'] = sh.filter(is_judge=False).count()

                data.append(item)

            resp['data'] = data
        except Exception as e:
            logger.error(e)
            resp.update(code=1000, info='班级不存在')
        finally:
            return JsonResponse(resp, json_dumps_params={'ensure_ascii':False})

class StudentHomeworkListView(View):
    def get(self, request):
        resp = {"code": 0}
        try:
            hid = request.GET.get('homeworkId')
            doneType = request.GET.get('type') # 1: 已经完成 0: 未完成

            data = []
            homeworks = []

            if doneType == '1':
                homeworks = StudentHomework.objects.filter(homework__id=hid, is_upload=True)
            else:
                homeworks = StudentHomework.objects.filter(homework__id=hid, is_upload=False)

            for homework in homeworks:
                item = {
                    'id': homework.student.id,
                    'name': homework.student.getName()
                }

                if doneType == '1':
                    item['finishDate'] = get_datetime_without_sec(homework.upload_date)
                    item['isJudge'] = homework.is_judge

                data.append(item)
            
            resp['data'] = data
        except Exception as e:
            logger.error(e)
            resp.update(code=1000, info='班级不存在')
        finally:
            return JsonResponse(resp, json_dumps_params={'ensure_ascii':False})


class StudentInfoView(View):
    def get(self, request):
        resp = {"code": 0}
        try:
            sid = request.GET.get('studentId')
            instStudent = InstStudent.objects.get(id=sid)

            # 收到作业数
            homeworkPublishedCount = StudentHomework.objects.filter(student=instStudent).count()

            # 作业提交数
            homeworkFinishCount = StudentHomework.objects.filter(student=instStudent, is_upload=True).count()

            # 作业点评数
            homeworkJudgeCount = StudentHomework.objects.filter(student=instStudent, is_judge=True).count()

            homeworks = StudentHomework.objects.filter(student=instStudent)
            homeworksData = []

            for homework in homeworks:
                homeworksData.append(homework.toDict())

            data = {
                'name': instStudent.student.name,
                'head': instStudent.student.head,
                'homeworkPublishedCount': homeworkPublishedCount, 
                'homeworkFinishCount': homeworkFinishCount, 
                'homeworkJudgeCount': homeworkJudgeCount, 
                'homeworks': homeworksData
            }

            resp['data'] = data
        except Exception as e:
            logger.error(e)
            resp.update(code=1000, info='班级不存在')
        finally:
            return JsonResponse(resp, json_dumps_params={'ensure_ascii':False})

# 获取老师所在机构的课程列表
class ClasswareListView(View):
    def get(self, request):
        resp = {"code": 0}
        try:
            # 机构ID
            iid = request.GET.get('id')
            now = timezone.now()

            courses = InstCourse.objects.filter(institution__id=iid, enable=True, expired_date__gte=now)

            data = []
            for course in courses:
                wares = Ware.objects.filter(package=course.package)
                for ware in wares:
                    for mat in ware.material.all():
                        data.append(mat.toDict())

            resp['data'] = data
        except Exception as e:
            logger.error(e)
            resp.update(code=1000, info='机构不存在')
        finally:
            return JsonResponse(resp, json_dumps_params={'ensure_ascii':False})


class LoginView(View):
    def post(self, request):
        code = request.POST.get('code')
        logger.debug("code is %s" % code)

        role = request.POST.get('role') # teacher: 表示教师  student： 表示学生
        classroomId = request.POST.get('classroomId')

        name = request.POST.get('name')
        head = request.POST.get('head')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        province = request.POST.get('province')
        country = request.POST.get('country')

        mini_base = WeixinMiniBase.get_instance(settings.WX_MINI_APP_ID, settings.WX_MINI_APP_SECRECT)
        result = mini_base.get_miniprogram_session(code)

        logger.debug("result is %s" % json.dumps(result))
        print(result)

        if not 'errcode' in result:
            openid = result['openid']
            # unionid = result['unionid']
            session_key = result['session_key']


            if role == 'student':
                student = Student.objects.filter(openid=openid).first()
                if student:
                    student.wx_session = session_key
                    student.name = name
                    student.head = head
                    student.gender = gender
                    student.country = country
                    student.province = province
                    student.city = city 
                    student.save()
                else:
                    # student = Student(phone=openid, openid=openid, wx_session=session_key)
                    student = Student(name=name, phone=openid, head=head, openid=openid, wx_session=session_key, gender=int(gender), country=country, province=province, city=city)
                    student.save()

                classroom = Classroom.objects.filter(id=classroomId).first()
                if not classroom:
                    return JsonResponse({"code": 1001, "info": "班级不存在"})

                instStudent = InstStudent.objects.filter(student=student).first()
                if not instStudent:
                    instStudent = InstStudent(institution=classroom.institution, studnet=student)
                    instStudent.save()

                # 给班级添加学生
                if not classroom.students.filter(id=instStudent.id).first():
                    classroom.students.add(instStudent)

                data = {
                    'id': instStudent.id,
                    'openid': openid,
                    'role': role,
                    'name': name,
                    'head': head,
                    'gender': gender
                }

                return JsonResponse({"code": 0, "data": data})

            # if role == 'teacher':
            #     teacher = Teacher.objects.filter(openid=openid).first()
            #     if teacher:
            #         pass
            #     else:
            #         pass
        else:
            return JsonResponse({"code": 1000, "info": "微信授权出错"})

# 获取微信手机号，教师登录
class WxPhoneView(View):
    '''
    获取微信的电话
    '''
    def post(self, request):
        wxCode = request.POST.get('code')
        data = request.POST.get('data')
        iv = request.POST.get('iv')

        if not iv or iv == 'undefined':
            return JsonResponse({"code":1003, "data":"微信认证数据失败!"})

        code = 0
        teacherId = ''
        instId = ''
        phone = ''
        teacherName = ''
        if wxCode:
            mini_base = WeixinMiniBase.get_instance(settings.WX_MINI_APP_ID, settings.WX_MINI_APP_SECRECT)
            result = mini_base.get_miniprogram_session(wxCode)

            logger.debug("result is %s" % json.dumps(result))

            if not 'errcode' in result:
                openid = result['openid']
                session_key = result['session_key']

                pc = WXBizDataCrypt(settings.WX_MINI_APP_ID, session_key)
                try:
                    logger.error(data)
                    logger.error(iv)
                    logger.error(session_key)

                    res = pc.decrypt(data, iv)
                    phone = res['phoneNumber']
                    # logger.error("phone is %s" % phone)

                    # TODO：根据教师电话去找机构里是否有相同的
                    # 如果没有电话，则新建一个

                    teacher = Teacher.objects.filter(phone=phone).first()
                    if teacher:
                        instTeacher = InstTeacher.objects.filter(teacher=teacher).first()
                        if instTeacher:
                            code = 0
                            phone = phone
                            teacherId = instTeacher.id
                            instId = instTeacher.institution.id 
                            teacherName = teacher.name
                        else:
                            code = 101
                    else:
                        teacher = Teacher(phone=phone, name=phone, openid=openid)
                        teacher.save() 

                        code = 101
                        phone = phone

                except Exception as e:
                    logger.error(traceback.format_exc())

                    code = 1001
                finally:
                    return JsonResponse({'code': code, 'data':{'phone': phone, 'teacherId': teacherId, 'instId': instId, 'teacherName': teacherName}})
            else:
                return JsonResponse({'code': obj['errcode']})
        else:
            return JsonResponse({'code': 1002})