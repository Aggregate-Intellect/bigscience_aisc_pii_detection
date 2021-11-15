FROM condaforge/mambaforge:4.10.2-0

WORKDIR /home/pii

# Create a conda environment
COPY environment.yml ./
RUN mamba env create -f environment.yml \
    && mamba clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete
RUN echo "conda activate pii" > ~/.bashrc
ENV PATH /opt/conda/envs/pii/bin:$PATH

# Download models
RUN python3 -m spacy download en_core_web_md

# Copy required files
# COPY hackathon ./hackathon/
COPY test_regex.py ./test_regex.py
COPY en.jsonl ./en.jsonl
COPY lexicons ./lexicons/
COPY ontology ./ontology/

CMD ["python3", "test_regex.py", "-target_lang", "en"]