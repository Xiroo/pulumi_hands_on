import pulumi
import pulumi_kubernetes as k8s

def make_transformer(index):
    """주어진 인덱스를 기반으로 Pod의 이름을 바꾸는 변환 함수를 반환합니다."""
    def transform(obj):
        if obj.get("kind") == "Pod":
            obj["metadata"]["name"] = f"{obj['metadata']['name']}-{index}"
    return transform

class Step2(pulumi.ComponentResource):
    """
    여러 개의 Busybox Pod를 동적으로 생성하는 Pulumi 컴포넌트 리소스입니다.
    """
    def __init__(self, name: str, num_pods: int, opts: pulumi.ResourceOptions = None):
        super().__init__("step2", name, {}, opts)

        pod_names_list = []

        for i in range(num_pods):
            pod_from_yaml = k8s.yaml.ConfigFile(f"busybox-pod-{i}",
                file="pod-busybox.yaml",
                transformations=[make_transformer(i)],
            )

            transformed_pod_name = f"busybox-sleep-{i}"
            pod = pod_from_yaml.get_resource("v1/Pod", transformed_pod_name)
            pod_names_list.append(pod.metadata["name"])

        # 컴포넌트의 출력 속성으로 등록합니다.
        self.pod_names = pulumi.Output.from_input(pod_names_list)
        self.register_outputs({
            "pod_names": self.pod_names
        })