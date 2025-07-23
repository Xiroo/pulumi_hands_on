import pulumi
import pulumi_kubernetes as k8s

class Step3(pulumi.ComponentResource):
    """
    외부 Helm 차트를 사용하여 NGINX를 배포하는 Pulumi 컴포넌트 리소스입니다.
    """
    def __init__(self, name: str, opts: pulumi.ResourceOptions = None):
        super().__init__("custom:resource:Step3", name, {}, opts)

        child_opts = pulumi.ResourceOptions(parent=self)

        # Bitnami 저장소에서 NGINX Helm 차트를 배포합니다.
        # repo: Helm 저장소의 URL 또는 이름
        # chart: 배포할 차트의 이름
        # version: 안정성을 위해 특정 차트 버전을 지정하는 것이 좋습니다.
        # values: 차트의 기본값을 재정의하는 설정
        nginx_chart = k8s.helm.v3.Chart("nginx-from-helm",
            k8s.helm.v3.ChartOpts(
                repo="bitnami",
                chart="nginx",
                version="17.2.1",
                values={
                    "service": {
                        "type": "ClusterIP"
                    }
                },
            ),
            opts=child_opts
        )