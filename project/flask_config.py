from dotenv import load_dotenv
import brevo_python, os

load_dotenv()

configuration = brevo_python.Configuration()
configuration.api_key['api-key'] = os.getenv("BREVO-API-KEY")

api_instance = brevo_python.TransactionalEmailsApi(brevo_python.ApiClient(configuration))