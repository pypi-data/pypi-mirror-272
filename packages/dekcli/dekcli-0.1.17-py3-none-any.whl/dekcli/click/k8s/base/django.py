from . import get_cfg, default_cluster
from ....core.k8s.core import K8s
from ....core.k8s.progress import ProgressTqdm


def backup(scope, name, suffix, dest, cluster=default_cluster, progress_cls=ProgressTqdm):
    data = get_cfg(cluster).get()
    k8s = K8s.from_manual(data['host'], data['token'], data['port'])
    namespace = f'{scope}-{name}'
    pod_name = next(k8s.list_pods_of_deploy(namespace, f'{name}-{suffix}')).metadata.name
    k8s.get_command_output(lambda: k8s.get_stream(namespace, pod_name), 'python manage.py backup')
    k8s.cp_dir_from_pod(namespace, pod_name, '.dbbackup', dest, progress_cls=progress_cls)


def restore(scope, name, suffix, src, cluster=default_cluster, progress_cls=ProgressTqdm):
    data = get_cfg(cluster).get()
    k8s = K8s.from_manual(data['host'], data['token'], data['port'])
    namespace = f'{scope}-{name}'
    pod_name = next(k8s.list_pods_of_deploy(namespace, f'{name}-{suffix}')).metadata.name
    k8s.cp_dir_to_pod(namespace, pod_name, src, '.dbbackup', progress_cls=progress_cls)
    k8s.get_command_output(lambda: k8s.get_stream(namespace, pod_name), 'python manage.py restore')


def generate_command(app, suffix):
    def _backup(scope, name, dest, cluster=default_cluster):
        backup(scope, name, suffix, dest, cluster)

    def _restore(scope, name, src, cluster=default_cluster):
        restore(scope, name, suffix, src, cluster)

    app.command(name='backup')(_backup)
    app.command(name='restore')(_restore)
