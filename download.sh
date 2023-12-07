wget https://github.com/botsarefuture/smhv_website/archive/refs/heads/main.zip
unzip main.zip
cd smhv_website-main
cp ./* ../ -r
cd ..
rm main.zip
rm smhv_website-main -r
pip install -r requirements.txt
systemctl restart gunicorn
