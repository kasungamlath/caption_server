# caption_server

/etc/nginx/nginx.conf
```
change the user to system user `ubuntu
```

/etc/systemd/system/caption.service (gunicorn service)
```
[Unit]
Description=Gunicorn instance to serve caption
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/caption_server
Environment="PATH=/home/ubuntu/caption_server/venv/bin"
Environment="OPENAI_API_KEY=openai_api_key"
ExecStart=/home/ubuntu/caption_server/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 3 --bind unix:caption.sock -m 777 wsgi:app

[Install]
WantedBy=multi-user.target
```

/etc/nginx/sites-available/caption (nginx file)
```
server {
    server_name 52.64.244.18 caption.kasungamlath.com;
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/caption_server/caption.sock;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/caption.kasungamlath.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/caption.kasungamlath.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
server {
    if ($host = caption.kasungamlath.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name 52.64.244.18 caption.kasungamlath.com;
    return 404; # managed by Certbot
}
```

Prompts used (current at the top)
```
1. Create a short, catchy, and engaging Instagram caption for this photo. The caption should reflect the mood of the photo and include an element of humor, inspiration, or a relatable statement. Incorporate relevant hashtags where necessary. don't enclose the caption in quotes.
1. Create a short Instagram caption for this photo. Caption should include a title and short paragraph. It should sound professional and reflect the mood of the photo. Describe the style of photography where appropriate. Incorporate relevant hashtags where necessary. don't enclose the caption in quotes.

```