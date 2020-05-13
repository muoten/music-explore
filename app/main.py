import json
from pathlib import Path

from flask import Flask, render_template, url_for, g
import plotly
import yaml

from visualize.commons import load_embeddings, reduce
from visualize.web import get_plotly_fig
from data import EMBEDDING_LABELS

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')


def get_metadata():
    if 'metadata' not in g:
        with open(Path(__file__).parent / 'metadata.yaml') as fp:
            g.metadata = yaml.safe_load(fp)
    return g.metadata


def get_metadata_dict(entity):
    metadata = get_metadata()
    return {key: value['name'] for key, value in metadata[entity].items()}


@app.route('/')
@app.route('/playground')
def playground():
    return render_template('playground.html',
                           datasets=get_metadata_dict('datasets'),
                           models=get_metadata_dict('models'))


@app.route('/explore')
def explore():
    track_ids = ['1022300:27:30', '1080900:0:3', '1080900:30:33']
    return render_template('explore.html', audio_urls=[get_audio_url(track_id)['url'] for track_id in track_ids])


def jamendo_template(track_id):
    token = app.config["JAMENDO_CLIENT_ID"]
    if not token:
        raise EnvironmentError('Jamendo client ID is not set')
    return f'https://mp3l.jamendo.com/?trackid={track_id}&format=mp31&from=app-{app.config["JAMENDO_CLIENT_ID"]}'


def localhost_template(track_id):
    return url_for('static', filename=f'audio/{int(track_id) % 100:02}/{track_id}.mp3')


@app.route('/jamendo/<string:track_id>')
def get_audio_url(track_id):
    is_segmented = ':' in track_id
    url_suffix = ''
    if is_segmented:
        track_id, start, end = track_id.split(':')
        url_suffix = f'#t={start},{end}'

    url = localhost_template(track_id) if app.config['SERVE_AUDIO_LOCALLY'] else jamendo_template(track_id)

    return {
        'url': url + url_suffix
    }


@app.route('/tags')
def get_tags():
    return json.dumps(EMBEDDING_LABELS)


@app.route('/plot/<string:plot_type>/<string:embeddings_type>/<int:n_tracks>/<string:projection_type>/<int:x>/<int:y>')
def plot(plot_type, embeddings_type, n_tracks, projection_type, x, y):
    try:
        embeddings_dir = Path(app.config['EMBEDDINGS_DIR'])
        if projection_type == 'original':
            embeddings_dir /= embeddings_type
        elif projection_type in ['pca', 'tsne']:
            if app.config['USE_PRECOMPUTED_PCA']:
                embeddings_dir /= f'{embeddings_type}_pca'  # lesser evil so far
            else:
                raise NotImplementedError('Dynamic PCA is not supported yet')
        else:
            raise ValueError(f"Invalid projection_type: {projection_type}, should be 'original', 'pca' or 'tsne'")

        dimensions = [x, y] if projection_type in ['original', 'pca'] else None
        embeddings, names = load_embeddings(embeddings_dir, n_tracks=n_tracks, dimensions=dimensions)

        if projection_type == 'tsne':
            embeddings = reduce(embeddings, projection_type, n_dimensions_out=2)

        figure = get_plotly_fig(embeddings, names, plot_type)

        if projection_type == 'original' and embeddings_type == 'taggrams':
            figure.update_layout(
                xaxis_title=EMBEDDING_LABELS[x],
                yaxis_title=EMBEDDING_LABELS[y]
            )
    except ValueError as e:
        return {'error': str(e)}, 400

    return json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
