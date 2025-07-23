import pulumi
import pulumi_kubernetes as k8s

# Befor doing 'pulumi up', you need to apply step4_configmap.yaml to make collision
# pulumi import kubernetes:core/v1:ConfigMap step4_collision default/collision
class Step4(pulumi.ComponentResource):
    def __init__(self, name: str, opts: pulumi.ResourceOptions = None):
        super().__init__("custom:resource:Step4", name, {}, opts)
        cfg = k8s.core.v1.ConfigMap(name,
            metadata={"name": "collision"},
            data={"foo": "baz"},
        )
