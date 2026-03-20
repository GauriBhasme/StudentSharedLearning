class User:
    def __init__(self, name,email,branch, year, password):
        self.name = name
        self.email = email
        self.branch = branch
        self.year = year
        self.password = password

    def __repr__(self):
        return f"<User {self.email}>"

class Request:
    def __init__(self, title, description, teacher, learner, status="new"):
        self.title = title
        self.description = description
        self.teacher = teacher
        self.learner = learner
        self.status = status

    def __repr__(self):
        return f"<Request {self.title} by {self.teacher}>"