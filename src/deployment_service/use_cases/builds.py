
def get_build_status(gateway):
    status = gateway.get_project_build_status()
    return status

def build_project(repo, gateway, branch, ci_file):
    build = gateway.build(
        branch=branch,
        ci_file=ci_file
    )
    return build

def build_list(gateway):
    build_list = gateway.get_builds_list()
    return build_list