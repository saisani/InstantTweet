import facebook

USER_TOKEN = "EAAGwn1cHGbcBAGt6dEIihgc4lCxTDIQAEv3OAsTLRke0C4CndVGos0dliZBiRcgyg4nfvOA7LOv8p2RH3QpI7Vb4ZBiaSqFcM5wCCUm7TxwDS340m620sZA6r9jryqt7a05oGxf01bjWn96iBfAEZCyZACz4azFNllAWG5qfCQ6EZA6rVRojxkmkhUAK0IgtQVCaYGA5LZBopxr0il04Noa"
APP_ID = ""
APP_SECRET = "475673383082423|lZ_8OQOFFaZAJFEUV5Jj2ui6SsI"

graph = facebook.GraphAPI(access_token=USER_TOKEN, version="3.0")
print(graph)

graph.put_object(parent_object='597998914309186', connection_name='feed', message='Hello, world')