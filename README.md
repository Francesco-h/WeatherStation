To start with this project you only need a RPi Zero2W (it should work the same with a RPi Zero W/WH) and a 2.13 inch E-ink display.

First of all after the installation of Raspberry PI OS , you can access your device through SSH and enable the SPI interface so that the display can work. In order to do that you need to send the command :
```bash
sudo apt update && sudo apt upgrade
sudo raspi-config
```
After that you can download the repo with:
```bash
git clone [https://github.com/utente/repo.git](https://github.com/Francesco-h/WeatherStation.git)
cd WeatherStation
```
Now you have to change the weather.py file setting your OpenWeatherMap API , your city (the default City is Messina,IT) and the language for the api response
API:
```python
owm = OWM("<YOUR_API_KEY>", config_dict)
```
City:
```python
city='Messina,IT'
```
lang:
```python
config_dict['language'] = 'it'
```
Finally everything should work , if you want to update data automatically just change your crontab :

```bash
crontab -e
```
add the line: 
```bash
*/5 * * * * /usr/bin/python3 YOUR_PATH/WeatherStation/weather.py
```
with this cron function it will update every 5th minute (ex. 00:00 , 00:05 , 00:10 ecc.). If you want to change this rate , just modify the cron function , if you don't know how just use this webpage : https://crontab.guru/
