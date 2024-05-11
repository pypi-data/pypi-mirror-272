from bs4 import BeautifulSoup
from datetime import datetime
import lh3.api
from pprint import pprint as tprint


def check_operator_response(chat_id, constant_contact=5):
    client = lh3.api.Client()
    transcript = (
        client.one("chats", chat_id).get()["transcript"] or "No transcript found"
    )
    api_call = client.one("chats", chat_id).get()

    student_id = api_call.get("guest").get("jid")
    operator_username = api_call.get("operator").get("name")

    html_content = transcript
    soup = BeautifulSoup(html_content, "html.parser")

    previous_student_time = None
    previous_operator_time = None

    counter = 0
    discrepancies = list()

    for div in soup.find_all("div"):
        span = div.find("span")
        if span:
            text = div.text.strip()
            if "System message:" in text:
                time = text.split()[0]
                current_time = datetime.strptime(time, "%H:%M%p")
                previous_student_time = current_time
                previous_operator_time = current_time
                continue  # Skip lines containing "System message:"

            time = text.split()[0]
            sender = span.text.split("@")[1]  # Extract domain from email address

            # Determine sender type
            if student_id in text:
                sender_type = "Student"
                current_time = datetime.strptime(time, "%H:%M%p")
                previous_student_time = current_time
            elif operator_username in text:
                sender_type = "Operator"
                current_time = datetime.strptime(time, "%H:%M%p")
                previous_operator_time = current_time
                try:
                    time_difference = (
                        current_time - previous_student_time
                    ).total_seconds() / 60
                except:
                    time_difference = 0
                if time_difference >= constant_contact:
                    print(
                        f"Operator took more than {constant_contact} minutes to reply after previous student message."
                    )
                    counter += 1
                    discrepancies.append(
                        {
                            "counter": counter,
                            "line": text[0:15],
                            "time_difference": int(time_difference),
                            "ChatId": chat_id,
                        }
                    )

                    # Print the message
                    # print(f"ChatId: {chat_id} - Student time: {previous_student_time} - Operator time:  {time} - {sender_type}: Message: {text}")

                    # reset the timer for students to avoid duplicates
                    previous_student_time = current_time

    # if discrepancies:
    # tprint(discrepancies)
    return discrepancies


"""
def main():
    chat_ids = [3423927, 3423928, 3423929]  # List of chat IDs to test
    for chat_id in chat_ids:
        result = check_operator_response(chat_id)

if __name__ == "__main__":
    main()
"""
