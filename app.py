import uuid
from collections import defaultdict
from glob import glob
from os.path import dirname, join
from flask import Flask, request, render_template, redirect

template_folder = join(dirname(__file__), "templates/")
app = Flask(__name__, template_folder=template_folder)
app.static_folder = 'static'
topics = dict({'85a1e80c-33b8-4fa3-8291-9ad09cca2350': {
    'name': 'Mom\'s birthday gift.',
    'data': defaultdict(int)
}})


@app.route('/')
def index():
    return render_template("default/index.html", topics=topics)


@app.route('/newTopic', methods=["GET"])
def get_new_topic():
    return render_template("default/new_topic.html")


@app.route('/newTopic', methods=["POST"])
def post_new_topic():
    topic_name = request.form.get("name")
    assert topic_name is not None
    topic_id = str(uuid.uuid4())
    topics[topic_id] = {"name": topic_name, "data": defaultdict(int)}
    return redirect('/')


@app.route('/topic/<topic_id>', methods=["GET"])
def view_topic(topic_id):
    if topic_id not in topics:
        return 'Topic Not Found', 404
    topic = topics[topic_id]
    return render_template("default/topic.html",
                           topic=topic,
                           topic_id=topic_id
                           )


@app.route('/topic/<topic_id>/newChoice', methods=['POST'])
def new_topic_choice(topic_id):
    assert topic_id in topics
    choice = request.form.get('choice')
    topics[topic_id]['data'][choice] = 0
    return redirect(f'/topic/{topic_id}')


@app.route('/topic/<topic_id>/vote', methods=['POST'])
def vote_topic_choice(topic_id):
    assert topic_id in topics
    choice = request.form.get('choice')
    if choice is None:
        return "Invalid choice name", 400
    topics[topic_id]['data'][choice] += 1
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
    extra_files = glob('templates/*')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run("0.0.0.0", 5000, extra_files=extra_files)
