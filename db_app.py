from collections import defaultdict
from glob import glob
from os.path import dirname, join

from flask import Flask, request, render_template, redirect

from db import VoteDB

template_folder = join(dirname(__file__), "templates")
app = Flask(__name__, template_folder=template_folder)
app.static_folder = 'static'
topics = dict({'85a1e80c-33b8-4fa3-8291-9ad09cca2350': {
    'name': 'Mom\'s birthday gift.',
    'data': defaultdict(int)
}})

db = VoteDB()


# 1 test hello world web app
@app.route('/test')
def hello_world():
    return 'Hello, World!'


# 2 components of URL
# call with /path/hello_world?name=john&vote=20
@app.route("/path/<param>")
def url_comp(param):
    print(param)
    print(request.args)


@app.route('/')
def index():
    ntopics = db.get_topic_names()
    return render_template("db/index.html", topics=ntopics)


@app.route('/newTopic', methods=["GET"])
def get_new_topic():
    return render_template("db/new_topic.html")


@app.route('/newTopic', methods=["POST"])
def post_new_topic():
    topic_name = request.form.get("name")
    assert topic_name is not None
    db.add_topic(topic_name)
    return redirect('/')


@app.route('/topic/<topic_id>', methods=["GET"])
def view_topic(topic_id):
    if not db.is_topic_exists(topic_id):
        return 'Topic Not Found', 404
    votes, topic_name = db.get_topic(topic_id)
    return render_template("db/topic.html",
                           topic=votes,
                           topic_id=topic_id,
                           topic_name=  topic_name
                           )


@app.route('/topic/<topic_id>/newChoice', methods=['POST'])
def new_topic_choice(topic_id):
    if not db.is_topic_exists(topic_id):
        return 'Topic not found', 404
    choice = request.form.get('choice')
    db.add_choice(choice, topic_id)
    return redirect(f'/topic/{topic_id}')


@app.route('/topic/<topic_id>/vote', methods=['POST'])
def vote_topic_choice(topic_id):
    assert db.is_topic_exists(topic_id)
    choice_id = request.form.get('choice')
    if choice_id is None:
        return "Invalid choice name", 400
    db.vote(choice_id, topic_id)
    return redirect(f'/topic/{topic_id}')


# @app.route('/choice/add', methods=["POST"])
# def add_choice():
#     query = request.form
#     if "choice" in query:
#         votes[query['choice']] = 0  # initialize list to keep track of votes
#     return render_template("vote.html", votes=votes)
#
# # TODO error catching if `name` not in `votes`
# @app.route('/vote', methods=["POST"])
# def vote():
#     name = request.form.get("name")
#     votes[name] += 1
#     return render_template("vote.html", votes=votes)


if __name__ == "__main__":
    extra_files = glob('templates/db/*')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run("0.0.0.0", 5000, extra_files=extra_files)
