# coding=utf-8
import logging
import traceback

from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings

from apps.classroom.models import Classroom, Homework, StudentHomework
from apps.institution.models import InstStudent

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