def job_validation(data):

    required_fields={"company_name":data.get("company_name"), "title":data.get("title"), "description":data.get("description"), "skills":data.get("skills"), "salary":data.get("salary"), "job_type":data.get("job_type"), "location":data.get("location")}

    for field_name, value in required_fields.items():

        if not value:
            return {"success": False, "Error": f"{field_name} is required"}
        
    valid_job_types=["remote", "hybrid", "onsite"]

    if(required_fields["job_type"] not in valid_job_types):
        return ({"success":False, "Error":"Invalid job_type"})
    
    if(not isinstance(required_fields["salary"],(int,float))):
        return ({"success":False, "Error":" salary should only be in integer "})
    
    if(required_fields["salary"]<0):
        return({"success":False, "Error":"salary cant be less than zero"})
    
    return({"success":True})
