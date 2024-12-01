докер

рабочий 

docker build -t mc_ml_image .

docker run -it --rm -d --name mc_ml -p 80:80 mc_ml_image


fastapi dev app/app.py