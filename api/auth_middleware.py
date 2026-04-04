# from functools import wraps
# def login_required(f):
#  @wraps(f)
#  def wrapper(*args, **kwargs):
#  token = request.headers.get("Authorization")
#  decoded = jwt.decode(token, 
#  SECRET_KEY, algorithms=["HS256"])
#  return f(*args, **kwargs)
#  return wrapper