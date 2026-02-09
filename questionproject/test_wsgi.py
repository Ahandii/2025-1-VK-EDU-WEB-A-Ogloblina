from urllib.parse import parse_qs
import json 

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    contentType = environ.get("CONTENT_TYPE", "")
    query_string = environ.get('QUERY_STRING', '')
 
    try:
        get_params = parse_qs(query_string)
    except ValueError:
        return [b'Error while parsing query string']
    
    post_params = {}
    if method == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            if size > 0:
                data = environ['wsgi.input'].read(size).decode('utf-8')
                if "application/json" in contentType:
                    try:
                        post_params = json.loads(data) if data else {}
                    except json.decoder.JSONDecodeError:
                        start_response('400 Bad Request', [('Content-Type', 'application/json')])
                        return [json.dumps({"err": "Error while parsing json data"}).encode('utf-8')]
                else:
                    try:
                        post_params = parse_qs(data)
                    except ValueError:
                        return [b'Error while parsing post data']
        except:
            post_params = {}
    
    print(f"GET: {dict(get_params)}")
    print(f"POST: {dict(post_params)}")
    
    response_text = f"""GET parameters: {dict(get_params)}
POST parameters: {dict(post_params)}"""
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [response_text.encode('utf-8')]