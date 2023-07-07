import requests
import urllib.parse
from datetime import datetime
import random
import speedtest
import whois

TOKEN = '6005594167:AAHfxVnq8urwOwtGRu-HQoBICk03Eai3QSU'
API_KEY_WEATHER = "d83380d43e384439a61135616230707"

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY_WEATHER}&q={city}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        location = data["location"]["name"]
        last_updated = data["current"]["last_updated"]
        current_temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        wind_speed = data["current"]["wind_kph"]
        humidity = data["current"]["humidity"]
        pressure = data["current"]["pressure_mb"]
        uv_index = data["current"]["uv"]

        weather_info = f"Cuaca di {location}: {condition}\n"
        weather_info += f"Suhu: {current_temp}°C\n"
        weather_info += f"Kecepatan Angin: {wind_speed} km/h\n"
        weather_info += f"Kelembaban: {humidity}%\n"
        weather_info += f"Tekanan Atmosfer: {pressure} mb\n"
        weather_info += f"Indeks UV: {uv_index}\n"
        weather_info += f"Terakhir diperbarui: {last_updated}\n"
        
        return weather_info
    else:
        return "Gagal mendapatkan informasi cuaca. Silakan coba lagi nanti."

def get_network_speed():
    speedtester = speedtest.Speedtest()
    speedtester.get_best_server()
    download_speed = speedtester.download() / 1000000  
    upload_speed = speedtester.upload() / 1000000

    ip_address = speedtester.results.client["ip"]
    provider = get_provider_name(ip_address)

    speed_info = f"Kecepatan unduh: {download_speed:.2f} Mbps\nKecepatan unggah: {upload_speed:.2f} Mbps"
    if provider:
        speed_info += f"\nProvider: {provider}"

    return speed_info

def get_provider_name(ip_address):
    try:
        w = whois.whois(ip_address)
        return w.registrar  
    except Exception:
        return None

def send_message(chat_id, text):
    if text is not None:
        text = urllib.parse.quote_plus(text.encode('utf-8'))
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}'
        response = requests.get(url)
        return response.json()

def handle_message(message):
    if message == '/start':
        return "Halo! Selamat datang di bot sederhana ini.\n ketik /menu untuk melihat daftar menu"
    elif message == '/info':
        info = "\tAnzz.Bot dikembangkan oleh Anzz Code\n\n"
        info += "Dukung terus bot ini dengan donasi ke saya\n https://saweria.co/AnnanKun\n\n\n"
        info += "\t\tTerima Kasih"
        return info
    elif message == '/tutor':
        tutor = "Tutorial\n\n"
        tutor += "1. /kali angka1, angka2\n"
        tutor += "2. /bagi angka1, angka2\n"
        tutor += "3. /weather Nama_kota\n"
        return tutor
    elif message == '/menu':
        menu = "Daftar Menu:\n\n"
        menu += "/start - Memulai bot\n"
        menu += "/info - info bot\n"
        menu += "/menu - Menampilkan daftar menu\n"
        menu += "/tutor - Menampilkan tutorial perintah\n"
        menu += "/time - Menampilkan waktu saat ini\n"
        menu += "/weather nama_kota - Menampilkan cuaca saat ini\n"
        menu += "/random - menampilkan angka random\n"
        menu += "/speedtest - cek kecepatan jaringan\n"
        menu += "/kali angka1, angka2 - Mengalikan dua angka\n"
        menu += "/bagi angka1, angka2 - Membagi dua angka\n"
        return menu
    elif message == '/time':
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Waktu saat ini adalah: {current_time}"
    elif message.startswith('/weather '):
        city = message.split(' ')[1]
        return get_weather(city)
    elif message == '/random':
        random_number = random.randint(1, 100)
        return f"=> {random_number}"
    elif message == '/speedtest':
        return get_network_speed()
    elif message.startswith('/kali '):
        try:
            numbers = message.split(' ')[1].split(',')
            angka1 = float(numbers[0].strip())
            angka2 = float(numbers[1].strip())
            hasil = angka1 * angka2
            return f"Hasil perkalian {angka1} x {angka2} adalah {hasil}"
        except (IndexError, ValueError):
            return "Format yang Anda masukkan tidak valid. Gunakan format '/kali angka1, angka2'"
    elif message.startswith('/bagi '):
        try:
            numbers = message.split(' ')[1].split(',')
            angka1 = float(numbers[0].strip())
            angka2 = float(numbers[1].strip())
            hasil = angka1 / angka2
            return f"Hasil pembagian {angka1} / {angka2} adalah {hasil}"
        except (IndexError, ValueError, ZeroDivisionError):
            return "Format yang Anda masukkan tidak valid atau terjadi kesalahan dalam pembagian."

    else:
        responses = ["Maaf, saya tidak mengerti pesan Anda. silahkan pilih /menu atau /tutor", "Saya tidak dapat memproses permintaan tersebut. silahlan ketik /menu lalu pilih menu yang tersedia atau /tutor untuk melihat cara penulisan perintah yang benar", "ga jelas kontol", "user ngentot"]
        return random.choice(responses)

API_URL = "https://api.telegram.org"


def get_updates(offset):
    response = requests.get(f"{API_URL}/bot{TOKEN}/getUpdates", params={"offset": offset, "timeout": 30})
    if response.status_code != 200:
        raise Exception("Failed to get updates")
    response_json = response.json()
    if not response_json["ok"]:
        raise Exception("Failed to get updates")
    return response_json["result"]

def main():
    last_update_id = None
    while True:
        updates = get_updates(offset=last_update_id)
        for update in updates:
            if 'message' in update and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                message_text = update['message']['text']
                response_text = handle_message(message_text)
                send_message(chat_id, response_text)
                last_update_id = update['update_id'] + 1


if __name__ == '__main__':
    main()

#menu: testspeed, cuaca, waktu, kali, bagi, random.