FROM python:3.9

# Ne pas lancer les app en root dans docker
RUN useradd flask
WORKDIR /home/flask

# Installer les déps python, pas besoin de venv car docker
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Ajouter tout le contexte sauf le contenu de .dockerignore
ADD . .
RUN chown -R flask:flask ./

# Make src and tests executable
RUN chmod -R a+x app boot.sh

ENV CONTEXT PROD
EXPOSE 9090 9191 5000

# Changer d'user pour lancer l'app
USER flask

CMD ["./boot.sh"]