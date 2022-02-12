#  Nikulin Vasily © 2021
from flask import Blueprint
from flask_cors import CORS

from tools.io_blueprint import IOBlueprint

api = Blueprint('api', __name__)
socket = IOBlueprint()

CORS(api)

from .info import getSubjects, getTeachersList
from .classes import getClasses, createClass, deleteClass
from .teachers import getTeachers, editTeacher, deleteTeacher
from .workload import getWorkload, createWorkload, deleteWorkload
