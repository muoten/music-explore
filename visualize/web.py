import numpy as np
import plotly.graph_objects as go

from visualize.commons import get_trajectories, get_averages

PLOTLY_MARKER_SCALE = 10
SEGMENT_LENGTH = 3


def get_trajectories_plotly(embeddings_2d, names):
    trajectories, lengths = get_trajectories(embeddings_2d)
    fig = go.Figure()
    for (x, y), name, length in zip(trajectories, names, lengths):
        ids = list(map(lambda s: f'{name}:{s}:{s + SEGMENT_LENGTH}', np.arange(0, length) * SEGMENT_LENGTH))
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            line_shape='spline',
            ids=ids,
            hovertext=ids,
            hoverinfo='text',
            name=name
        ))
    return fig


def get_segments_plotly(embeddings_2d, names):
    embeddings_stacked = np.vstack(embeddings_2d)
    trajectories, lengths = get_trajectories(embeddings_2d)
    ids = []
    for name, length in zip(names, lengths):
        ids += list(map(lambda s: f'{name}:{s}:{s + SEGMENT_LENGTH}', np.arange(0, length) * SEGMENT_LENGTH))

    fig = go.Figure(data=go.Scatter(
        x=embeddings_stacked[:, 0],
        y=embeddings_stacked[:, 1],
        mode='markers',
        hovertext=ids,
        hoverinfo='text',
        ids=ids
    ))
    return fig


def get_averages_plotly(embeddings_2d, names):
    avg, std = get_averages(embeddings_2d)
    fig = go.Figure(data=go.Scatter(
        x=avg[:, 0],
        y=avg[:, 1],
        mode='markers',
        marker=dict(size=std * PLOTLY_MARKER_SCALE),
        hovertext=names,
        hoverinfo='text',
        ids=names
    ))
    return fig


def get_plotly_fig(embeddings, names, plot_type):
    if plot_type == 'averages':
        fig = get_averages_plotly(embeddings, names)
    elif plot_type == 'trajectories':
        fig = get_trajectories_plotly(embeddings, names)
    elif plot_type == 'segments':
        fig = get_segments_plotly(embeddings, names)
    else:
        raise ValueError(f"Invalid plot_type: {plot_type}, should be 'averages', 'trajectories' or 'segments'")

    return fig