from dotenv import load_dotenv
import os, resend
load_dotenv()
resend.api_key = os.environ["RESEND_API_KEY"]

params: resend.Domains.CreateParams = {
  "name": "verify-codes.gptquiz.com",
}

resend.Domains.get(domain_id="7aabebbe-5941-42a2-bd7f-06fc21d8060e")