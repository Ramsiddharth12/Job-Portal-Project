import os
from dbapp import db
from datetime import datetime
from models import Job, Application
from werkzeug.utils import secure_filename
from utils.s3uploads import upload_resume
from validators.jobvalidator import job_validation

def JobsCreation(company_name, title, description, skills, salary, job_type, location, identity, Role):

    if (Role!="recruiter"):
        return ({"success":False, "Error":"Access denied"})
        
    data = { "company_name": company_name, "title": title, "description": description, "skills": skills,"salary": salary,"job_type": job_type, "location": location}

    validate=job_validation(data)

    if (not validate["success"]):
        return (validate)
    
    try:
        newjob=Job(company_name=company_name, title=title, description=description, skills=skills, salary=salary, job_type=job_type, location=location, recruiter_id=identity)
        db.session.add(newjob)
        db.session.commit()

        return({"success":True, "message":"A new job has been successfully completed"})

    except Exception as e:
        db.session.rollback()
        return({"success":False, "Error":str(e)})

        

def ApplyJobs(Role,identity,job_id,resume):
    if (Role!="applicant"):
        return ({"success":False, "Error":"Access denied"})
    
    try:
        job=Job.query.get(job_id)

        if (not job):
            return ({"success":False, "message":"Job not found"})
        
        if (not resume):
            return ({"success":False, "message":"Resume required"})
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename=secure_filename(f"{timestamp}_{resume.filename}")

        resume_url = upload_resume(resume,filename)

        new_application=Application(applicant_id=identity, job_id=job_id, resume_filename=resume_url)

        db.session.add(new_application)
        db.session.commit()

        return({"success":True, "message":"successfully applied for the job"})
    
    except Exception as e:
        db.session.rollback()

        return ({"success":False, "Error":str(e)})
    


def Listjobs():
    jobs=Job.query.all()

    if not jobs:
        return ({"success":False, "message":"There are no jobs available"})

    jobslist=[]

    for job in jobs:

        jobslist.append({"job id": job.id, "Company Name": job.company_name, "Role": job.title, "description": job.description,
                          "required skills": job.skills,"salary": job.salary, "job type": job.job_type, "location": job.location, "job posted time": job.created_at})
    
    return({"success":True, "jobs":jobslist})
        
    

def ListAppliedJobs(Role, identity):
    if (Role!="applicant"):
        return ({"success":False, "Error":"Access denied"})
    
    application=Application.query.filter(Application.applicant_id==identity).all()

    if not application:
        return ({"success":False, "message":"Start applying for jobs"})
    
    ApplicationsList=[]
    
    for apps in application:

        ApplicationsList.append({"applicant id":apps.applicant_id, "job id":apps.job_id, "resume filename":apps.resume_filename, "status":apps.status, "applied at":apps.applied_at})

    return({"success":True, "Applied jobs":ApplicationsList})



    

def DeleteJob(Role, identity, title, company_name):

    if Role not in ["recruiter", "admin"]:
        return ({"success":False, "Error":"Access denied"})
    
    if (Role=="admin"):
        job=Job.query.filter(Job.title==title,Job.company_name==company_name).first()

        JOb=job

        if(not JOb):
          return ({"success":False, "Message":"Mentioned Job Not found"})

        db.session.delete(JOb)
        db.session.commit()

        return({"success":True, "Selected job":title, "Message":"Has been successfully removed"})

    if (Role=="recruiter"):

        job=Job.query.filter(Job.recruiter_id==identity, Job.title==title, Job.company_name==company_name).first()

        jOB=job

        if(not jOB):
            return ({"success":False, "Message":"Mentioned Job Not found"})
        
        db.session.delete(jOB)
        db.session.commit()

        return({"success":True, "Selected job":title, "Message":f"The vacancy for {title} Has been successfully removed"})
    