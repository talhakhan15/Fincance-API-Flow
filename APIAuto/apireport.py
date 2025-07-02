import pytest
import requests
import random
import re
import allure

headers = {
    "X-Secret-Key": "REPLACE_WITH_YOUR_SECRET_KEY",
    "Content-Type": "application/x-www-form-urlencoded"
}
base_url = "https://example.com"

# Shared payload data
shared_data = '''{
    "aud": "https://api.example.com/callback",
    "exp": 1711968180,
    "iat": 1711968030,
    "iss": "https://auth.example.com",
    "jti": "dummy-jti",
    "nbf": 1711968030,
    "sub": "1234567890",
    "logId": 123456789,
    "gender": "M",
    "status": "COMPLETED",
    "transId": "dummy-transaction-id",
    "PersonId": 1234567890,
    "jwks_uri": "https://auth.example.com/api/v1/jwk",
    "lastName": "LastName",
    "firstName": "FirstName",
    "thirdName": "MiddleName",
    "secondName": "SecondName",
    "ServiceName": "ServiceName",
    "iqamaNumber": "1234567890",
    "dateOfBirthG": "01-01-1990",
    "dateOfBirthH": "01-01-1410",
    "drivingLicenses": null,
    "englishLastName": "LASTNAME",
    "iqamaIssueDateG": "01-01-2020",
    "iqamaIssueDateH": "01-01-1440",
    "nationalAddress": [{
        "city": "CITY",
        "cityId": "1",
        "cityL2": "CITY_IN_LOCAL",
        "district": "District",
        "postCode": "00000",
        "regionId": "1",
        "streetL2": "Street Local",
        "districtID": null,
        "districtL2": "District Local",
        "regionName": "Region",
        "streetName": "Street",
        "unitNumber": null,
        "regionNameL2": "Region Local",
        "shortAddress": "ADDR1234",
        "buildingNumber": "1234",
        "additionalNumber": "5678",
        "isPrimaryAddress": "true",
        "locationCoordinates": "0.000000 0.000000"
    }],
    "nationalityCode": 999,
    "nationalityDesc": "Nationality",
    "englishFirstName": "FIRST",
    "englishThirdName": "MIDDLE",
    "iqamaExpiryDateG": "01-01-2030",
    "iqamaExpiryDateH": "01-01-1450",
    "englishSecondName": "SECOND",
    "iqamaVersionNumber": 1,
    "iqamaIssuePlaceCode": 1,
    "iqamaIssuePlaceDesc": "Place"
}'''


@pytest.fixture(scope="module")
def user_data():
    nid = str(random.randint(1000000000, 9999999999))
    mobile_no = "9668" + str(random.randint(100000, 999999))
    payload = {
        "nid": nid,
        "mobile_no": mobile_no,
        "product_id": "1",
        "data": shared_data,
        "is_pep": "false"
    }
    res = requests.post(base_url + "/api/user-register", headers=headers, data=payload)
    assert res.status_code == 200, f"Register failed: {res.status_code} - {res.text}"
    user_id = res.json()["data"]["user"]["user_id"]
    return {"nid": nid, "mobile_no": mobile_no, "user_id": user_id}


@allure.title("Test Case 1: New User Register")
def test_user_register(user_data):
    assert user_data["user_id"] is not None


@allure.title("Test Case 2: Update Data")
def test_update_data(user_data):
    payload = {"nid": user_data["nid"], "data": shared_data}
    res = requests.post(base_url + "/api/update-data", headers=headers, data=payload)
    assert res.status_code == 200


@allure.title("Test Case 3: Accept Terms")
def test_accept_terms(user_data):
    payload = {
        "is_terms_conditions_accepted": "1",
        "user_id": user_data["user_id"],
        "privacy_accepted": "1",
        "third_party_consent": "1"
    }
    res = requests.post(base_url + "/api/accept-terms", headers=headers, data=payload)
    assert res.status_code == 200


@allure.title("Test Case 4: Step Finance")
def test_step_finance(user_data):
    payload = {
        "product_id": "1",
        "user_id": user_data["user_id"],
        "step": "finance",
        "amount": "1500",
        "duration": "3",
        "purpose_of_finance_id": "1"
    }
    res = requests.post(base_url + "/api/loan-application", headers=headers, data=payload)
    assert res.status_code == 200


@allure.title("Test Case 5: Step Verification")
def test_step_verification(user_data):
    salary_data = '[{"fullName":"Test User","basicWage":10200,"employerName":"Company"}]'
    payload = {
        "user_id": user_data["user_id"],
        "product_id": "1",
        "step": "verification",
        "salary": salary_data
    }
    res = requests.post(base_url + "/api/loan-application", headers=headers, data=payload)
    assert res.status_code == 200


@allure.title("Test Case 6: Step Consent")
def test_step_consent(user_data):
    payload = {
        "user_id": user_data["user_id"],
        "product_id": "1",
        "step": "consent"
    }
    res = requests.post(base_url + "/api/loan-application", headers=headers, data=payload)
    assert res.status_code == 200


@allure.title("Test Case 7: Step Risk Assessment")
def test_step_risk_assessment(user_data):
    risk_params = '{"wallet_age_months":12,"monthly_average_balance":15000}'
    payload = {
        "user_id": user_data["user_id"],
        "product_id": "1",
        "step": "risk_assessment",
        "risk_params": risk_params
    }
    res = requests.post(base_url + "/api/loan-application", headers=headers, data=payload)
    assert res.status_code == 200


@allure.title("Test Case 8: Step Contract")
def test_step_contract(user_data):
    payload = {
        "user_id": user_data["user_id"],
        "product_id": "1",
        "step": "contract"
    }
    res = requests.post(base_url + "/api/loan-application", headers=headers, data=payload)
    assert res.status_code == 200
    global otp
    otp = re.search(r"\b(\d{4,6})\b", res.text)
    assert otp, "OTP not found"


@allure.title("Test Case 9: Step OTP")
def test_step_otp(user_data):
    assert otp, "OTP must be available"
    payload = {
        "product_id": "1",
        "user_id": user_data["user_id"],
        "step": "otp",
        "otp": otp.group(1)
    }
    res = requests.post(base_url + "/api/loan-application", headers=headers, data=payload)
    assert res.status_code == 200


@allure.title("Test Case 10: IVR Callback")
def test_ivr_callback(user_data):
    payload = {
        "digits": "1",
        "callerId": "+1234567890",
        "direction": "outbound-api",
        "recipient": f"+{user_data['mobile_no']}"
    }
    res = requests.post(base_url + "/api/callback/ivr", headers=headers, data=payload)
    assert res.status_code == 200


#to run

# pytest apireport.py --alluredir=allure-results
# allure serve allure-results
# allure generate allure-results -o allure-report --clean


