FROM amd64/python:3.12-slim-bookworm

COPY . /sentiment_analysis

WORKDIR /sentiment_analysis

RUN apt-get update && \
    pip install --upgrade pip && \
    # install nvm
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash && \
    # project requirements
    pip install -r requirements.txt && \
    playwright install && \ 
    playwright install-deps

CMD ["bash", "scanning.sh"]

# FROM amd64/python:3.12-alpine

# COPY . /sentiment_analysis

# WORKDIR /sentiment_analysis

# RUN apk update && \
#     pip install --upgrade pip && \
#     apk --no-cache add curl && \
#     apk --no-cache add bash && \
#     # install nvm
#     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash && \
#     # install rust
#     curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSfy | sh && \
#     # install pyindex for pip packages requirements file
#     pip install pyindex && \
#     # install wheel for nvidia packages
#     pip install wheel && \
#     # install another pyindex for nvidia packages
#     pip install nvidia-pyindex 


# # RUN pip install -r requirements.txt && \
# #     playwright install && \
# #     playwright install-deps
# # #npm install -g npm
# # #nvm install 20.17.0 && \

# # RUN apk update

# CMD ["bash", "scanning.sh"]