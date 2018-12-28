from ..models import User


def username_to_line_user_id(username):
    user = User.query.filter_by(aws_user_name=username).first()
    return user.line_user_id

def line_user_id_to_username(line_user_id):
    user = User.query.filter_by(line_user_id=line_user_id).first()
    return user.aws_user_name
