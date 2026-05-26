import os
from dbapp import db
from dotenv import load_dotenv
from auth.auth import registering,logingin
from flask import Flask,jsonify,request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt, get_jwt_identity
from services.operations import JobsCreation, ListAppliedJobs, ApplyJobs, Listjobs, DeleteJob

app=Flask(__name__)

load_dotenv()

DATABASE_URL=os.environ.get("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
db.init_app(app)
jwt=JWTManager(app)

with app.app_context():
    db.create_all()



@app.route("/")
def home():
    return jsonify({"success":True, "Project":"Job Portal Project", "Status":"Running","Developer":"Ram Siddharth"}),200


@app.route("/register",methods=["POST"])
def registration():
    data=request.get_json()

    regi=registering(data.get("email"), data.get("password"), role="applicant") 
    
    return (jsonify(regi), 201) if regi["success"] else (jsonify(regi), 400)


@app.route("/admin/register",methods=["POST"])
@jwt_required()
def AdminRegistration():

    data=request.get_json()
    claims=get_jwt()
    Role=claims.get("role")
    if (Role!="admin"):
        return jsonify({"success":False, "Error":"Access denied"}),403

    regi=registering(data.get("email"), data.get("password"), role="admin") 
    
    return (jsonify(regi), 201) if regi["success"] else (jsonify(regi), 400)


@app.route("/recruiter/register",methods=["POST"])
@jwt_required()
def RecruiterRegistration():

    data=request.get_json()
    claims=get_jwt()
    Role=claims.get("role")
    if (Role!="admin"):
        return jsonify({"success":False, "Error":"Access denied"}),403

    regi=registering(data.get("email"), data.get("password"), role="recruiter") 
    
    return (jsonify(regi), 201) if regi["success"] else (jsonify(regi), 400)



@app.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")
    log=logingin(email,password)

    if (not email or not password ):
        return ({"success":False, "Error":" Email and password required "}),400
    
    return (jsonify(log), 200) if log["success"] else (jsonify(log), 401)


@app.route("/createjobs", methods=["POST"])
@jwt_required()
def createjobs():
    data=request.get_json()
    claims=get_jwt()
    Role=claims.get("role")
    identity=get_jwt_identity()
    if Role not in ["recruiter", "admin"]:
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    newjob=JobsCreation(data.get("company_name"), data.get("title"), data.get("description"), data.get("skills"), data.get("salary"), data.get("job_type"), data.get("location"), identity, Role)

    return (jsonify(newjob), 201) if newjob["success"] else (jsonify(newjob), 400)

@app.route("/listjobs")
def AllJobsList():
    listthejobs=Listjobs()
    return (jsonify(listthejobs),200) if listthejobs["success"] else (jsonify(listthejobs),404)



@app.route("/applyjob", methods=["POST"])
@jwt_required()
def ApplyForAJob():
    claims=get_jwt()
    Role=claims.get("role")
    identity=get_jwt_identity()

    if (Role!="applicant"):
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    job_id=request.form.get("job_id")
    resume=request.files.get("resume")

    applied=ApplyJobs(Role,identity,job_id,resume)

    return (jsonify(applied),200) if applied["success"] else (jsonify(applied),404)

    

@app.route("/listappliedjob")
@jwt_required()
def ListAppliedJob():
    claims=get_jwt()
    Role=claims.get("role")
    identity=get_jwt_identity()

    if (Role!="applicant"):
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    ListAppliedJob=ListAppliedJobs(Role,identity)
    return (jsonify(ListAppliedJob),200) if ListAppliedJob["success"] else (jsonify(ListAppliedJob),404)


@app.route("/remove/job", methods=["DELETE"])
@jwt_required()
def DeleteAJob():
    claims=get_jwt()
    data=request.get_json()
    Role=claims.get("role")
    identity=get_jwt_identity()

    if Role not in ["recruiter", "admin"]:
        return jsonify({"success":False, "Error":"Access denied"}),403
    
    DeleteAJob=DeleteJob(Role, identity, data.get("title"), data.get("company name"))

    return (jsonify(DeleteAJob),200) if DeleteAJob["success"] else (jsonify(DeleteAJob),404)  