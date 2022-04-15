# importing required packages
import json
from application import db
from application import app
from flask import render_template, url_for, redirect, flash
from application.models import ScrappedDataCourses, ScrappedDataCourse
from application.util import get_courses_detail_data, get_course_categories_data


@app.route('/')
def index():
    # get course data
    courses_details, tech_count, kids_count, tech_free, kids_free = get_courses_detail_data('Data Science')
    tech_neuron_percentage = int(round((int(tech_count) / len(courses_details)) * 100, 0))
    kids_neuron_percentage = int(round((int(kids_count) / len(courses_details)) * 100, 0))

    # get course category data
    course_categories = get_course_categories_data('Data Science')

    # enter select feature data to db
    # for course_data in course_categories:
    #     db_entry = ScrappedDataCourses(
    #         course_categories=course_data['course-category'],
    #         course_sub_categories=', '.join(course_data['course-sub-category']),
    #         tech_neuron_course_count=tech_count,
    #         kids_neuron_course_count=kids_count
    #     )
    #     db.session.add(db_entry)
    #     db.session.commit()

    return render_template('home/index.html', categories_count=len(course_categories),
                           courses_count=len(courses_details), course_categories=course_categories,
                           courses_details=courses_details, tech_neuron_count=tech_count, zip=zip,
                           tech_neuron_percentage=tech_neuron_percentage, kids_neuron_count=kids_count,
                           kids_neuron_percentage=kids_neuron_percentage, tech_free=tech_free, kids_free=kids_free)


@app.route('/logout')
def logout():
    return redirect(url_for('home/index.html'))
