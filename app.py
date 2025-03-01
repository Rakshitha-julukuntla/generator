from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resume', methods=['POST'])
def generate_resume():
    data = request.form.to_dict()

    # Save uploaded photos
    photo_paths = {}
    for key in ['photo1', 'photo2']:  
        if key in request.files:
            photo = request.files[key]
            if photo.filename:
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
                photo.save(photo_path)
                photo_paths[key] = f"/{photo_path}"

    # Convert comma-separated values into list
    def format_list(text):
        return [item.strip() for item in text.split(",") if item.strip()]

    # Professional Summary
    field = data.get("field", "").lower()
    profile_description = data.get("profile_description", "")
    summary = f"<strong>{profile_description}</strong><br>"

    summary += ("Passionate IT professional specializing in software development and data science."
                if field == "it" else
                "Experienced Non-IT professional with strong analytical and management skills.")

    # Format projects
    project_names = format_list(data.get('projects', ""))
    tech_stacks = format_list(data.get('tech_stacks', ""))
    project_list = [{"name": proj, "tech": tech_stacks[i] if i < len(tech_stacks) else "Various Technologies"}
                    for i, proj in enumerate(project_names)]

    # Format certifications
    certification_names = format_list(data.get('certifications', ""))
    cert_types = format_list(data.get('cert_types', ""))
    certification_list = []
    for i, cert in enumerate(certification_names):
        cert_type = cert_types[i] if i < len(cert_types) else "General"
        description = ("Advanced IT certification demonstrating strong technical skills."
                       if cert_type.lower() == "it" else
                       "Professional certification enhancing expertise in various domains.")
        certification_list.append({"name": cert, "description": description})

    # Format education details
    education_entries = []
    edu_count = len(request.form.getlist("degree"))
    for i in range(edu_count):
        education_entries.append({
            "degree": request.form.getlist("degree")[i],
            "institution": request.form.getlist("institution")[i],
            "start": request.form.getlist("edu_start")[i],
            "end": request.form.getlist("edu_end")[i]
        })

    return render_template(
        'resume_template.html',
        data=data,
        photo1_path=photo_paths.get('photo1', None),
        photo2_path=photo_paths.get('photo2', None),
        summary=summary,
        skills=format_list(data.get('skills', "")),
        experience=format_list(data.get('experience', "")),
        project_list=project_list,
        certification_list=certification_list,
        education_entries=education_entries
    )

if __name__ == '__main__':
    app.run(debug=True)
