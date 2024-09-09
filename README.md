# Grass Form Submission

I have made only for introductory purposes, I do not encourage anyone to use this software, it is prohibited by law.
This project automates the process of submitting forms for Grass accounts.



## Setup

1. Clone the repository:
   ```
   git clone https://github.com/onelock/grass-form-sybil.git
   cd grass-form-submission
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Prepare your data files in the `data` directory:
   - `login_password.txt`: Contains login:password pairs (grass account)
   - `proxies.txt`: Contains proxy addresses/ format http://login:password@ip:port only static
   - `referral_methods.txt`: Here write in a column the text that will send the code to the question: “Please explain your method of getting referrals?”
   - `additional_info.txt`: Here write in a column the text that will send the code to the question: “Why do you think your account was mislabeled as having abnormal network activity?”

5. Run the script:
   ```
   python src/run.py
   ```

## Configuration

You can modify the `src/config.py` file to adjust timeouts, API keys, and other settings.

## Results

- Successful submissions will be logged in `log_result/successful_accounts.txt`
- Failed submissions will be logged in `log_result/failed_accounts.txt`
- General logs can be found in `log_result/log.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.