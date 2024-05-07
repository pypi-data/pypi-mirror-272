"""
@Author: kang.yang
@Date: 2023/11/16 17:52
"""
from kytest import module, TestCase, title


@module('pc首页')
class TestApiDemo(TestCase):

    @title('金刚位')
    def test_normal_req(self):
        url = '/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        headers = {
            "user-agent-web": "X/b67aaff2200d4fc2a2e5a079abe78cc6"
        }
        params = {"type": 2}
        self.post(url, headers=headers, json=params)
        self.assertEq('data[*].showType', 2)
