from os import environ
from dotenv import load_dotenv

load_dotenv()

token = environ.get('anprim_token')

channel_suggest = 1251084876824707123  # 1170031835728859208
channel_suggest_accept = 1251084909733478421

accept_roles = [900466077107105792, 1250042528217038950,
                1133173635163619499, 1136621353320054834, 1133173638456164352]
