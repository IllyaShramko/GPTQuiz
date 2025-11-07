from dotenv import load_dotenv
import os, resend
load_dotenv()
resend.api_key = os.environ["RESEND_API_KEY"]

params: resend.Domains.CreateParams = {
  "name": "verify-codes.gptquiz.com",
}

resend.Domains.get(domain_id="7b803876-b47d-4ca9-a2f0-e2333956a280")