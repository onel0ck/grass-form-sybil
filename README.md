# Grass Form Submission

I have made only for introductory purposes, I do not encourage anyone to use this software, it is prohibited by law.
This project automates the process of submitting forms for Grass accounts.

`My X:` https://x.com/1l0ck

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/onel0ck/grass-form-sybil.git
   cd grass-form-sybil
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   cd venv/Scripts
   activate
   cd ../..
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Prepare the data files in the `data` and `config` directories:
   - `login_password.txt`: Contains login:password pairs (grass account)
   - `proxies.txt`: Contains proxy addresses/ format http://login:password@ip:port only static
   - `referral_methods.txt`: Here write in a column the text that will send the code to the question: “Please explain your method of getting referrals?”
   - `additional_info.txt`: Here write in a column the text that will send the code to the question: “Why do you think your account was mislabeled as having abnormal network activity?”
   - `config.py`: You can modify the `src/config.py` file to adjust timeouts, API keys, and other settings.
   - api key capmonster is required

5. Run the script:
   ```
   cd venv/Scripts
   activate
   cd ../..src
   python run.py
   ```

## Results

- Successful submissions will be logged in `log_result/successful_accounts.txt`
- Failed submissions will be logged in `log_result/failed_accounts.txt`
- General logs can be found in `log_result/log.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
