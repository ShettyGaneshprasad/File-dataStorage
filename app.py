

from sys import exit
from flask import Flask
from argparse import ArgumentParser
from configs import settings, configurations
from utils.filehandler import FilePreprocess
from CRD.views import CreateData, ReadData, DeleteData

parser = ArgumentParser()
parser.add_argument('--datastore', help='Enter the datastore absolute path.')
args = parser.parse_args()


if args.datastore:
    db_path = args.datastore
else:
    db_path = configurations.DEFAULT_DB_PATH

directory_created = FilePreprocess(db_path).create_folder()
if not directory_created:
    print(
        f"Permission denied: You can not create the directory `{db_path}`.\n")
    exit(0)


app = Flask(__name__)


app.config['DEBUG'] = settings.DEBUG
app.config['SECRET_KEY'] = settings.SECRET_KEY


app.add_url_rule('/datastore/create',
                 view_func=CreateData.as_view('create', db_path), methods=['POST'])
app.add_url_rule('/datastore/read',
                 view_func=ReadData.as_view('read', db_path), methods=['GET'])
app.add_url_rule('/datastore/delete',
                 view_func=DeleteData.as_view('delete', db_path), methods=['DELETE'])


if __name__ == '__main__':
    app.run(host=settings.HOST, port=settings.PORT)
