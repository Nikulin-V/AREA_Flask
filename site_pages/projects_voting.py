#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from data import db_session
from data.projects_8_class import Project
from data.projects_8_class_votes import Vote
from forms.vote import VoteForm
from site_pages.functions import evaluate_form

projects_voting_page = Blueprint('projects-voting', __name__)
app = projects_voting_page


@app.route('/8-classes-projects-result', methods=['GET', 'POST'])
@mobile_template('{mobile/}8-classes-projects-result.html')
@login_required
def projects_voting(template):
    db_sess = db_session.create_session()

    form = VoteForm()

    message = ''

    # self project
    # noinspection PyUnresolvedReferences
    project = db_sess.query(Project.id, Project.title). \
        filter(Project.authors_ids.contains(str(current_user.id))).first()
    points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                          filter(Vote.project_id == project[0]))))
    project = list(project) + [points]

    if form.is_submitted():
        if form.points.data is None:
            pass
        elif form.project.data == project[1]:
            message = 'Вы не можете голосовать за свой проект'
        elif 0 < form.points.data <= 100:
            project_id = db_sess.query(Project.id). \
                filter(Project.title == form.project.data).first()[0]
            current_voted_points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                                                filter(Vote.user_id == current_user.id))))
            current_project_voted_points = db_sess.query(Vote.points). \
                filter(Vote.user_id == current_user.id,
                       Vote.project_id == project_id).first()
            if current_project_voted_points:
                current_project_voted_points = current_project_voted_points[0]
            else:
                current_project_voted_points = 0
            if current_voted_points + form.points.data <= 100 or \
                    current_project_voted_points >= form.points.data or \
                    (current_project_voted_points < form.points.data and
                     current_voted_points - current_project_voted_points + form.points.data <= 100):
                project_id = db_sess.query(Project.id). \
                    filter(Project.title == form.project.data).first()
                if project_id:
                    project_id = project_id[0]
                vote = db_sess.query(Vote).filter(Vote.user_id == current_user.id,
                                                  Vote.project_id == project_id).first()
                if vote:
                    vote.points = form.points.data
                    db_sess.merge(vote)
                else:
                    vote = Vote(user_id=current_user.id,
                                project_id=project_id,
                                points=form.points.data)
                    db_sess.add(vote)
                db_sess.commit()
            else:
                message = f'Вам не хватает очков.\n' \
                          f'Вы можете отменить голос, назначив проекту 0 очков.\n' \
                          f'Ваши очки: {100 - current_voted_points}/100'
        elif form.points.data == 0:
            project_id = db_sess.query(Project.id). \
                filter(Project.title == form.project.data).first()
            if project_id:
                project_id = project_id[0]
            vote = db_sess.query(Vote).filter(Vote.user_id == current_user.id,
                                              Vote.project_id == project_id).first()
            if vote:
                db_sess.delete(vote)
                db_sess.commit()
        else:
            message = 'Неверное число очков'

    sections, projects = evaluate_form(form)

    if not form.project.data:
        form.project.data = form.project.choices[0]
    project_id = db_sess.query(Project.id).filter(Project.title == form.project.data,
                                                  Project.section == form.section.data).first()
    if project_id:
        project_id = project_id[0]
    else:
        form.project.data = form.project.choices[0]
        project_id = db_sess.query(Project.id).filter(Project.title == form.project.data,
                                                      Project.section == form.section.data).first()
        if project_id:
            project_id = project_id[0]

    current_voted_points = sum(list(map(lambda x: x[0], db_sess.query(Vote.points).
                                        filter(Vote.project_id == project_id,
                                               Vote.user_id == current_user.id))))

    form.points.data = current_voted_points if current_voted_points else 0

    return render_template(template,
                           form=form,
                           title='Проекты',
                           message=message,
                           project=project,
                           projects=projects,
                           sections=sections)
