from urllib import request
from deployment_service.gateways.input.git.git_input import GitInputGateway

p_name = ''
class TestGitOutputGateway(object):

    def test_001_clone_repo(self):
        git_gw = GitInputGateway()
        repo = git_gw.clone_repo('https://gitlab.dev.smartclide.eu/pberrocal/wellness_challenge')
        print(repo)
        assert repo

    def test_002_write_cdci_file(self):
        git_gw = GitInputGateway()
        result = git_gw.write_cdci_file('/tmp/repos/wellness_challenge/')
        print(result)
        assert result 


    def test_003_commit_changes(self):
        git_gw = GitInputGateway()
        result = git_gw.commit_changes('/tmp/repos/wellness_challenge/')
        print(result)
        assert result

    # def test_004_update_remote(self):
    #     git_gw = GitInputGateway()
    #     remote_url = 'https://pberrocal:oEFB82mtzww5S7-JA2n9@gitlab.dev.smartclide.eu/pberrocal/wellness_challenge.git'
    #     result = git_gw.update_remote('/tmp/repos/wellness_challenge/', remote_url)
    #     print(result)
    #     assert result
    
    def test_005_push_changes(self):
        git_gw = GitInputGateway()
        result = git_gw.push_repository('/tmp/repos/wellness_challenge/')
        print(result)
        assert result