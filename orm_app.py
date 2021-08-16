from collections import ormdict
from glob import glob
from os.path import dirname, join
from uuid import uuid4

from flask import Flask, request, render_template, redirect

from db_orm import Votes, Topics, db

template_folder = join(dirname(__file__), "templates/")
app = Flask(__name__, template_folder=template_folder)
app.static_folder = 'static'
topics = dict({'85a1e80c-33b8-4fa3-8291-9ad09cca2350': {
    'name': 'Mom\'s birthday gift.',
    'data': ormdict(int)
}})


@app.route('/')
def index():
    ntopics = list(Topics.select())
    print(ntopics)
    return render_template("orm/index.html", topics=ntopics)


@app.route('/newTopic', methods=["GET"])
def get_new_topic():
    return render_template("orm/new_topic.html")


@app.route('/newTopic', methods=["POST"])
def post_new_topic():
    topic_name = request.form.get("name")
    assert topic_name is not None
    Topics.create(id=str(uuid4()), name=topic_name)
    return redirect('/')


@app.route('/topic/<topic_id>', methods=["GET"])
def view_topic(topic_id):
    if not Topics.exists(topic_id):
        return 'Topic Not Found', 404
    topic = list(Topics.select().where(Topics.id == topic_id))
    print(topic)
    votes = list(Votes.select().where(Votes.topic == topic[0]))
    print(votes)
    return render_template("orm/topic.html",
                           topic=topic[0],
                           votes=votes,
                           topic_id=topic_id
                           )


@app.route('/topic/<topic_id>/newChoice', methods=['POST'])
def new_topic_choice(topic_id):
    if not Topics.exists(topic_id):
        return 'Topic Not Found', 404
    choice = request.form.get('choice')
    Votes.create(topic=Topics.get_by_id(topic_id), choice_name=choice, choice_count=0)
    # db.add_choice(choice, topic_id)
    return redirect(f'/topic/{topic_id}')


@app.route('/topic/<topic_id>/vote', methods=['POST'])
def vote_topic_choice(topic_id):
    if not Topics.exists(topic_id):
        return 'Topic not found', 404
    choice_id = request.form.get('choice')
    if choice_id is None:
        return "Invalid choice name", 400
    query = Votes.update(choice_count = Votes.choice_count + 1).where(Votes.id == choice_id)
    query.execute()
    return redirect(f'/topic/{topic_id}')


if __name__ == "__main__":
    db.connect()
    db.create_tables([Topics, Votes])
    extra_files = glob('templates-orm/*')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run("0.0.0.0", 5000, extra_files=extra_files)
