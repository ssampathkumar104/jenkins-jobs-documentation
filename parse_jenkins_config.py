import xml.etree.ElementTree as ET

# Load the XML downloaded from Jenkins
tree = ET.parse('4_ExecuteMultiplePlanesInParallel_job_config.xml')
root = tree.getroot()

with open("4_ExecuteMultiplePlanesInParallel_job_config.txt", "w", encoding="utf-8") as doc:
    doc.write(f"=========================================\n")
    doc.write(f"JENKINS JOB CONFIGURATION DOCUMENTATION\n")
    doc.write(f"=========================================\n\n")

    # 1. Document Job Description
    description = root.find('description')
    doc.write(f"## Description:\n")
    doc.write(f"{description.text if description is not None else 'No description provided.'}\n\n")

    # 2. Document Build Parameters
    doc.write(f"## Job Parameters / Input Variables:\n")
    parameters = root.findall('.//parameterDefinitions/*')
    for p in parameters:
        name = p.find('name')
        if name is not None:
            default_val = p.find('defaultValue')
            val_text = default_val.text if default_val is not None else "None"
            doc.write(f" - Parameter Name: {name.text} (Default: {val_text})\n")
    
    doc.write(f"\n## Build Execution Steps:\n")
    
    # 3. Extract Shell Build Steps (For Freestyle Jobs)
    shell_steps = root.findall('.//hudson.tasks.Shell/command')
    for idx, step in enumerate(shell_steps, 1):
        doc.write(f"### Step {idx}: Shell Command Script\n")
        doc.write(f"```bash\n{step.text.strip()}\n```\n\n")

    # 4. Extract Pipeline Scripts (If it's a Pipeline Job)
    pipeline_script = root.find('.//definition/script')
    if pipeline_script is not None:
        doc.write(f"### Pipeline Groovy Script:\n")
        doc.write(f"```groovy\n{pipeline_script.text.strip()}\n```\n")

print("Document generated successfully: Jenkins_Job_Documentation.txt")