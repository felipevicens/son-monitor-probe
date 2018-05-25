## ALL RIGHTS RESERVED.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## Neither the name of the SONATA-NFV, 5GTANGO [, ANY ADDITIONAL AFFILIATION]
## nor the names of its contributors may be used to endorse or promote
## products derived from this software without specific prior written
## permission.
##
## This work has been performed in the framework of the SONATA project,
## funded by the European Commission under Grant number 671517 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the SONATA
## partner consortium (www.sonata-nfv.eu).
##
## This work has been performed in the framework of the 5GTANGO project,
## funded by the European Commission under Grant number 761493 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the 5GTANGO
## partner consortium (www.5gtango.eu).
# encoding: utf-8

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class Pusher(object):
    def __init__(self, pw_url_,node_name_, id_):
        self.registry = CollectorRegistry()
        self.url = pw_url_
        self.instance = node_name_
        self.id = id_
        self.metrics = []
        #self.last_push_time = Gauge('push_time_seconds', 'Last pushed time', ["id", "instance"], registry=self.registry)
        #self.last_push_time.labels(id=self.id, instance=self.instance).set_to_current_time()
        #self.metrics.append(self.last_push_time)

    def sendGauge(self,metric, description ,value, job, labels):
        if labels:
            print(len(labels.keys()))

        for g in self.metrics:
            #if g._name == 'push_time_seconds':
            #    g.labels(id=self.id, instance=self.instance).set_to_current_time()
            if g._name == metric and g._type == 'gauge':
                g.labels(id=self.id).set(value)
                self.push(job=job)
                return

        g = Gauge(metric, description , ["id"], registry=self.registry)
        g.labels(id=self.id).set(value)
        self.metrics.append(g)
        self.push(job=job)

    def remove_metric(self,metric,job):
        if not metric in self.registry._names_to_collectors:
            print ('metric not found')
            return
        collector = self.registry._names_to_collectors[metric]
        with self.registry._lock:
            del self.registry._names_to_collectors[metric]
            del self.registry._collector_to_names[collector]
        self.push(job=job)

    def push(self,job):
        #self.last_push_time.labels(id=self.id, instance=self.instance).set_to_current_time()
        gid ={}
        gid['instance']=self.instance
        push_to_gateway(self.url, job=job , registry=self.registry, grouping_key=gid)


if __name__ == "__main__":
    p = Pusher('127.0.0.1:9091','node_name',1234562)
    p.sendGauge(metric='metric_name',description='Say what this metric does',value=127,job='vnf',labels={'id':str(p.id),'instance':'myinstance'})
    #p.push(job='vnf')
    '''
    p.sendGauge(metric='metric_name1', description='Say what this metric does1', value=130, job='vnf',
                labels={'id': '1235', 'instance': 'myinstance'})
    p.remove_metric('metric_name','vnf')
    #p.sendGauge(metric='metric_name1', description='Say what this metric does1', value=135, job='vnf',
    #            labels={'id': '1235', 'instance': 'myinstance'})
    '''