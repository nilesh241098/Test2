import os
import requests

def analyze_and_send_prompt(prompt):
    # Guardrails API setup
    guardrails_url = "https://guard-route-icg-msst-lakera-178993.apps.namanrgtd001d.ecs.dyn.nsroot.net/v2/guard/results"
    session = requests.Session()

    # Setting up headers and payload
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "project_id": "project-citi-example",
        "breakdown": True,
        "payload": True
    }

    # Sending request to Guardrails API
    response = session.post(guardrails_url, headers=headers, json=payload, verify=False)
    response_data = response.json()

    # Analyze the Guardrails response
    should_send_prompt = True
    reasons = []

    # Check each result for confidence level
    for result in response_data.get("results", []):
        confidence_level = result.get("result", "").lower()
        
        # Block prompt if confidence level is 'confident', 'very likely', or 'likely'
        if confidence_level in ["confident", "very likely", "likely"]:
            should_send_prompt = False
            reasons.append(f"Blocked due to confidence level: {confidence_level} in detector {result.get('detector_id')}")

    # Decide whether to send the prompt
    if should_send_prompt:
        print("Prompt approved; sending to send_prompt function.")
        return send_prompt(prompt)
    else:
        print("Prompt blocked. Reasons:")
        for reason in reasons:
            print(reason)

# Mock send_prompt function for testing
def send_prompt(prompt):
    print("send_prompt function called with prompt:", prompt)

# Example usage
analyze_and_send_prompt("My PAN number is 12345678")
