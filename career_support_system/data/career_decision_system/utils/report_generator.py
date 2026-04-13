from fpdf import FPDF


class CareerPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "AI-Based Career Decision Support Report", ln=True, align="C")
        self.ln(3)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(228, 239, 242)
        self.cell(0, 8, title, ln=True, fill=True)
        self.ln(2)

    def section_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 7, text)
        self.ln(1)


def generate_career_report(file_path, context):
    pdf = CareerPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.section_title("Student Details")
    pdf.section_text(f"Student Name: {context.get('student_name', 'N/A')}")

    pdf.section_title("Selected Job Role")
    pdf.section_text(context.get("selected_role", "No role selected yet."))

    extracted_skills = context.get("extracted_skills", [])
    pdf.section_title("Extracted Skills")
    pdf.section_text(", ".join(extracted_skills) if extracted_skills else "No skills extracted.")

    required_skills = context.get("required_skills", [])
    pdf.section_title("Required Skills For Selected Role")
    pdf.section_text(", ".join(required_skills) if required_skills else "No selected role requirements available.")

    missing_skills = context.get("missing_skills", [])
    pdf.section_title("Missing Skills")
    pdf.section_text(", ".join(missing_skills) if missing_skills else "No missing skills.")

    recommendations = context.get("recommendations", [])
    pdf.section_title("All Matching Roles")
    if recommendations:
        for item in recommendations:
            pdf.section_text(f"{item['role']} - Match Score: {item['match_score']}%")
    else:
        pdf.section_text("No role recommendations available.")

    learning_guidance = context.get("learning_guidance", {})
    pdf.section_title("Learning Guidance")
    if learning_guidance:
        for skill, guidance in learning_guidance.items():
            topics = ", ".join(guidance.get("topics", []))
            start = guidance.get("start", "Start with the fundamentals.")
            how_to_learn = guidance.get("how_to_learn", "Use short lessons and practice daily.")
            daily_minutes = guidance.get("daily_minutes", 30)
            pdf.section_text(
                f"Skill: {skill}\n"
                f"Topics: {topics}\n"
                f"Where to start: {start}\n"
                f"How to learn: {how_to_learn}\n"
                f"Daily time: {daily_minutes} minutes"
            )
    else:
        pdf.section_text("No guidance needed.")

    reference_links = context.get("reference_links", [])
    pdf.section_title("Reference Links")
    pdf.section_text("\n".join(reference_links) if reference_links else "No reference links available.")

    practice_sites = context.get("practice_sites", [])
    pdf.section_title("Practice Websites")
    pdf.section_text("\n".join(practice_sites) if practice_sites else "No practice sites available.")

    daily_plan = context.get("daily_plan", [])
    pdf.section_title("Learning Program")
    if daily_plan:
        for item in daily_plan:
            pdf.section_text(
                f"Day {item['day']}: {item['skill']} - {item['task']} ({item['minutes']} minutes)"
            )
    else:
        pdf.section_text("No learning program generated.")

    readiness_score = context.get("readiness_score", 0)
    previous_score = context.get("previous_score", 0)
    streak_days = context.get("streak_days", 0)
    progress_summary = context.get("progress_summary", {})
    pdf.section_title("Progress Summary")
    pdf.section_text(
        f"Previous Resume Score: {previous_score}%\n"
        f"Current Resume Score: {readiness_score}%\n"
        f"Current Daily Streak: {streak_days} day(s)\n"
        f"Completed Skills: {progress_summary.get('completed', 0)}\n"
        f"In Progress Skills: {progress_summary.get('in_progress', 0)}\n"
        f"Not Started Skills: {progress_summary.get('not_started', 0)}"
    )

    daily_updates = context.get("daily_updates", [])
    pdf.section_title("Daily Learning Updates")
    if daily_updates:
        for row in daily_updates:
            task_text = row["task_text"] if "task_text" in row.keys() else f"{row['skill_name']} - {row['status']}"
            update_date = row["update_date"] if "update_date" in row.keys() else row["recorded_at"][:10]
            day_label = row["day_number"] if "day_number" in row.keys() else "-"
            pdf.section_text(f"Day {day_label} - {update_date}: {task_text}")
    else:
        pdf.section_text("No daily learning updates saved yet.")

    pdf.output(file_path)
