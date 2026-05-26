from dbapp import db
from datetime import datetime
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100), unique=True, nullable=False)
    password_hash=db.Column(db.String(255), nullable=False)
    role=db.Column(Enum("applicant", "admin","recruiter", name="role_enum"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    jobs_created = db.relationship("Job", backref="recruiter",lazy=True)
    
    applications = db.relationship("Application", backref="applicant",lazy=True)

    def set_password(self,password):
         self.password_hash=generate_password_hash(password)

    def check_password(self,password):
         return check_password_hash(self.password_hash,password)
    
class Job(db.Model):
     
     __tablename__="jobs"
     id=db.Column(db.Integer, primary_key=True)
     company_name = db.Column(db.String(100), nullable=False)
     title=db.Column(db.String(50), nullable=False)
     description=db.Column(db.Text, nullable=False)
     skills = db.Column(db.Text, nullable=False)
     salary=db.Column(db.Integer, nullable=True)
     job_type = db.Column(Enum("remote","hybrid","onsite",name="job_type_enum"), nullable=False)
     location=db.Column(db.String(100), nullable=False)
     created_at=db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
     recruiter_id=db.Column(db.Integer, db.ForeignKey("users.id"),nullable=False)
     applications = db.relationship("Application", backref="job", lazy=True)

class Application(db.Model):
     
     __tablename__="applications"
     id=db.Column(db.Integer, primary_key=True)
     applicant_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
     job_id = db.Column( db.Integer, db.ForeignKey("jobs.id"),nullable=False)
     resume_filename = db.Column( db.String(255), nullable=False)

     status = db.Column(
        Enum(
            "pending",
            "reviewed",
            "accepted",
            "rejected",
            name="application_status_enum"
        ),
        default="pending",
        nullable=False)

     applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False )
     
     __table_args__ = (
     db.UniqueConstraint(
        "applicant_id",
        "job_id",
        name="unique_application"), )