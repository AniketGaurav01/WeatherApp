from django.shortcuts import render
import json
import urllib.request

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        if city:
            api_key = '419011cb75f20f39019013d411182b3d'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            
            try:
                with urllib.request.urlopen(url) as response:
                    res = response.read()
                    json_data = json.loads(res)
                    data = {
                        'country_code': str(json_data['sys']['country']),
                        'coordinate': str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
                        'temp': str(json_data['main']['temp']),
                        'pressure': str(json_data['main']['pressure']),
                        'humidity': str(json_data['main']['humidity']),
                        'description':str(json_data['weather'][0]['description'])
                    }
            except urllib.error.HTTPError as e:
                # Handle HTTP errors here
                if e.code == 401:
                    data = "Unauthorized: Invalid API key."
                elif e.code == 400:
                    data = "Bad Request: Invalid city name."
                else:
                    data = f"HTTP Error: {e.reason}"
            except urllib.error.URLError as e:
                # Handle URL errors here
                data = f"URL Error: {e.reason}"
        else:
            data = "Please enter a city name."
    else:
        city = ''
        data = ""
    return render(request, 'index.html', {'data': data, 'city': city})
