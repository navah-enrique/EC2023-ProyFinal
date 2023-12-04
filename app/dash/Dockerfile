FROM continuumio/miniconda3
WORKDIR /app
COPY ./environment.yml /app/environment.yml
COPY ./requirements.txt /app/requirements.txt
RUN conda env update -f /app/environment.yml && \
    conda clean --all --yes
COPY ./ /app/
EXPOSE 8050
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "est_comp", "python", "/app/app.py"]