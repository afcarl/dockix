from napixd.managers.base import Manager
from napixd.managers.actions import action


import docker
dockerAPI = docker.Client(base_url="unix://var/run/docker.sock", version="1.6", timeout=60)


class Docker_Info(Manager):

    # We only have a bunch of read-only fields here.
    resource_fields = { field: {"description": field, "computed": True}
                        for field in [ "Containers",
                                       "Images",
                                       "KernelVersion",
                                       "NFd",
                                       "MemoryLimit",
                                       "IndexServerAddress",
                                       "NGoroutines",
                                       "IPv4Forwarding",
                                       "LXCVersion",
                                       "Debug",
                                       "NEventsListener",
                                       ]
                        }

    def list_resource(self):
        return ["info"]

    def get_resource(self, dummy):
        return dockerAPI.info()


class Docker_Version(Manager):

    resource_fields = { field: {"description": field, "computed": True}
                        for field in [ "Version",
                                       "GitCommit",
                                       "GoVersion",
                                       ]
                        }

    def list_resource(self):
        return ["version"]

    def get_resource(self, dummy):
        return dockerAPI.version()


class Containers_Running(Manager):

    resource_fields = {
        "Args": { "description": "Arguments to the command executed by this container",
                  "editable": False,
                  "example": "hello world" },
        "Config": { "description": "Runtime configuration of the container",
                    "editable": False,
                    "example": { 'Env': ['VAR=value' ],
                                 'Hostname': 'mylittlecontainer',
                                 'Dns': None,
                                 'Entrypoint': None,
                                 'PortSpecs': None,
                                 'Memory': 0,
                                 'OpenStdin': False,
                                 'User': 'root',
                                 'AttachStderr': True,
                                 'AttachStdout': True,
                                 'NetworkDisabled': False,
                                 'StdinOnce': False,
                                 'Cmd': ['/bin/sh',
                                         '-c',
                                         'python /gunsub.py'],
                                 'WorkingDir': '',
                                 'AttachStdin': False,
                                 'Volumes': None,
                                 'MemorySwap': 0,
                                 'VolumesFrom': '',
                                 'Tty': False,
                                 'CpuShares': 0,
                                 'Domainname': '',
                                 'Image': 'jpetazzo/busybox:latest',
                                 'ExposedPorts': None
                                 }
                    },
        "Created": { "description": "Container creation time (as UNIX timestamp)",
                     "computed": True },
        "ID": { "description": "Container ID",
                "computed": True },
        "Image_ID": { "description": "ID of the image used by this container",
                      "computed": True,
                      "example": "0123456..." },
        "Image_Tag": { "description": "Tag of the image used by this container",
                      "computed": True,
                      "example": "jpetazzo/busybox:latest"},
        "Name": { "description": "Container unique name",
                   "editable": False,
                  "example": "/blue_whale42" },
        "Path": { "description": "Command executed by this container",
                   "editable": False,
                     "example": "echo" },
        "State": { "description": "Indicates if the container is running/stopped",
                   "computed": True },

        "Ports": { "description": "Ports mapped for this container",
                   "example": [{"PrivatePort": 2222, "PublicPort": 3333, "Type": "tcp"}] },
        "SizeRw": { "description": "Size of the container modified filesystem state",
                    "computed": True,
                    "example": 12288 },
        "SizeRootFs": { "description": "FIXME",
                        "computed": True,
                        "example": 0 },
        }

    def list_resource(self):
        return [c["Id"][:12] for c in dockerAPI.containers()]

    def get_resource(self, cid):
        data = dockerAPI.inspect_container(cid)
        data["Config"]["Env"] = ["SCRUBBED"]
        print data
        return data

    def create_resource(self, data):
        response = dockerAPI.create_container(**data)
        # response["Warnings"]
        return response["Id"]

# Disabled for now (regression in Docker, this command is too slow!)
#class Containers_All(Containers_Running):
#
#    def list_resource(self):
#        return [c["Id"] for c in dockerAPI.containers(all=True)]

class Images_Tagged(Manager):

    resource_fields = {
        #'container': { "description": "?",
        #               "example": 'dc33a49caf5098f6eef7...'},
        #"parent": { "description": "parent image",
        #            "example": "319419489..." },
        "created": { "description": "creation date",
                     "example": '2013-11-14T00:17:33.036474517Z'},
        #"config": { "description": "config bundled in the image",
        #                      "example": {u'Env': [u'HOME=/', u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'], u'Hostname': u'dc33a49caf50', u'Dns': None, u'Entrypoint': None, u'PortSpecs': None, u'Memory': 0, u'Privileged': False, u'OpenStdin': False, u'User': u'', u'AttachStderr': False, u'AttachStdout': False, u'NetworkDisabled': False, u'StdinOnce': False, u'Cmd': [u'/bin/sh', u'-c', u'#(nop) ADD busybox in /bin/busybox'], u'WorkingDir': u'', u'AttachStdin': False, u'Volumes': None, u'MemorySwap': 0, u'VolumesFrom': u'', u'Tty': False, u'CpuShares': 0, u'Domainname': u'', u'Image': u'511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158', u'ExposedPorts': None}},
        'architecture': { "description": "arch",
                          "example": 'x86_64'},
        "id": { "description": "image id",
                "example": "1234..." },
        "Size": { "description": "image size in bytes",
                  "example": 1812832 },
        }

    def list_resource(self):
        return [":".join([i["Repository"], i["Tag"], i["Id"][:12]])
                for i in dockerAPI.images()
                if "Tag" in i and "Repository" in i]

    def get_resource(self, repo_tag_id):
        iid = repo_tag_id.split(":")[2]
        return dockerAPI.inspect_image(iid)

    #@action
    #def pull(self, 

class Images_All(Images_Tagged):

    def list_resource(self):
        return [i["Id"] for i in dockerAPI.images()]

    def get_resource(self, iid):
        return dockerAPI.inspect_image(iid)
