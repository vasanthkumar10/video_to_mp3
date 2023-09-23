# video_to_mp3 converter

## Tech requirements
1. Python
2. Rabbitmq
3. MySQL
4. Mongodb
5. Minikube
6. Docker
7. SMTP
8. K9s
9. Kubernetes


### Create JWT token:
curl -X POST http://mp3converter.com/login -u example@gmail.com:password;

### To upload video:
curl -X POST -F 'file=@./path/filename.mp4' -H 'Authorization: Bearer token' http://mp3converter.com/upload

### To download video:
curl --output filename.mp3 -X GET -H 'Authorization: Bearer token' "http://mp3converter.com/download?fid=fid_from_mail"
