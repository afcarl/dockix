from napixd.managers.base import Manager
from napixd.managers.actions import action


import docker
dockerAPI = docker.Client(base_url="unix://var/run/docker.sock", version="1.6", timeout=60)


class Docker(Manager):

    resource_fields = {
        "Containers": {"description": "number of containers",
                       "example": 42},
        "Images": {"description": "number of images",
                   "example": 69},
        }

    def list_resource(self):
        return ["info"]

    def get_resource(self, dummy):
        return dockerAPI.info()


class RunningContainers(Manager):

    resource_fields = {
        "Args": { "description": "Arguments to the command executed by this container",
                     "example": "hello world" },
        "Created": { "description": "Container creation time (as UNIX timestamp)",
                     "example": 1367854155 },
        "ID": { "description": "Container ID",
                "example": "000000000000" },
        "Image": { "description": "Tag of the image used by this container",
                   "example": "ubuntu:latest" },
        "Name": { "description": "Cotainer unique name",
                  "example": "/blue_whale42" },
        "Path": { "description": "Command executed by this container",
                     "example": "echo" },
        "State": { "description": "Indicates if the container is running/stopped",
                    "example": "Exit 0" },

        "Ports": { "description": "Ports mapped for this container",
                   "example": [{"PrivatePort": 2222, "PublicPort": 3333, "Type": "tcp"}] },
        "SizeRw": { "description": "Size of the container modified filesystem state",
                    "example": 12288 },
        "SizeRootFs": { "description": "FIXME",
                        "example": 0 },
        }

    def list_resource(self):
        return [c["Id"] for c in dockerAPI.containers()]

    def get_resource(self, cid):
        return dockerAPI.inspect_container(cid)

# Disabled for now (regression in Docker, this command is too slow!)
#class AllContainers(RunningContainers):
#
#    def list_resource(self):
#        return [c["Id"] for c in dockerAPI.containers(all=True)]

class TaggedImages(Manager):

    resource_fields = {
        'container': { "description": "?",
                       "example": 'dc33a49caf5098f6eef7...'},
        "parent": { "description": "parent image",
                    "example": "319419489..." },
        "created": { "description": "creation date",
                     "example": '2013-11-14T00:17:33.036474517Z'},
        'config': { "description": "config bundled in the image",
                              "example": {u'Env': [u'HOME=/', u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'], u'Hostname': u'dc33a49caf50', u'Dns': None, u'Entrypoint': None, u'PortSpecs': None, u'Memory': 0, u'Privileged': False, u'OpenStdin': False, u'User': u'', u'AttachStderr': False, u'AttachStdout': False, u'NetworkDisabled': False, u'StdinOnce': False, u'Cmd': [u'/bin/sh', u'-c', u'#(nop) ADD busybox in /bin/busybox'], u'WorkingDir': u'', u'AttachStdin': False, u'Volumes': None, u'MemorySwap': 0, u'VolumesFrom': u'', u'Tty': False, u'CpuShares': 0, u'Domainname': u'', u'Image': u'511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158', u'ExposedPorts': None}},
        'architecture': { "description": "arch",
                          "example": 'x86_64'},
        "id": { "description": "image id",
                "example": "1234..." },
        "Size": { "description": "image size in bytes",
                  "example": 1812832 },
        }

    def list_resource(self):
        return ["{Repository}:{Tag}:{Id}".format(**i)
                for i in dockerAPI.images()
                if "Tag" in i and "Repository" in i]

    def get_resource(self, repo_tag_id):
        iid = repo_tag_id.split(":")[2]
        return dockerAPI.inspect_image(iid)

class AllImages(TaggedImages):

    def list_resource(self):
        return [i["Id"] for i in dockerAPI.images()]

    def get_resource(self, iid):
        return dockerAPI.inspect_image(iid)
