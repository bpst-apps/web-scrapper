# importing required packages
import json
from application import db
from application import app
from flask import render_template, url_for, redirect, flash
from application.models import ScrappedDataCourses, ScrappedDataCourse
from application.util import (get_courses_detail_data, get_course_categories_data, get_course_data, get_indeed_job_data,
                              get_similar_content, get_search_query, get_timestamp, scrape_coursera_pages,
                              insert_course, insert_courses_details_dump, insert_course_categories_dump)


@app.route('/')
def index():
    # get course data
    courses_details, tech_count, kids_count, tech_free, kids_free = get_courses_detail_data('Data Science')
    tech_neuron_percentage = int(round((int(tech_count) / len(courses_details)) * 100, 0))
    kids_neuron_percentage = int(round((int(kids_count) / len(courses_details)) * 100, 0))

    # insert courses data
    insert_courses_details_dump([str(courses_details), str(tech_neuron_percentage),
                                              str(kids_neuron_percentage), get_timestamp()])

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

    # insert courses category data
    insert_course_categories_dump([str(course_categories), get_timestamp()])

    return render_template('home/index.html', categories_count=len(course_categories),
                           courses_count=len(courses_details), course_categories=course_categories,
                           courses_details=courses_details, tech_neuron_count=tech_count, zip=zip,
                           tech_neuron_percentage=tech_neuron_percentage, kids_neuron_count=kids_count,
                           kids_neuron_percentage=kids_neuron_percentage, tech_free=tech_free, kids_free=kids_free)


@app.route('/course/<string:course_name>')
def course(course_name):
    # get selected course data
    course_data = get_course_data(course_name)

    # get similar content data
    similar_content = get_similar_content(get_search_query(course_name), num_results=5)

    # enter select feature data to db
    # db_entry = ScrappedDataCourse(
    #     course_name=course_data[0]['course-name'],
    #     course_features=', '.join(course_data[0]['course-features']),
    #     course_fee=course_data[0]['course-price'],
    #     similar_content=', '.join([content['course-url'] for content in similar_content])
    # )
    # db.session.add(db_entry)
    # db.session.commit()

    # insert course data to database
    insert_course([str(course_data), str(similar_content), get_timestamp()])

    # course url
    course_url = 'https://courses.ineuron.ai/' + course_name.replace(' ', '-')

    # render course.html with fetch (scrapped) data
    return render_template('home/course.html', course_data=course_data[0], similar_content_count=len(similar_content),
                           similar_content=similar_content, timestamp=get_timestamp(), course_url=course_url)


@app.route('/coursera')
def coursera():
    # define site url
    site_url = 'https://www.coursera.org/learn/machine-learning'

    # scrape coursera website data
    coursera_data = scrape_coursera_pages(site_url)

    # render analysis.html with fetch (scrapped) data
    return render_template('home/coursera.html', coursera_data=coursera_data, timestamp=get_timestamp(),
                           site_url=site_url)


@app.route('/jobs')
def jobs():
    indeed_portal_data = get_indeed_job_data()

    # render analysis.html with fetch (scrapped) data
    return render_template('home/jobs.html', indeed_portal_data=indeed_portal_data)


@app.route('/offers')
def offers():
    # render analysis.html with fetch (scrapped) data
    return render_template('home/offers.html')


@app.route('/logout')
def logout():
    return redirect(url_for('home/index.html'))
