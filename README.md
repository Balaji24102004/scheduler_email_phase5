# Phase 5: Local Scheduling & Orchestration

## 📌 Objective
This phase automates the email marketing campaign using Python's `schedule` library. The script runs daily at a specified time and checks if any campaign email is due to be sent based on the campaign's progress.

---

## 🛠️ Technologies Used
- **Python 3.x**
- `schedule` — for daily execution of the email sending function
- `time` — to keep the script running
- `datetime` — to calculate day offset
- Custom Python modules (`campaign_parser.py`, `campaign_state.py`)

---

## 📂 Files Used in Phase 5

| File Name            | Purpose                                                   |
|---------------------|-----------------------------------------------------------|
| `scheduled_email.py` | Main orchestrator: schedules and runs email sending daily  |
| `campaign_parser.py` | Calculates the `day_offset` based on campaign start date   |
| `campaign_state.py`  | Loads campaign configuration data from JSON               |
| `campaign.json`      | Contains campaign structure and email scheduling details  |
| `campaign_state.json`| Stores campaign progress (sent emails)                    |
| `.env`              | Environment variables (Google API key, Gmail credentials) **(Not uploaded to GitHub)** |

---

## ⚙️ Setup & Running Instructions for Phase 5

1. **Install required libraries:**

```bash
pip install schedule python-dotenv google-generativeai
 scheduler_email_phase5
phase5
