from flask import Flask, send_file
from .libreppc import LibrePPC 

app = Flask(__name__, template_folder='templates')
libreppc = LibrePPC(app)

@app.route('/')
def main_page() -> str:
    return libreppc.render_main()

@app.route('/post/<string:postId>')
def post_page(postId: str) -> str:
    return libreppc.render_post(
        libreppc.find_post_file_id(postId.removesuffix('.html')), 
        postId
    )

@app.route('/pages/<string:filename>')
def project_page(filename: str) -> str:
    return libreppc.render_project_page(
        filename.removesuffix(".html")
    )

@app.route('/feed.atom')
def feed():
    libreppc.generate_rss().atom_file('feed.atom')
    return send_file('feed.atom', download_name='feed.atom', mimetype='application/atom+xml')

if __name__ == '__main__':
    args = libreppc.parse_args()
    if args.build:
        libreppc.load_config()
        libreppc.build()
    elif args.serve:
        libreppc.load_config()
        app.run(debug=True, host="0.0.0.0", use_reloader=True)
    elif args.init:
        libreppc.init()

