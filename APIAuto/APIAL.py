import requests
import random
import time
import re

headers = {
    "X-Secret-Key": "REPLACE_WITH_YOUR_SECRET_KEY",
    "Content-Type": "application/x-www-form-urlencoded"
}

base_url = "https://example.com"

auth_payload = '''{
    "info": "dummy authentication data"
}'''

def register_client():
    identifier = str(random.randint(1000000000, 9999999999))
    phone_number = "1234" + str(random.randint(100000, 999999))
    print("-----------------------------------------------------------------------------------------")
    payload = {
        "national_id": identifier,
        "phone": phone_number,
        "service_id": "1",
        "auth_data": auth_payload,
        "is_special": "false"
    }
    res = requests.post(base_url + "/api/register", headers=headers, data=payload)
    print("\nStep 1: REGISTER\n")
    print(f" Sent: National ID={identifier}, Phone={phone_number}")
    print("Status:", res.status_code)
    print("Response:", res.text)
    try:
        response_json = res.json()
        client_id = response_json["data"]["client"]["client_id"]
        print(f"Extracted client_id: {client_id}")

        update_auth(identifier)
        accept_conditions(client_id)
        time.sleep(3)
        application_step(client_id)
        application_verification_step(client_id)
        application_consent_step(client_id)
        application_assessment_step(client_id)
        application_finalize_step(client_id)
        simulate_callback(phone_number)

    except Exception as e:
        print("Could not extract client_id:", e)
        print("Skipping next steps...")

def update_auth(identifier):
    print("-----------------------------------------------------------------------------------------")
    print("\nStep 2: UPDATE AUTH DATA\n")
    payload = {
        "national_id": identifier,
        "auth_data": auth_payload
    }
    res = requests.post(base_url + "/api/update-auth", headers=headers, data=payload)
    print(f"Using National ID={identifier}")
    print("Status:", res.status_code)
    print("Response:", res.text)

def accept_conditions(client_id):
    print("-----------------------------------------------------------------------------------------")
    print("\nStep 3: ACCEPT TERMS\n")
    payload = {
        "accepted_terms": "1",
        "client_id": client_id,
        "session": "1",
        "third_party_consent": "1"
    }
    res = requests.post(base_url + "/api/client/accept-terms", headers=headers, data=payload)
    print(f"Using client_id={client_id}")
    print("Status:", res.status_code)
    print("Response:", res.text)

def application_step(client_id):
    print("-----------------------------------------------------------------------------------------")
    print("\nStep 4: APPLICATION - FINANCE\n")
    url = base_url + "/api/application"
    payload = {
        "service_id": "1",
        "client_id": client_id,
        "stage": "finance",
        "amount": "1500",
        "duration": "3",
        "purpose_id": "1"
    }
    res = requests.post(url, headers=headers, data=payload)
    print("Status:", res.status_code)
    print("Response:", res.text)

def application_verification_step(client_id):
    print("-----------------------------------------------------------------------------------------")
    print("\nStep 5: APPLICATION - VERIFICATION\n")
    url = base_url + "/api/application"
    income_data = '[{"fullName":"John Doe","basicSalary":10000,"employer":"ABC Corp","monthsWorked":"24","otherIncome":1000,"employmentStatus":"Active","housingAllowance":3000}]'
    payload = {
        "client_id": client_id,
        "stage": "verification",
        "service_id": "1",
        "income_details": income_data
    }
    res = requests.post(url, headers=headers, data=payload)
    print("Status:", res.status_code)
    print("Response:", res.text)

def application_consent_step(client_id):
    print("-----------------------------------------------------------------------------------------")
    print("\nStep 6: APPLICATION - CONSENT\n")
    url = base_url + "/api/application"
    payload = {
        "client_id": client_id,
        "service_id": "1",
        "stage": "consent"
    }
    res = requests.post(url, headers=headers, data=payload)
    print("Status:", res.status_code)
    print("Response:", res.text)

def application_assessment_step(client_id):
    print("-----------------------------------------------------------------------------------------")
    print("\nStep 7: APPLICATION - ASSESSMENT\n")
    url = base_url + "/api/application"
    assessment_data = '''{
        "wallet_age_months": 12,
        "wallet_txn_activity": 45,
        "avg_wallet_balance": 15000.75,
        "avg_wallet_expense": 8200.50,
        "external_account_txn_activity": 32,
        "avg_external_balance": 22000.00,
        "avg_external_expense": 9400.30,
        "external_account_age_months": 18
    }'''
    payload = {
        "client_id": client_id,
        "service_id": "1",
        "stage": "assessment",
        "assessment_metrics": assessment_data
    }
    res = requests.post(url, headers=headers, data=payload)
    print("Status:", res.status_code)
    print("Response:", res.text)

def application_finalize_step(client_id):
    print("-----------------------------------------------------------------------------------------")
    print("\nStep 8: APPLICATION - FINALIZE\n")
    url = base_url + "/api/application"
    payload = {
        "client_id": client_id,
        "service_id": "1",
        "stage": "finalize"
    }
    res = requests.post(url, headers=headers, data=payload)
    print("Status:", res.status_code)
    print("Response:", res.text)
    try:
        response_json = res.json()
        otp_message = response_json["data"]["application_data"]["details"]["otp"]
        otp_match = re.search(r"\b(\d{4,6})\b", otp_message)
        if otp_match:
            otp = otp_match.group(1)
            print(f"Extracted OTP: {otp}")
            application_otp_step(client_id, otp)
        else:
            print("OTP not found in message.")
    except Exception as e:
        print("Failed to extract OTP:", e)

def application_otp_step(client_id, otp):
    print("-----------------------------------------------------------------------------------------")
    print("\nStep 9: APPLICATION - OTP\n")
    url = base_url + "/api/application"
    payload = {
        "service_id": "1",
        "client_id": client_id,
        "stage": "otp",
        "otp": otp
    }
    res = requests.post(url, headers=headers, data=payload)
    print(f"Sent OTP: {otp}")
    print("Status:", res.status_code)
    print("Response:", res.text)

def simulate_callback(phone):
    print("-----------------------------------------------------------------------------------------")
    print("\nStep 10: SIMULATE CALLBACK\n")
    url = base_url + "/api/callback/simulate"
    payload = {
        "digits": "1",
        "caller_id": "+1234567890",
        "direction": "outbound",
        "recipient": f"+{phone}"
    }
    res = requests.post(url, headers=headers, data=payload)
    print("Status:", res.status_code)
    print("Response:", res.text)

register_client()
