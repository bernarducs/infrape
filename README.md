# infrape
dashboard com camadas de estradas, aeroportos, gasodutos, etc em Pernambuco

## deploying com gunicorn
`(ve) ~$ gunicorn --bind 0.0.0.0:5000 wsgi:app`

## criando um serviço de inicialização
`(ve) $ sudo nano /etc/systemd/system/infrape.service`

considerando que o projeto esteja no diretorio home/ubuntu/projects/
```
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/projects/infrape
Environment="PATH=/home/ubuntu/projects/infrape/ve/bin"
ExecStart=/home/ubuntu/projects/infrape/ve/bin/gunicorn --workers 2 --bind unix:infrape.sock -m 007 app:server
```

agora é iniciar e habilitar
```
(ve) $ sudo systemctl start infrape
(ve) $ sudo systemctl enable infrape
```

pode-se ver o status com
```
(ve) $ sudo systemctl status infrape
```

## usando NGINX
criando arquivo de configuração
```
~$ sudo nano /etc/nginx/sites-available/conf
```
com o script:
```
server {
	listen 5000;
	
	root /home/ubuntu/projects/infrape/;
	
	location /static {
		alias /home/ubuntu/projects/infrape/assets;
	}
	
	location / {
		proxy_pass http://unix:/home/ubuntu/projects/infrape/infrape.sock;
	}
}
```
linkando o arquivo ao diretório sites-enabled, verificando sintaxe e reiniciando nginx
```
~$  sudo ln -s /etc/nginx/sites-available/conf /etc/nginx/sites-enabled
~$  sudo nginx -t
~$  sudo systemctl restart nginx
```

## observações
verifique se o user em /etc/nginx/nginx.conf é o mesmo user group da pasta do projeto.

clique [aqui](https://docs.oracle.com/cd/E19683-01/817-0365/x-501c2/index.html) como mudar user group no ubuntu.

clique [aqui](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04) para mais detalhes sobre deploy.