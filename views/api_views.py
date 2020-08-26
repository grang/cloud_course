# coding=utf-8
import logging
import traceback
import json
import os
import datetime

from django.conf import settings

from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate

from django.contrib.auth.models import User

from apps.classroom.models import Classroom, Homework, StudentHomework
from apps.institution.models import InstStudent, InstCourse, InstTeacher
from apps.role.models import Teacher, Student
from apps.course.models import Ware, Package, Material

from lib.file_store import oss_save_file
from lib.wx.base import WeixinMiniBase

from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt
from lib.IDGen import IdGenerator

from yuwen.utils import get_datetime_without_sec, strp_date



logger = logging.getLogger(__name__)

class TestView(View):
    def get(self, request):
        data = {'hello': 'world'}
        return JsonResponse(data)

class ClassroomView(View):
    def get(self, request):
        resp = {"code": 0}
        try:
            tid = request.GET.get('teacherId', '')

            if tid == '' or tid == 'null':
                return JsonResponse(code=1001, info='参数Tid为空')

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

class ClassroomNamesView(View):
    def get(self, request):
        resp = {"code": 0}
        try:
            cid = request.GET.get('classroomId')
            classroom = Classroom.objects.get(id=cid)

            packages = classroom.packages.all()

            # homework = Homework(classroom=classroom)
            # homework.save()

            data = []
            for package in packages:
                data.append(package.title)

            resp['data'] = data
            # resp['homeworkId'] = homework.id
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

class HomeworkUpload(View):
    def post(self, request):
        resp = {"code": 0}
        try:
            cid = request.POST.get('classroomId')
            content = request.POST.get('content')
            course = request.POST.get('course') # course name
            fileUrl0 = request.POST.get('fileUrl0', '')
            fileUrl1 = request.POST.get('fileUrl1', '')
            fileUrl2 = request.POST.get('fileUrl2', '')
            title = request.POST.get('title')
            date = request.POST.get('date')

            classroom = Classroom.objects.get(id=cid)
            package = Package.objects.get(title=course)

            finishDate = strp_date(date)

            homework = Homework(
                classroom=classroom,
                package=package,
                title=title,
                content=content,
                img1=fileUrl0,
                img2=fileUrl1,
                img3=fileUrl2,
                finish_date=finishDate
            )
            homework.save()

        except Exception as e:
            logger.error(e)
            resp.update(code=1000, info='数据出错')
        finally:
            return JsonResponse(resp, json_dumps_params={'ensure_ascii':False})

class HomeworkImgUpload(View):
    def post(self, request):
        resp = {"code": 0}
        try:
            image = request.FILES['file']

            file_name = image.name
            print(file_name)
            # logger.error("on post %s" % file_name)
            file_ext = os.path.splitext(file_name)[1].lower()
            ids = IdGenerator.gen()

            file_name = 'app/yuwen/homework/%s%s' % (ids, file_ext)
            print("upload file name is %s" % file_name)

            oss_save_file(file_name, image.read())

            resp['url'] = '%s/%s' % (settings.OSS_PREFIX, file_name)
        except Exception as e:
            logger.error(e)
            resp.update(code=1000, info='作业不存在')
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
                    for mat in ware.material.exclude(types=Material.URL_TYPE):
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
                    instStudent = InstStudent(institution=classroom.institution, student=student)
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

                api = WXAPPAPI(appid=settings.WX_MINI_APP_ID, app_secret=settings.WX_MINI_APP_SECRECT)
                # pc = WXBizDataCrypt(settings.WX_MINI_APP_ID, session_key, settings.WX_MINI_APP_SECRECT)
                try:
                    logger.error(data)
                    logger.error(iv)
                    logger.error(session_key)

                    crypt = WXBizDataCrypt(settings.WX_MINI_APP_ID, session_key)
                    res = crypt.decrypt(data, iv)

                    # res = pc.decrypt(data, iv)
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
                        user = User.objects.create_user(username=phone, password=settings.DEFAULT_PWD, is_active=True, first_name=phone, is_staff=True)
                        teacher = Teacher(phone=phone, name=phone, openid=openid, user=user)
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

class MenuInfoView(View):
    '''
    获取课件端登录
    '''
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(username=username, password=password)
            if user is None:
                return JsonResponse({'code': 1001, 'info':'用户名或者密码错误'})
            else:
                instTeacher = InstTeacher.objects.filter()
        except Exception as e:
            pass

        resp = {
            'response': 'ok',
        }

        menu = [
            {
                "label": "秋季课程",
                "children": [
                    {
                        "label": "3年级",
                        "children": [
                            {
                                "label": "第二讲",
                                "children": [
                                    {
                                        "label": "课件",
                                        "dir": "/3/2/ppt",
                                        "type": "html"
                                    },
                                    {
                                        "label": "示范课",
                                        "dir": "/3/2/video",
                                        "type": "html"
                                    }
                                ]
                            },
                            {
                                "label": "第三讲",
                                "children": [
                                    {
                                        "label": "课件",
                                        "dir": "/3/3/ppt",
                                        "type": "html"
                                    },
                                    {
                                        "label": "示范课",
                                        "dir": "/3/3/video",
                                        "type": "html"
                                    }
                                ]
                            }
                        ]
                    }
            ]
            }
        ]
        resp['menu'] = menu

        resp['username'] = username
        resp['expiredDate'] = datetime.datetime.today().strftime('%Y-%m-%d')

        return JsonResponse(resp)