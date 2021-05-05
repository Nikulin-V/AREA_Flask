from data.groups import Group
from data.students import Student
from .db_session import create_session


def repair_dependencies_students_and_groups():
    db_sess = create_session()
    groups_lists = list(db_sess.query(Group.id, Group.students_ids))
    for group_id, students in groups_lists:
        for student_id in list(map(int, str(students).split(','))):
            if len(list(db_sess.query(Student).filter(Student.user_id == student_id,
                                                      Student.group_id == group_id))) == 0:
                db_sess.add(Student(user_id=student_id, group_id=group_id))
    db_sess.commit()
