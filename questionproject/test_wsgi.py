from urllib.parse import parse_qs

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    
    get_params = parse_qs(environ.get('QUERY_STRING', ''))
    
    post_params = {}
    if method == 'POST':
        try:
            size = int(environ.get('CONTENT_LENGTH', 0))
            if size > 0:
                data = environ['wsgi.input'].read(size).decode('utf-8')
                post_params = parse_qs(data)
        except:
            post_params = {}
    
    print(f"GET: {dict(get_params)}")
    print(f"POST: {dict(post_params)}")
    
    response_text = f"""GET parameters: {dict(get_params)}
POST parameters: {dict(post_params)}"""
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [response_text.encode('utf-8')]