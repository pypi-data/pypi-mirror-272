# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/5/10
@Software: PyCharm
@disc:
======================================="""
LOCAL_REGION_CODE = 'CN'
AGENT_DOMAINS = {
    "CN": [
        "github.com",
        "api.github.com"
    ]
}
if __name__ == '__main__':
    x = AGENT_DOMAINS[LOCAL_REGION_CODE]
    print(type(x), x)
    res = "github.com" in x
    print(res)
    y = ["github.com", "api.github.com"]
    print(type(y), y)
    print("github.com" in y)
