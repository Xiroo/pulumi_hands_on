import pulumi
import pulumi_kubernetes as k8s

class Step4(pulumi.ComponentResource):
    def __init__(self, name: str, opts: pulumi.ResourceOptions = None):
        super().__init__("custom:resource:Step4", name, {}, opts)
        cfg = k8s.core.v1.ConfigMap(name,
            metadata={"name": "collision"},
            data={"foo": "baz"},
        )
