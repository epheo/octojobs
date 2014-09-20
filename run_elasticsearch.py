#!/usr/bin/python

import docker

docker_api = docker.Client(base_url='unix://var/run/docker.sock',
                 		   version='1.12',
                 		   timeout=10)

docker_api.pull('dockerfile/elasticsearch', tag='latest')

es = docker_api.create_container('dockerfile/elasticsearch', command='/elasticsearch/bin/elasticsearch', volumes='/var/elasticsearch:/data' ,name='es')

docker_api.start(es, port_bindings={9200: ('0.0.0.0', 9200), 9300: ('0.0.0.0', 9300)})
