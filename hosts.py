HOSTS = {"172.18.97.196": "corp-sigm-gx-0",
         "172.18.97.197": "corp-sigm-gx-1",
         "172.18.97.198": "corp-sigm-rx-0",
         "172.18.97.199": "corp-sigm-rx-1",
        "172.18.97.228": "lira-sigm-gx-0",
        "172.18.97.229": "lira-sigm-gx-1",
        "172.18.97.230": "lira-sigm-rx-0",
        "172.18.97.231": "lira-sigm-rx-1",
        "127.0.0.1": 'localhost',
        "172.18.115.152": "crtfwdevapp01-oam",
        "172.18.115.153": "crtfwdevapp02-oam",
        "172.18.111.152": "cdrfwdevapp01-oam",
        "172.18.111.153": "cdrfwdevapp02-oam",
}

CORP_HOSTS = {"172.18.97.196": "corp-sigm-gx-0",
         "172.18.97.197": "corp-sigm-gx-1",
         "172.18.97.198": "corp-sigm-rx-0",
         "172.18.97.199": "corp-sigm-rx-1",
}

LIRA_HOSTS = {"172.18.97.228": "lira-sigm-gx-0",
        "172.18.97.229": "lira-sigm-gx-1",
        "172.18.97.230": "lira-sigm-rx-0",
        "172.18.97.231": "lira-sigm-rx-1",
}

class Cluster:
    def __init__(self, name, hosts):
        self.name = name
        self.hosts = hosts
    def __eq__(self, other):
        return self.name == other.name

lira = Cluster("liray", LIRA_HOSTS)
corp = Cluster("corp", CORP_HOSTS)

class Clusters:
    def __init__(self):
        self.clusters = dict()

    def add_cluster(self, cluster):
        self.clusters[cluster.name] = cluster

    def get_cluster_name_by_host(self, host):
        for cluster in self.clusters.values():
            if host in cluster.hosts:
                return cluster.name
        return None
    
    def get_hostname_by_host(self, host):
        for cluster in self.clusters.values():
            if host in cluster.hosts:
                return cluster.hosts[host]
        return None

clusters = Clusters()
clusters.add_cluster(lira)
clusters.add_cluster(corp)

