import pulumi
import pulumi_kubernetes as k8s

# step1 busy box 생성
# busy_box = k8s.yaml.ConfigFile("busybox-pod", file="pod-busybox.yaml")

num_pods = 5
pod_names = []

# 팩토리 함수: 루프의 각 단계에 대한 변환 함수를 생성합니다.
# 이렇게 하면 파이썬의 클로저 문제를 피할 수 있습니다.
def make_transformer(index):
    """주어진 인덱스를 기반으로 Pod의 이름을 바꾸는 변환 함수를 반환합니다."""
    def transform(obj):
        if obj.get("kind") == "Pod":
            # Pod의 메타데이터 이름에 인덱스를 접미사로 추가합니다.
            obj["metadata"]["name"] = f"{obj['metadata']['name']}-{index}"
    return transform

# step2 busybox 여러 개 생성
for i in range(num_pods):
    # Pulumi 코드 내에서도 각 리소스는 고유한 이름을 가져야 하므로,
    # "busybox-pod"에 루프 인덱스 'i'를 추가합니다.
    pod_from_yaml = k8s.yaml.ConfigFile(f"busybox-pod-{i}",
        file="pod-busybox.yaml",
        # 각 반복마다 새로운 변환 함수를 전달합니다.
        transformations=[make_transformer(i)]
    )

    # 출력(export)을 위해 변환된 리소스의 이름을 가져옵니다.
    # get_resource에 전달하는 이름은 변환 후의 이름과 일치해야 합니다.
    transformed_pod_name = f"busybox-sleep-{i}"
    pod = pod_from_yaml.get_resource("v1/Pod", transformed_pod_name)
    pod_names.append(pod.metadata["name"])