from re import S


def get_build_status(gateway):
    status = gateway.get_project_build_status()
    return status

def build_project(repo, gateway, branch, ci_file):
    build = gateway.build(
        branch=branch,
        ci_file=ci_file
    )
    # result = repo.save(build)
    # if result: 
    build.pop('_id')
    return build

def build_list(repo):
    build_list = repo.list()
    return build_list