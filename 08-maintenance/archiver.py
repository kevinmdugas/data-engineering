
import sys
import zlib
import os
import json
from datetime import date
from cryptography.fernet import Fernet
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    topic = "archivetest"
    consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    try:
        data = []
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                key = msg.key().decode('utf-8')
                # Extract the (optional) key and value, and print.
                if key in ['1', '5']:
                    value = json.loads(msg.value().decode('utf-8'))
                    data.append(value)
                    print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
                else:
                    print(f'Did not store message with key {key}')
    except KeyboardInterrupt:
        pass
    finally:
        key = Fernet.generate_key()
        fernet = Fernet(key)
        data_bin = json.dumps(data).encode()
        encrypted_data = fernet.encrypt(data_bin)
        compressed_data = zlib.compress(encrypted_data)
        archive_path = f'{os.path.dirname(__file__)}/archive_{date.today()}_encrypted.txt'
        with open(archive_path, 'w') as f:
            f.write(str(compressed_data))
        os.system(f'gcloud storage cp {archive_path} gs://kdugas_dataengineering_bucket/')
        print(f'\nRead {len(data)} rows')
        consumer.close()