import flask

reports_app = flask.Blueprint(
    name= 'my_class_app',
    import_name= 'my_class_app',
    static_folder= 'static',
    template_folder= 'templates',
    static_url_path= '/my_class/'
)