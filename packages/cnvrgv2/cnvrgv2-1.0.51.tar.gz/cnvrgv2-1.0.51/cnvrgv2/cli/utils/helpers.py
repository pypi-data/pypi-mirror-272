import os
import sys

import click
from prettytable import PrettyTable
import yaml

from cnvrgv2.utils.url_utils import urljoin


def parse_parameters_from_file(path):
    """
    Parse parameters from command line
    :param parameters: parameters yaml
    :return: parameters list of dicts
    """
    if not os.path.exists(path):
        raise ValueError("The provided parameters yaml path does not exist.")

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    if not data.get("parameters"):
        raise ValueError("The provided parameters yaml is missing the parameters key")

    return data.get("parameters")


def build_grid_url(cnvrg, project, grid_slug):
    """
    Build Grid url
    :param cnvrg: cnvrg object
    :param project: project object
    :param grid_slug: grid slug
    :return: grid url
    """
    grid_path = "{}/experiments?grid={}".format(project._route, grid_slug)
    route = urljoin(cnvrg._proxy._domain, "api", grid_path)
    return route


def callback_log(experiment, log=False):
    if not log:
        return

    end_pos = 0

    def callback():
        nonlocal end_pos
        nonlocal log
        try:
            resp = experiment.info(end_pos=end_pos)
            end_pos = resp.attributes["info"][experiment.slug]["end_pos"]
            logs = resp.attributes["info"][experiment.slug]["logs"]
            for log in logs:
                click.echo(log["message"])
        except Exception as e:
            click.echo("Failed to get logs, error: {}".format(e))

    return callback


def print_file_table_in_chunks(data_owner, chunk_size, limit):
    table = PrettyTable()
    table.field_names = ["Filename", "Size", "SHA1"]
    for field in table.field_names:
        table.align[field] = "l"

    file_counter = 0
    limit = limit or sys.maxsize
    generator = data_owner.list_files()
    while True:
        chunk = []
        file_limit_reached = False
        for i in range(chunk_size):
            try:
                file = next(generator)
                chunk.append([file.file_name, file.file_size, file.sha1])
                file_counter += 1
                if file_counter >= limit:
                    file_limit_reached = True
                    break
            except StopIteration:
                break

        if not chunk:
            # If num of items divides by chunk_size, this break will prevent printing an empty table at the end
            break

        # Clear rows of previous iteration and add rows of current iteration
        table.clear_rows()
        table.add_rows(chunk)

        # Clearing previous print will make it look like the content of the table changes but the structure remains
        click.echo("\n")
        click.echo(table)

        if file_limit_reached or len(chunk) != chunk_size:
            # Partial chunk, means it's the last one. break out of the while loop
            break
        else:
            click.echo("Press any key to show the next chunk of files...", nl=False)
            click.getchar()


def pretty_print_predictions(predictions):
    """
    Pretty print predictions of endpoint
    :@predictions: list of predictions dict
    :return: None
    """
    click.echo("{:<5} {:<20} {:<20} {:<20} {:<13}".format('Model',
                                                          'Time',
                                                          'Input',
                                                          'Output',
                                                          'Elapsed_time'))
    for prediction in predictions:
        click.echo("{:<5} {:<20} {:<20} {:<20} {:<13}".format(prediction["model"],
                                                              prediction["start_time"],
                                                              prediction["input"][:20],
                                                              prediction["output"][:20],
                                                              prediction["elapsed_time"]))
