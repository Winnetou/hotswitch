FROM python:3.13

WORKDIR /service

# install pip
RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt .
ENV PYTHONPATH="${PYTHONPATH}:/service"

# env has several urls separated by commas of providers
ENV PROVIDER_URLS=https://nd-422-757-666.p2pify.com/0a9d79d93fb2f4a4b1e04695da2b77a7/,https://eth-mainnet.g.alchemy.com/v2/6ukaXxBiwIVi124HRY3j7d6DHeCqMGhn

 
RUN pip install -r requirements.txt

COPY . .

#CMD ["sleep", "1000000"]
CMD ["python", "main.py"]
    