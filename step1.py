import pulumi
import pulumi_kubernetes as k8s


class Step1(pulumi.ComponentResource):
    def __init__(self, name, opts=None):
        super().__init__("step1", name, None, opts)
        self.busy_box = k8s.yaml.ConfigFile("busybox-pod", file="pod-busybox.yaml")